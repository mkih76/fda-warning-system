#!/usr/bin/env python3
"""FDA警告信原文预处理 — 清理网页导航/页脚等非正文内容"""
import re

# 需要移除的导航/页脚模式
NAV_PATTERNS = [
    r'跳至主要内容', r'跳至FDA搜索', r'跳至本节菜单', r'跳至页脚链接',
    r'跳至主内容', r'跳至FDA\s*搜索', r'跳至本部分菜单', r'跳至页脚',
    r'Skip to main content', r'Skip to FDA Search', r'Skip to in this section menu',
    r'Skip to footer links',
    r'首页\s*检查、合规、执法和刑事调查', r'合规行动和活动\s*警告信',
    r'主页\s*检查、合规、执法和刑事调查',
    r'Home\s*Inspections?,\s*Compliance?,\s*Enforcement?,?\s*and?\s*Criminal\s*Investigations?',
    r'Compliance?\s*Actions?\s*and\s*Activities?\s*Warning\s*Letters?',
]

FOOTER_PATTERNS = [
    r'在Facebook上关注FDA', r'在X上关注FDA', r'在Instagram上关注FDA',
    r'在LinkedIn上关注FDA', r'在YouTube上观看FDA视频',
    r'订阅FDA\s*RSS源', r'联系电话\s*1-888-INFO-FDA.*?返回顶部',
    r'1-888-INFO-FDA\s*\(1-888-463-6332\)', r'返回顶部',
    r'反馈\s*联系FDA', r'Contact\s*FDA', r'Follow\s*FDA\s*on',
    r'Subscribe\s*to\s*FDA\s*RSS', r'Phone\s*1-888-INFO-FDA',
    r'返回FDA首页', r'Back\s*to\s*Top',
    r'在Facebook上.*?在X上.*?在Instagram上.*?在LinkedIn上.*?在YouTube上.*?订阅FDA',
]

# 需要移除的HTML标签残留
HTML_PATTERNS = [
    r'<[^>]+>',  # HTML标签
    r'&nbsp;', r'&amp;', r'&lt;', r'&gt;', r'&quot;',
    r'&#\d+;',
]


def clean_fulltext(text):
    """清理FDA警告信原文，移除网页导航/页脚等非正文内容"""
    if not text:
        return text
    
    original_len = len(text)
    
    # 1. 移除HTML标签
    for pattern in HTML_PATTERNS[:1]:
        text = re.sub(pattern, '', text)
    # 移除HTML实体
    for pattern in HTML_PATTERNS[1:]:
        text = re.sub(pattern, ' ', text)
    
    # 2. 移除导航栏文字
    for pattern in NAV_PATTERNS:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # 3. 移除页脚内容
    # 先尝试移除整个页脚块（从"反馈 联系FDA"或"Contact FDA"到结尾）
    footer_start = None
    for marker in ['反馈 联系FDA', 'Contact FDA', 'Follow FDA on', 'Subscribe to FDA', 
                   '1-888-INFO-FDA', '返回顶部', 'Back to Top']:
        idx = text.find(marker)
        if idx != -1:
            if footer_start is None or idx < footer_start:
                footer_start = idx
    
    if footer_start and footer_start > len(text) * 0.5:  # 页脚通常在后半部分
        text = text[:footer_start]
    
    # 4. 逐行清理残留的页脚/导航片段
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            cleaned_lines.append('')
            continue
        
        # 跳过纯导航行
        skip = False
        for pattern in NAV_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                skip = True
                break
        if skip:
            continue
        
        # 跳过纯页脚行
        skip = False
        for pattern in FOOTER_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                skip = True
                break
        if skip:
            continue
        
        # 跳过面包屑导航行（如 "首页 > 检查 > 合规 > 警告信"）
        if re.match(r'^(首页|主页|Home)\s*[>›/]', line):
            continue
        
        # 跳过社交媒体链接行
        if re.match(r'^(Follow|关注|订阅|Subscribe)', line, re.IGNORECASE):
            continue
        
        cleaned_lines.append(line)
    
    # 5. 合并连续空行为单个
    text = '\n'.join(cleaned_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 6. 去除首尾空白
    text = text.strip()
    
    cleaned_len = len(text)
    reduction = (1 - cleaned_len / original_len) * 100 if original_len > 0 else 0
    
    return text


def extract_letter_sections(text):
    """将清理后的原文按结构分段"""
    sections = {}
    
    # 提取日期
    date_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', text)
    if date_match:
        sections['date'] = date_match.group(1)
    
    # 提取称呼
    dear_match = re.search(r'(Dear\s+(?:Mr|Ms|Mrs|Dr)\.?\s+[^:]+:)', text)
    if dear_match:
        sections['salutation'] = dear_match.group(1)
    
    # 提取签名
    sincerely_match = re.search(r'(Sincerely,?\s*\n[\s\S]*?)$', text)
    if sincerely_match:
        sections['signature'] = sincerely_match.group(1).strip()
    
    # 提取正文（去掉日期、称呼、签名）
    body = text
    if 'date' in sections:
        body = body.replace(sections['date'], '', 1)
    if 'salutation' in sections:
        body = body.split(sections['salutation'])[-1]
    if 'signature' in sections:
        body = body.split(sections['signature'])[0]
    
    sections['body'] = body.strip()
    
    return sections


if __name__ == '__main__':
    import sqlite3
    DB = '/root/data/fda_warning.db'
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    c.execute('SELECT id, fda_id, full_text FROM warning_letters WHERE full_text IS NOT NULL AND full_text != ""')
    rows = c.fetchall()
    
    total = len(rows)
    cleaned = 0
    for row in rows:
        lid, fda_id, text = row
        cleaned_text = clean_fulltext(text)
        if cleaned_text != text:
            cleaned += 1
            # 保存清洗后的原文
            c.execute('UPDATE warning_letters SET full_text_clean = ? WHERE id = ?', (cleaned_text, lid))
    
    conn.commit()
    print(f'原文预处理完成: {cleaned}/{total} 封已清洗')
    conn.close()
