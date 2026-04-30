#!/usr/bin/env python3
"""
FDA 警告信数据同步 — CLI 入口

用法:
  cd backend && ../.venv/bin/python -m app.sync_cli
  cd backend && ../.venv/bin/python sync.py     # 或者直接执行
"""
import argparse
import asyncio
import logging
import os
import sys

# 把 app/ 加入包路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


async def check_status():
    from app.database import AsyncSessionLocal
    from app.models import WarningLetter
    from sqlalchemy import select, func

    async with AsyncSessionLocal() as session:
        total = (await session.execute(select(func.count(WarningLetter.id)))).scalar() or 0
        offices = await session.execute(
            select(WarningLetter.issuing_office, func.count(WarningLetter.id))
            .where(WarningLetter.issuing_office.isnot(None))
            .group_by(WarningLetter.issuing_office)
            .order_by(func.count(WarningLetter.id).desc())
        )
        print(f"\n📊 FDA 警告信数据库状态")
        print(f"  ─────────────────────────────────────")
        print(f"  总记录数: {total}")
        print(f"\n  签发办公室分布:")
        for office, cnt in offices:
            print(f"    • {office or '(未知)'}: {cnt} 封")
        print()


async def do_sync():
    """执行同步"""
    print(f"\n📥 FDA 警告信数据同步")
    print(f"  ─────────────────────────────────────")

    from app.database import init_db, AsyncSessionLocal
    from app.crawler.xlsx_sync import XlsxSync

    # 确保数据库表存在
    print("  📦 初始化数据库表...")
    await init_db()

    print("  🌐 下载 FDA XLSX 数据...")
    sync = XlsxSync()

    async with AsyncSessionLocal() as session:
        result = await sync.sync_to_db(session)

    print(f"\n  ✅ 同步完成!")
    print(f"  ─────────────────────────────────────")
    print(f"  新增: {result['new']} 封")
    print(f"  更新: {result['updated']} 封")
    print(f"  XLSX 共: {result['total']} 条")
    print()


async def main():
    parser = argparse.ArgumentParser(description="FDA 警告信数据同步工具")
    parser.add_argument("--check", action="store_true", help="仅查看状态，不做同步")
    args = parser.parse_args()

    if args.check:
        await check_status()
    else:
        await do_sync()
        await check_status()


if __name__ == "__main__":
    asyncio.run(main())
