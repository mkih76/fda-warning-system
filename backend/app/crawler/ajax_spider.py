"""
FDA Drupal Views AJAX 列表爬虫
通过 FDA.gov 的 Drupal Views AJAX 接口获取警告信列表。
"""
import logging
import re
import httpx

logger = logging.getLogger(__name__)

AJAX_URL = "https://www.fda.gov/views/ajax"
VIEW_NAME = "warning_letter_solr_index"
VIEW_DISPLAY = "warning_letter_solr_block"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/x-www-form-urlencoded",
}


class AjaxSpider:
    """FDA 警告信 AJAX 列表爬虫"""

    async def fetch_list_page(self, page: int = 0) -> list[dict]:
        """获取单页列表，返回 [ {title, url, date, ...} ]"""
        data = {
            "view_name": VIEW_NAME,
            "view_display_id": VIEW_DISPLAY,
            "page": page,
        }
        async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
            resp = await client.post(AJAX_URL, data=data)
            resp.raise_for_status()
            return self._parse_list_response(resp.text)

    def _parse_list_response(self, html: str) -> list[dict]:
        """从 AJAX 返回的 HTML 中提取警告信信息"""
        items = []
        # 提取信件 URL 和标题
        pattern = r'<a[^>]*href="(/warning-letters/[^"]+)"[^>]*>([^<]+)</a>'
        for match in re.finditer(pattern, html):
            items.append({
                "url": "https://www.fda.gov" + match.group(1),
                "title": match.group(2).strip(),
            })
        return items

    async def get_total_pages(self) -> int:
        """获取总页数（第一页响应中包含）"""
        items = await self.fetch_list_page(0)
        return len(items)  # 第一页就是全部，AJAX 接口可能直接返回全部

    async def collect_all_urls(self, max_pages: int = 10) -> list[str]:
        """收集多页 URL"""
        all_urls = []
        for page in range(max_pages):
            items = await self.fetch_list_page(page)
            if not items:
                break
            all_urls.extend(item["url"] for item in items)
        return list(set(all_urls))
