#!/usr/bin/env python3
"""翻译质量校验脚本"""
import re

# AI总结性词汇
AI_MARKERS = [
    '总之', '综上所述', '总结', '概括来说', '简而言之',
    '值得注意的是', '需要指出', '关键要点', '主要发现',
    '总的来说', '简单来说', '概括地说', '总结如下',
    '总而言之', '概括而言', '要而言之',
]

# 网页导航残留
NAV_MARKERS = [
    '跳至', '跳转到', '首页', '主页', '返回顶部',
    '在Facebook上', '在X上', '在Instagram上', '在LinkedIn上',
    '订阅FDA', '联系电话', '返回FDA',
]

# FDA页脚残留
FOOTER_MARKERS = [
    '1-888-INFO-FDA', '返回顶部', '反馈 联系FDA',
    'Follow FDA', 'Subscribe to FDA', 'Back to Top',
]


def validate_translation(zh_text, en_text):
    """校验翻译质量，返回 (score, issues)"""
    issues = []
    score = 100
    
    if not zh_text or not en_text:
        return 0, ['翻译或原文为空']
    
    # 1. 长度比检查 (30%)
    ratio = len(zh_text) / len(en_text) if len(en_text) > 0 else 0
    if ratio < 0.2:
        issues.append(f'翻译过短: {ratio:.2f} (原文{len(en_text)}字, 翻译{len(zh_text)}字)')
        score -= 30
    elif ratio < 0.3:
        issues.append(f'翻译偏短: {ratio:.2f}')
        score -= 15
    elif ratio > 0.9:
        issues.append(f'翻译偏长: {ratio:.2f}')
        score -= 10
    
    # 2. AI总结词检查 (25%)
    found_ai = []
    for marker in AI_MARKERS:
        if marker in zh_text:
            found_ai.append(marker)
    if found_ai:
        issues.append(f'发现AI总结词: {", ".join(found_ai[:5])}')
        score -= 25
    
    # 3. 导航残留检查 (25%)
    found_nav = []
    for marker in NAV_MARKERS:
        if marker in zh_text:
            found_nav.append(marker)
    found_footer = []
    for marker in FOOTER_MARKERS:
        if marker in zh_text:
            found_footer.append(marker)
    if found_nav:
        issues.append(f'发现导航残留: {", ".join(found_nav[:5])}')
        score -= 15
    if found_footer:
        issues.append(f'发现页脚残留: {", ".join(found_footer[:3])}')
        score -= 10
    
    # 4. 段落一致性检查 (20%)
    en_paras = len([p for p in en_text.split('\n\n') if p.strip()])
    zh_paras = len([p for p in zh_text.split('\n\n') if p.strip()])
    if en_paras > 0:
        para_ratio = zh_paras / en_paras
        if para_ratio < 0.5 or para_ratio > 2.0:
            issues.append(f'段落数差异过大: 英文{en_paras}段, 中文{zh_paras}段')
            score -= 20
        elif para_ratio < 0.7 or para_ratio > 1.5:
            issues.append(f'段落数差异较大: 英文{en_paras}段, 中文{zh_paras}段')
            score -= 10
    
    # 5. 英文比例检查
    en_chars = len(re.findall(r'[a-zA-Z]', zh_text))
    if len(zh_text) > 0 and en_chars / len(zh_text) > 0.5:
        issues.append(f'英文比例过高: {en_chars/len(zh_text):.1%}')
        score -= 15
    
    # 6. 最小长度检查
    if len(zh_text) < 200:
        issues.append(f'翻译过短: {len(zh_text)}字')
        score -= 20
    
    score = max(0, score)
    return score, issues


def quality_grade(score):
    """质量等级"""
    if score >= 90: return 'A'
    if score >= 80: return 'B'
    if score >= 70: return 'C'
    if score >= 60: return 'D'
    return 'F'


if __name__ == '__main__':
    import sqlite3
    DB = '/root/data/fda_warning.db'
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    c.execute('''
        SELECT w.id, w.fda_id, w.full_text, a.translation_zh 
        FROM ai_analysis a 
        JOIN warning_letters w ON a.warning_letter_id = w.id 
        WHERE a.translation_zh IS NOT NULL AND a.translation_zh != ''
    ''')
    rows = c.fetchall()
    
    grades = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    all_issues = []
    
    for row in rows:
        lid, fda_id, en, zh = row
        score, issues = validate_translation(zh, en)
        grade = quality_grade(score)
        grades[grade] += 1
        if issues:
            all_issues.append((lid, fda_id, score, grade, issues))
    
    print(f'=== 翻译质量校验结果 ({len(rows)}封) ===')
    for g in ['A', 'B', 'C', 'D', 'F']:
        print(f'  {g}: {grades[g]}封 ({grades[g]*100/len(rows):.1f}%)')
    print(f'  总问题: {len(all_issues)}封')
    
    if all_issues:
        print('\n=== 问题详情（前10封）===')
        for lid, fda_id, score, grade, issues in sorted(all_issues, key=lambda x: x[2])[:10]:
            print(f'  [{grade}] id={lid} {fda_id} (评分{score})')
            for issue in issues:
                print(f'    - {issue}')
    
    conn.close()
