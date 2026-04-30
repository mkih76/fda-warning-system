"""
定时任务调度器
负责调度RSS同步、AI内容生成等定时任务
"""

import asyncio
from datetime import datetime, time
from typing import Callable, Awaitable
import signal
import sys


class TaskScheduler:
    """任务调度器"""

    def __init__(self):
        self.tasks = {}
        self.running = False
        self._stop_event = asyncio.Event()

    def add_daily_task(
        self,
        name: str,
        func: Callable[[], Awaitable],
        hour: int = 0,
        minute: int = 0,
        **kwargs,
    ):
        """添加每日任务"""
        self.tasks[name] = {
            'func': func,
            'schedule': 'daily',
            'hour': hour,
            'minute': minute,
            'kwargs': kwargs,
            'last_run': None,
            'running': False,
        }
        print(f"📅 添加每日任务: {name} ({hour:02d}:{minute:02d})")

    def add_interval_task(
        self,
        name: str,
        func: Callable[[], Awaitable],
        interval_minutes: int = 60,
        **kwargs,
    ):
        """添加间隔任务"""
        self.tasks[name] = {
            'func': func,
            'schedule': 'interval',
            'interval_minutes': interval_minutes,
            'kwargs': kwargs,
            'last_run': None,
            'running': False,
        }
        print(f"⏰ 添加间隔任务: {name} (每 {interval_minutes} 分钟)")

    async def start(self):
        """启动调度器"""
        print("\n🚀 任务调度器启动\n")

        self.running = True

        # 设置信号处理
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                asyncio.get_event_loop().add_signal_handler(sig, self._handle_signal)
            except NotImplementedError:
                # Windows不支持add_signal_handler
                pass

        # 启动调度循环
        await self._run_loop()

    async def _run_loop(self):
        """主调度循环"""
        while self.running and not self._stop_event.is_set():
            now = datetime.now()

            for name, task in self.tasks.items():
                if task['running']:
                    continue

                should_run = False

                if task['schedule'] == 'daily':
                    target_time = time(task['hour'], task['minute'])
                    current_time = now.time()

                    if (
                        abs(current_time.hour - target_time.hour) == 0
                        and abs(current_time.minute - target_time.minute) <= 1
                        and (task['last_run'] is None or task['last_run'].date() < now.date())
                    ):
                        should_run = True

                elif task['schedule'] == 'interval':
                    if task['last_run'] is None:
                        should_run = True
                    else:
                        elapsed = (now - task['last_run']).total_seconds() / 60
                        if elapsed >= task['interval_minutes']:
                            should_run = True

                if should_run:
                    print(f"\n{'='*60}")
                    print(f"▶️  执行任务: {name}")
                    print(f"   时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"{'='*60}\n")

                    task['running'] = True
                    asyncio.create_task(self._execute_task(name, task))

            await asyncio.sleep(60)

    async def _execute_task(self, name: str, task: dict):
        """执行单个任务"""
        try:
            await task['func'](**task['kwargs'])
            task['last_run'] = datetime.now()
            print(f"\n✅ 任务完成: {name}\n")
        except Exception as e:
            print(f"\n❌ 任务失败: {name}")
            print(f"   错误: {e}\n")
        finally:
            task['running'] = False

    def _handle_signal(self):
        """处理停止信号"""
        print("\n\n🛑 收到停止信号，正在关闭...\n")
        self.running = False
        self._stop_event.set()

    def stop(self):
        """停止调度器"""
        self.running = False
        self._stop_event.set()

    def get_status(self) -> dict:
        """获取任务状态"""
        status = {
            'running': self.running,
            'tasks': {},
        }

        for name, task in self.tasks.items():
            status['tasks'][name] = {
                'schedule': task['schedule'],
                'last_run': task['last_run'].isoformat() if task['last_run'] else None,
                'running': task['running'],
            }

        return status


scheduler = TaskScheduler()


async def setup_scheduler():
    """设置所有定时任务"""
    from .rss_sync import run_rss_sync

    scheduler.add_daily_task(
        name='rss_sync_all',
        func=run_rss_sync,
        hour=2,
        minute=0,
        sector=None,
    )

    print("\n✅ 定时任务配置完成\n")


async def start_scheduler():
    """启动调度器（用于独立进程）"""
    await setup_scheduler()
    await scheduler.start()


if __name__ == '__main__':
    print("🎯 启动定时任务调度器\n")

    try:
        asyncio.run(start_scheduler())
    except KeyboardInterrupt:
        print("\n\n👋 调度器已停止\n")
        sys.exit(0)
