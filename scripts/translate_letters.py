#!/usr/bin/env python3
"""
FDA Warning Letter Translation Pipeline
Translates English warning letters to Chinese using NVIDIA NIM API
Filters out *# symbols and formats content like academic papers
"""
import sqlite3
import json
import re
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Config
DB_PATH = "/root/data/fda_warning.db"
NVIDIA_API_KEY = "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"
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL = "nvidia/llama-3.3-nemotron-super-49b-v1"

# Second model for parallel processing (using zyapi)
ZYAPI_KEY = "pk_d0AA5mgktZxhT8wFPBQRTW2r2OkVyWE16qpekFd9Rlk"
ZYAPI_BASE_URL = "https://zyapi.tuluo.top:8888/v1"
ZYAPI_MODEL = "deepseek-v4-flash"

def clean_text(text):
    """Filter out *# symbols and clean up text"""
    if not text:
        return text
    # Remove * and # that are not part of meaningful content
    # Keep them if they're in context like section markers
    text = re.sub(r'\*{2,}', '', text)  # Remove ** (bold markers)
    text = re.sub(r'(?<!\w)\*(?!\w)', '', text)  # Remove standalone *
    text = re.sub(r'(?<!\w)#(?!\w)', '', text)  # Remove standalone #
    text = re.sub(r'#{2,}', '', text)  # Remove ##
    # Clean up multiple spaces
    text = re.sub(r' {3,}', '  ', text)
    # Clean up multiple newlines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()

def format_as_paper(text, company_name="", subject=""):
    """Format the letter content like an academic paper"""
    if not text:
        return text
    
    lines = text.split('\n')
    formatted = []
    
    # Add title
    if company_name:
        formatted.append(f"# {company_name}")
        formatted.append("")
    
    if subject:
        formatted.append(f"**主题：** {subject}")
        formatted.append("")
    
    formatted.append("---")
    formatted.append("")
    
    # Process content
    in_section = False
    for line in lines:
        line = line.strip()
        if not line:
            formatted.append("")
            continue
        
        # Detect section headers (all caps, or starts with number+period)
        if re.match(r'^[A-Z][A-Z\s]{5,}$', line) or re.match(r'^\d+[\.\)]\s+[A-Z]', line):
            formatted.append(f"\n## {line.title()}\n")
            in_section = True
        elif re.match(r'^[A-Z][a-z]+ [A-Z]', line) and len(line) < 80:
            # Possible sub-header
            formatted.append(f"\n### {line}\n")
        else:
            formatted.append(line)
    
    result = '\n'.join(formatted)
    # Clean up excessive newlines
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result

def call_nvidia_api(text, api_key, base_url, model, max_retries=3):
    """Call NVIDIA NIM API for translation"""
    prompt = f"""你是一名专业的法律和监管文件翻译专家，擅长将FDA警告信翻译成中文。

翻译要求：
1. 专业术语保留英文原文（如FDA、CGMP、483、Warning Letter、cGMP等），在首次出现时加括号注释中文含义
2. 公司名称、人名保留英文原文
3. 法律条款引用保留英文编号（如21 CFR Part 211）
4. 日期格式转换为中文习惯（如2024年1月6日）
5. 翻译要准确、专业、流畅，符合中国法规文件的语言风格
6. 过滤掉所有 * # 符号，这些是格式标记不是内容
7. 地址保留英文原文

请将以下FDA警告信翻译为中文：

{text}"""

    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 4096,
    }).encode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    for attempt in range(max_retries):
        try:
            req = Request(f"{base_url}/chat/completions", data=payload, headers=headers)
            with urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
                return data['choices'][0]['message']['content']
        except HTTPError as e:
            if e.code == 429:
                wait = (attempt + 1) * 10
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  API error {e.code}: {e.read().decode()[:200]}")
                time.sleep(5)
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(5)
    return None

