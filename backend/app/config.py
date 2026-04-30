"""FDA 警告信系统 — 全局配置
从环境变量读取配置，支持 .env 文件，所有字段有默认值。
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── 数据库 ──────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///data/fda_warning.db"
    DATA_DIR: str = "data"
    CORS_ORIGINS: list[str] = ["*"]

    # ── Cloudflare AI（LLM 分析流水线）───────────────────────
    CF_EMAIL: str = ""
    CF_API_KEY: str = ""
    CF_ACCOUNT_ID: str = ""

    # ── Telegram 推送 ──────────────────────────────────────
    TELEGRAM_BOT_TOKEN: str = ""

    model_config = {"env_file": ".env"}


# 全局单例，应用启动后通过 get_settings() 获取
settings = Settings()
