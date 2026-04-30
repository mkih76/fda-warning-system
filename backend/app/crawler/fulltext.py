#!/usr/bin/env python3
"""
全文爬虫 - 用 httpx 抓取 FDA 警告信 HTML 全文
"""
import sys
import re
import sqlite3
import time
from typing import Optional

import httpx

DB_PATH = '/root/data/fda_warning.db'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def clean_html(raw_html: str) -> str:
    """去掉 nav, footer, sidebar，保留正文"""
    # 移除 script / style
    html = re.sub(r'<script[^>]*>.*?</script>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # 移除 nav / footer / aside
    html = re.sub(r'<(?:nav|footer|aside|header)[^>]*>.*?</(?:nav|footer|aside|header)>',
                  '', html, flags=re.DOTALL | re.IGNORECASE)
    # 折叠多余空白
    html = re.sub(r'\n\s*\n+', '\n\n', html)
    return html.strip()


def fetch_fulltext(url: str, timeout: int = 30) -> Optional[str]:
    """抓取单封信的 HTML 全文"""
    try:
        with httpx.Client(timeout=timeout, headers=HEADERS, follow_redirects=True) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return clean_html(resp.text)
    except httpx.TimeoutException:
        print(f"   ⏱️ 超时: {url}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"   ⚠️ HTTP {e.response.status_code}: {url}")
        return None
    except Exception as e:
        print(f"   ❌ {e}: {url}")
        return None


def crawl_letter(letter_id: int, url: str, delay: float = 0.5) -> bool:
    """抓取单封信，返回是否成功"""
    time.sleep(delay)  # 礼貌爬虫，避免被拦
    html = fetch_fulltext(url)
    if html is None or len(html) < 500:
        return False

    # 提取纯文本
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE warning_letters SET full_text = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (text, letter_id)
    )
    conn.commit()
    conn.close()
    return True


def crawl_batch(limit: int = 50, delay: float = 0.5):
    """抓取下一批未下载全文的信"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, url FROM warning_letters
        WHERE url IS NOT NULL AND url != ''
          AND (full_text IS NULL OR full_text = '' OR LENGTH(full_text) < 100)
        ORDER BY issue_date DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("✅ 全部信已下载完毕")
        return

    print(f"📥 待抓取: {len(rows)} 封")
    success = 0
    for i, (lid, url) in enumerate(rows, 1):
        print(f"[{i}/{len(rows)}] 抓取 id={lid} ...", end=" ")
        if crawl_letter(lid, url, delay):
            print("✅")
            success += 1
        else:
            print("❌")

    print(f"\n📊 批量完成: {success}/{len(rows)} 成功")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="FDA 警告信全文爬虫")
    parser.add_argument("--limit", type=int, default=50, help="每次抓多少封")
    parser.add_argument("--delay", type=float, default=0.5, help="请求间隔(秒)")
    args = parser.parse_args()

    crawl_batch(limit=args.limit, delay=args.delay)


if __name__ == "__main__":
    main()
