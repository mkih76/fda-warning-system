#!/usr/bin/env python3
"""
FDA 爬虫定时任务调度器
每天凌晨 2:00 增量同步 XLSX
每周日凌晨 3:00 增量爬取全文
"""
import sys
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = '/root/fda-warning-system/backend'


def run_xlsx_sync():
    logger.info("🗓️ [XLSX Sync] 开始增量同步...")
    result = subprocess.run(
        [sys.executable, f"{BASE_DIR}/app/crawler/xlsx_sync.py"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        logger.info("✅ XLSX 同步成功")
    else:
        logger.error(f"❌ XLSX 同步失败:\n{result.stderr[-500:]}")


def run_fulltext_crawl():
    logger.info("🗓️ [Fulltext Crawl] 开始增量爬取全文...")
    result = subprocess.run(
        [sys.executable, f"{BASE_DIR}/app/crawler/fulltext.py", "--limit", "100", "--delay", "0.5"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        logger.info("✅ 全文爬取完成")
    else:
        logger.error(f"❌ 全文爬取失败:\n{result.stderr[-500:]}")


def main():
    scheduler = BlockingScheduler()

    # 每天凌晨 2:00 — XLSX 增量同步
    scheduler.add_job(
        run_xlsx_sync,
        CronTrigger(hour=2, minute=0),
        id='xlsx_sync',
        name='FDA XLSX 每日增量同步',
        replace_existing=True,
    )

    # 每周日凌晨 3:00 — 全文爬取
    scheduler.add_job(
        run_fulltext_crawl,
        CronTrigger(day_of_week='sun', hour=3, minute=0),
        id='fulltext_crawl',
        name='FDA 全文每周爬取',
        replace_existing=True,
    )

    logger.info("⏰ FDA 爬虫调度器启动")
    logger.info("   XLSX 同步: 每天 02:00")
    logger.info("   全文爬取: 每周日 03:00")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("👋 调度器已停止")
        sys.exit(0)


if __name__ == "__main__":
    main()
