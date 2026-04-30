"""
Cloudflare Workers AI 调用封装
用于警告信翻译、分类、摘要生成（充分利用 CF 免费额度）。

已测试可用模型（2026-04）：
  - @cf/qwen/qwq-32b          → 推理/翻译（需剥离 think 标签）
  - @cf/meta/llama-3.3-70b-instruct-fp8-fast  → 结构化输出/分类
  - @cf/qwen/qwen2.5-coder-32b-instruct       → 摘要/通用
  - @cf/deepseek-ai/deepseek-r1-distill-qwen-32b → 推理（需剥离 think 标签）
"""
import json
import logging
import re

import httpx
from typing import Optional

logger = logging.getLogger(__name__)

CF_BASE = "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1/chat/completions"

MODELS = {
    "translate": "@cf/qwen/qwq-32b",                              # 英→中翻译
    "classify": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",       # 违规分类
    "summarize": "@cf/qwen/qwen2.5-coder-32b-instruct",           # 摘要
}


def _strip_think(text: str) -> str:
    """去掉推理模型产出的 \<think\>...\</think\> 思维链标签"""
    cleaned = re.sub(r'<think>.*?</think>', '', text, count=1, flags=re.DOTALL)
    return cleaned.strip()


def _extract_json(text: str):
    """从模型输出中尽力提取并解析 JSON 对象/数组"""
    if not text:
        return None
    # 去掉 think 标签
    text = _strip_think(text)
    # 去掉 markdown 代码块标记
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 尝试提取 [...]
    m = re.search(r'\[.*?\]', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    # 尝试提取 {...}
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    return None


class CloudflareAI:
    """Cloudflare Workers AI 客户端"""

    def __init__(self, email: str, api_key: str, account_id: str):
        self.email = email
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = CF_BASE.format(account_id=account_id)

    async def chat(self, model: str, messages: list, max_tokens: int = 2048) -> Optional[str]:
        """调用 CF Workers AI，返回文本内容或 None"""
        headers = {
            "X-Auth-Email": self.email,
            "X-Auth-Key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
        }
        try:
            async with httpx.AsyncClient(timeout=90) as client:
                resp = await client.post(self.base_url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                # CF Workers AI 不同模型返回格式不同：
                #   str  → 文本（Qwen, DeepSeek）
                #   list → 已解析 JSON（LLaMA 70B）
                #   None → 不支持（GLM, Gemma）
                if isinstance(content, (list, dict)):
                    return json.dumps(content, ensure_ascii=False)
                return content if content else None
        except Exception as e:
            logger.error(f"CF AI [{model}] 调用失败: {e}")
            return None

    async def translate(self, text: str) -> Optional[str]:
        """英译中 — QwQ 模型，需剥离思维链"""
        prompt = f"将以下 FDA 警告信内容翻译为中文，保持专业术语准确性：\n\n{text[:3000]}"
        raw = await self.chat(MODELS["translate"], [
            {"role": "user", "content": prompt}
        ], max_tokens=4096)
        if raw:
            return _strip_think(raw)
        return raw

    async def classify_violations(self, text: str) -> Optional[list]:
        """违规分类 — LLaMA 70B，要求严格 JSON 数组输出"""
        prompt = f"""Analyze the following FDA Warning Letter and classify violations into Chinese categories.
Output ONLY a valid JSON array, no other text:

The six systems are:
- 质量系统 (quality system)
- 生产系统 (production system)
- 实验室控制 (laboratory control)
- 物料系统 (materials system)
- 设施设备 (facility/equipment system)
- 包装标签 (packaging/labeling system)

Format:
[{{"system": "质量系统", "type": "deviation type", "severity": "high/medium/low", "description": "violation description"}}]

Warning Letter:
{text[:4000]}"""
        result = await self.chat(MODELS["classify"], [
            {"role": "user", "content": prompt}
        ])
        if result:
            parsed = _extract_json(result)
            if parsed and isinstance(parsed, list):
                return parsed
            logger.warning(f"分类结果解析失败: {result[:150]}")
        return None

    async def summarize(self, text: str) -> Optional[dict]:
        """生成中文摘要 — Qwen Coder，要求严格 JSON 对象输出"""
        prompt = f"""Generate a short Chinese summary (about 100 chars) of this FDA Warning Letter.
Output ONLY a valid JSON object, no other text:
{{"summary_zh": "...", "key_risks": ["risk1", "risk2"]}}

Warning Letter:
{text[:3000]}"""
        result = await self.chat(MODELS["summarize"], [
            {"role": "user", "content": prompt}
        ])
        if result:
            parsed = _extract_json(result)
            if parsed and isinstance(parsed, dict):
                return parsed
            # 保底：直接把文本当摘要
            return {"summary_zh": _strip_think(result)[:200], "key_risks": []}
        return None