def translate_letter(letter_id, full_text, company_name, subject, api_key, base_url, model, model_name):
    """Translate a single letter"""
    if not full_text or len(full_text) < 50:
        return letter_id, None, None, None
    
    # Clean the text first
    cleaned = clean_text(full_text)
    
    # Truncate if too long (API limits)
    if len(cleaned) > 12000:
        cleaned = cleaned[:12000] + "\n\n[内容已截断...]"
    
    print(f"  [{model_name}] Translating letter {letter_id}: {company_name[:30]}...")
    
    # Translate
    translation = call_nvidia_api(cleaned, api_key, base_url, model)
    
    if translation:
        # Clean the translation
        translation = clean_text(translation)
        
        # Generate Chinese subject
        subject_cn = None
        if subject:
            subject_prompt = f"将以下FDA警告信主题翻译为简洁的中文标题（不超过50字），保留专业术语英文原文：\n{subject}"
            payload = json.dumps({
                "model": model,
                "messages": [{"role": "user", "content": subject_prompt}],
                "temperature": 0.3,
                "max_tokens": 200,
            }).encode('utf-8')
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            try:
                req = Request(f"{base_url}/chat/completions", data=payload, headers=headers)
                with urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read())
                    subject_cn = data['choices'][0]['message']['content'].strip()
            except:
                pass
        
        # Generate abstract
        abstract_cn = None
        if len(translation) > 200:
            abstract_prompt = f"请为以下翻译后的FDA警告信生成一段100-150字的中文摘要，概括主要违规事实和FDA要求：\n\n{translation[:3000]}"
            payload = json.dumps({
                "model": model,
                "messages": [{"role": "user", "content": abstract_prompt}],
                "temperature": 0.3,
                "max_tokens": 500,
            }).encode('utf-8')
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            try:
                req = Request(f"{base_url}/chat/completions", data=payload, headers=headers)
                with urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read())
                    abstract_cn = data['choices'][0]['message']['content'].strip()
            except:
                pass
        
        # Format as paper
        formatted = format_as_paper(translation, company_name, subject_cn)
        
        print(f"  [{model_name}] ✓ Letter {letter_id} translated ({len(translation)} chars)")
        return letter_id, formatted, subject_cn, abstract_cn
    
    print(f"  [{model_name}] ✗ Letter {letter_id} failed")
    return letter_id, None, None, None

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get letters that need translation
    cursor.execute("""
        SELECT id, full_text_clean, company_name, subject 
        FROM warning_letters 
        WHERE full_text_clean IS NOT NULL 
        AND length(full_text_clean) > 100
        AND full_text_cn IS NULL
        ORDER BY id
    """)
    letters = cursor.fetchall()
    
    print(f"Found {len(letters)} letters to translate")
    
    if not letters:
        print("All letters already translated!")
        conn.close()
        return
    
    # Split into two batches for parallel processing
    mid = len(letters) // 2
    batch1 = letters[:mid]
    batch2 = letters[mid:]
    
    print(f"Batch 1 (NVIDIA): {len(batch1)} letters")
    print(f"Batch 2 (ZyAPI/DeepSeek): {len(batch2)} letters")
    
    results = []
    
    def process_batch(batch, api_key, base_url, model, model_name):
        batch_results = []
        for i, (lid, text, company, subject) in enumerate(batch):
            result = translate_letter(lid, text, company, subject, api_key, base_url, model, model_name)
            batch_results.append(result)
            # Rate limiting
            if (i + 1) % 5 == 0:
                time.sleep(2)
        return batch_results
    
    # Process both batches concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(process_batch, batch1, NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_MODEL, "NVIDIA")
        future2 = executor.submit(process_batch, batch2, ZYAPI_KEY, ZYAPI_BASE_URL, ZYAPI_MODEL, "DeepSeek")
        
        results1 = future1.result()
        results2 = future2.result()
        results = results1 + results2
    
    # Update database
    updated = 0
    for lid, text_cn, subject_cn, abstract_cn in results:
        if text_cn:
            cursor.execute("""
                UPDATE warning_letters 
                SET full_text_cn = ?, subject_cn = ?, abstract_cn = ?, updated_at = datetime('now')
                WHERE id = ?
            """, (text_cn, subject_cn, abstract_cn, lid))
            updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n=== DONE ===")
    print(f"Translated: {updated}/{len(letters)}")
    print(f"Failed: {len(letters) - updated}")

if __name__ == "__main__":
    main()
