#!/usr/bin/env python3
"""
批量翻译 FDA 警告信：使用 NVIDIA NIM (DeepSeek V4 Flash) 将英文全文翻译为中文
- 读取有 full_text 但无 translation_zh 的信件
- 调用 NVIDIA NIM deepseek-v4-flash 翻译
- 更新 ai_analysis 表的 translation_zh 字段
- 支持中断后恢复（记录已完成的 letter_id）
"""

import sqlite3
import urllib.request
import json
import time
import sys
import os
import re

DB_PATH = "/root/data/fda_warning.db"
NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"
NIM_API_KEY = "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"
NIM_MODEL = "deepseek-ai/deepseek-v4-flash"
BATCH_SIZE = 20
PROGRESS_FILE = "/root/fda-warning-system/translation_progress.txt"
LOG_FILE = "/root/fda-warning-system/translation.log"
REQUEST_DELAY = 2  # 请求间隔（秒），避免限流

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def cleanup_translation(text: str) -> str:
    """清理翻译结果中的HTML残留、杂讯文字，并还原表格格式"""
    # 1. 移除HTML注释和特殊标记
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)  # 移除剩余HTML标签

    # 2. 移除FDA网站导航残留文字
    noise_patterns = [
        r'跳至\s*主要内容.*?(?=\n|$)',
        r'跳至\s*FDA\s*搜索.*?(?=\n|$)',
        r'跳至\s*本节菜单.*?(?=\n|$)',
        r'跳至\s*页脚链接.*?(?=\n|$)',
        r'^\s*主页.*?警告信\s*$',
        r'^\s*检查、?合规.*?刑事调查\s*$',
        r'^\s*合规行动和活动\s*$',
        r'^\s*本节\s*$',
        r'^\s*送达方式.*?(?=\n)',
        r'^\s*产品.*?(?=\n)',
        r'^\s*收件人[：:].*?(?=\n)',
        r'^\s*收件人职务.*?(?=\n)',
        r'^\s*签发办公室.*?(?=\n)',
        r'^\s*次要签发办公室.*?(?=\n)',
        r'^\s*警告信\s*CMS.*?(?=\n)',
        r'^\s*美国\s*$',
    ]
    for p in noise_patterns:
        text = re.sub(p, '', text, flags=re.MULTILINE)

    # 3. 清理多余空白行（超过2个连续空行缩成2个）
    text = re.sub(r'\n{4,}', '\n\n', text)

    # 4. 还原表格格式：识别 "型号 项目描述 型号 项目描述" 类标题行
    # 把连续的 "xxx yyy zzz www" 四列格式转为换行表格
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # 跳过仅含噪声词的单行
        if not stripped:
            cleaned_lines.append(line)
            continue
        # 跳过纯噪声残留
        if re.match(r'^(主页|检查|合规|产品|收件人|签发|次要|警告|CMS|美国|FDA|跳转|Skip to|Search|Menu|Main)', stripped):
            continue
        cleaned_lines.append(line)

    text = '\n'.join(cleaned_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def nim_translate(text: str) -> str:
    """调用 NVIDIA NIM DeepSeek V4 Flash 将英文翻译为中文"""
    url = f"{NIM_BASE_URL}/chat/completions"

    system_prompt = (
        "你是一个专业的医疗法规文档翻译。将英文FDA警告信翻译为简体中文。 "
        "保持格式和换行，公司名、地址、日期、FDA术语保留英文。 "
        "只输出中文翻译，不加任何评论。"
    )

    payload = {
        "model": NIM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        "max_tokens": 8192,
        "temperature": 0.3,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {NIM_API_KEY}")
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib.request.urlopen(req, timeout=300)
        d = json.loads(resp.read())
        choices = d.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "").strip()
        log(f"  NIM API no choices: {d}")
        return None
    except Exception as e:
        log(f"  Request error: {e}")
        return None

def get_letters_to_translate(conn, limit=BATCH_SIZE, skip_ids=None):
    """获取需要翻译的信件列表"""
    skip_clause = ""
    params = []
    if skip_ids:
        placeholders = ",".join("?" * len(skip_ids))
        skip_clause = f"AND wl.id NOT IN ({placeholders})"
        params = skip_ids
    
    query = f"""
        SELECT wl.id, wl.fda_id, wl.full_text
        FROM warning_letters wl
        LEFT JOIN ai_analysis aa ON wl.id = aa.warning_letter_id
        WHERE wl.full_text IS NOT NULL
          AND wl.full_text != ''
          AND wl.full_text != wl.subject
          AND (aa.translation_zh IS NULL OR aa.translation_zh = '')
          AND wl.id % 5 = 4
          {skip_clause}
        ORDER BY wl.id
        LIMIT ?
    """
    params.append(limit)
    
    c = conn.cursor()
    c.execute(query, params)
    return c.fetchall()

def ensure_ai_analysis_row(conn, letter_id):
    """确保 ai_analysis 表有对应行（UPSERT）"""
    c = conn.cursor()
    # 检查是否存在
    c.execute("SELECT id FROM ai_analysis WHERE warning_letter_id = ?", (letter_id,))
    row = c.fetchone()
    if row:
        return row[0]
    # 插入新行
    c.execute(
        "INSERT INTO ai_analysis (warning_letter_id, analyzed_at) VALUES (?, datetime('now'))",
        (letter_id,)
    )
    conn.commit()
    return c.lastrowid

def save_progress(letter_id):
    """记录已完成的最大 letter_id，方便恢复"""
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(letter_id))

def load_progress():
    """加载进度"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return int(f.read().strip())
    return 0

def main():
    log("=== FDA 警告信批量翻译任务启动 ===")
    
    conn = sqlite3.connect(DB_PATH)
    
    # 加载进度
    last_id = load_progress()
    if last_id > 0:
        log(f"从进度恢复：上次处理到 letter_id={last_id}")
    
    total_done = 0
    total_failed = 0
    skip_ids = [last_id] if last_id > 0 else []
    
    while True:
        letters = get_letters_to_translate(conn, limit=BATCH_SIZE, skip_ids=skip_ids if skip_ids else None)
        if not letters:
            log("没有更多需要翻译的信件，任务完成")
            break
        
        log(f"本批获取 {len(letters)} 封信件")
        
        for lid, fda_id, full_text in letters:
            log(f"翻译 letter_id={lid} fda_id={fda_id}...")
            
            # 截断过长的文本（CF token 限制）
            text_to_translate = full_text[:12000]
            if len(full_text) > 8000:
                log(f"  文本较长 ({len(full_text)} 字)，截取前 8000 字翻译")
            
            translation = nim_translate(text_to_translate)
            
            if translation:
                # 清理翻译结果（去除HTML残留、导航杂讯）
                translation = cleanup_translation(translation)

                # 确保 ai_analysis 行存在
                ensure_ai_analysis_row(conn, lid)
                
                # 更新翻译
                c = conn.cursor()
                c.execute(
                    "UPDATE ai_analysis SET translation_zh = ? WHERE warning_letter_id = ?",
                    (translation, lid)
                )
                conn.commit()
                
                log(f"  ✓ 完成 ({len(translation)} 字)")
                total_done += 1
                save_progress(lid)
            else:
                log(f"  ✗ 翻译失败，跳过")
                total_failed += 1
            
            # 频率限制
            time.sleep(REQUEST_DELAY)
        
        # 每批后稍作停顿
        time.sleep(2)
    
    conn.close()
    log(f"=== 任务结束：成功 {total_done}，失败 {total_failed} ===")

if __name__ == "__main__":
    main()
