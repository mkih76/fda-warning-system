"""
FDA Warning Letter LLM Analysis Pipeline
三步流水线：翻译 → 分类 → 摘要
"""
import os
import sys
import re
import json
import time
import httpx
from pathlib import Path
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.app.database import SessionLocal
from backend.app import models

# ── NVIDIA NIM ────────────────────────────────────────────────────
NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"
NIM_API_KEY = "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"

# ── LLM 模型配置 ───────────────────────────────────────────────────
# 全用 llama-3.3-70b-instruct (NIM)，三步不同 system prompt
MODELS = {
    "translate": {
        "model": "meta/llama-3.3-70b-instruct",
        "system": (
            "You are a professional pharmaceutical regulatory translator. "
            "Translate the FDA Warning Letter text below into Chinese (Simplified). "
            "Preserve all section headers, regulatory terminology, and proper nouns. "
            "Output ONLY the Chinese translation, no commentary."
        ),
    },
    "classify": {
        "model": "meta/llama-3.3-70b-instruct",
        "system": (
            "You are a pharmaceutical CGMP compliance expert. "
            "Analyze this FDA Warning Letter and classify it by CGMP violation system. "
            "Choose ONE from: Quality System | Production System | Facility and Equipment | "
            "Materials System | Personnel | Production and Process Controls | "
            "Laboratory Controls | Information Systems | Other. "
            "Also assess risk level: High | Medium | Low.\n\n"
            "Output ONLY valid JSON with keys: violation_type, risk_level, key_findings (array of 3-5 strings). "
            "No markdown, no explanation."
        ),
    },
    "summarize": {
        "model": "meta/llama-3.3-70b-instruct",
        "system": (
            "You are a pharmaceutical intelligence analyst. "
            "Summarize the Chinese FDA Warning Letter translation into a concise, structured "
            "business intelligence brief. Include: 1) Company & product scope, "
            "2) Core CGMP violations found, 3) FDA's key demands, 4) Business risk implications. "
            "Write in professional Chinese, 200-400 characters. "
            "Output ONLY the summary text."
        ),
    },
}

TIMEOUT = 120  # seconds per LLM call


def strip_think(text: str) -> str:
    """Remove think tags from qwq output."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def call_llm(model: str, system_prompt: str, user_prompt: str, is_json: bool = False) -> str:
    """Call NVIDIA NIM API."""
    headers = {
        "Authorization": f"Bearer {NIM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2 if not is_json else 0.1,
        "max_tokens": 4096,
    }
    if is_json:
        payload["response_format"] = {"type": "json_object"}

    try:
        resp = httpx.post(f"{NIM_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return content
    except httpx.HTTPStatusError as e:
        return f"[HTTP {e.response.status_code}] {e.response.text[:200]}"
    except Exception as e:
        return f"[ERROR] {str(e)}"


def analyze_letter(letter_id: int, dry_run: bool = False) -> dict:
    """
    Run full 3-step LLM pipeline on a single letter.
    Returns dict with translation_zh, summary_zh, violation_type, risk_level, key_findings.
    """
    db = SessionLocal()
    try:
        letter = db.query(models.WarningLetter).filter(
            models.WarningLetter.id == letter_id
        ).first()
        if not letter:
            return {"error": f"Letter {letter_id} not found"}

        full_text = letter.full_text or ""
        if not full_text.strip():
            return {"error": f"Letter {letter_id} has no full_text"}

        result = {}

        # ── Step 1: Translate (qwq-32b) ─────────────────────────────
        print(f"  [1/3] Translating letter {letter_id} with qwq-32b...")
        translate_prompt = f"Translate this FDA Warning Letter to Chinese:\n\n{full_text[:8000]}"
        raw_translation = call_llm(
            MODELS["translate"]["model"],
            MODELS["translate"]["system"],
            translate_prompt,
        )
        translation = strip_think(raw_translation)
        result["translation_zh"] = translation
        if translation.startswith("[ERROR]") or translation.startswith("[HTTP"):
            print(f"    ⚠️  Translation failed: {translation[:100]}")
            result["error"] = translation
            return result
        print(f"    ✓  Translation done ({len(translation)} chars)")

        # ── Step 2: Classify (llama-3.3-70b) ────────────────────────
        print(f"  [2/3] Classifying letter {letter_id} with llama-3.3-70b...")
        classify_prompt = f"Analyze this FDA Warning Letter:\n\n{full_text[:6000]}"
        raw_classify = call_llm(
            MODELS["classify"]["model"],
            MODELS["classify"]["system"],
            classify_prompt,
            is_json=True,
        )
        try:
            classify_data = json.loads(raw_classify)
            result["violation_type"] = classify_data.get("violation_type", "Other")
            result["risk_level"] = classify_data.get("risk_level", "Medium")
            result["key_findings"] = classify_data.get("key_findings", [])
        except json.JSONDecodeError:
            print(f"    ⚠️  Classification JSON parse failed, using defaults")
            result["violation_type"] = "Other"
            result["risk_level"] = "Medium"
            result["key_findings"] = []
        print(f"    ✓  Classified: {result['violation_type']} ({result['risk_level']})")

        # ── Step 3: Summarize (qwen2.5-coder-32b) ─────────────────
        print(f"  [3/3] Summarizing letter {letter_id} with qwen2.5-coder-32b...")
        summarize_prompt = f"Summarize this Chinese FDA Warning Letter:\n\n{translation[:6000]}"
        summary = call_llm(
            MODELS["summarize"]["model"],
            MODELS["summarize"]["system"],
            summarize_prompt,
        )
        result["summary_zh"] = summary
        if summary.startswith("[ERROR]") or summary.startswith("[HTTP"):
            print(f"    ⚠️  Summary failed: {summary[:100]}")
        else:
            print(f"    ✓  Summary done ({len(summary)} chars)")

        if dry_run:
            print(f"  [DRY RUN] Would save results to DB")
            return result

        # ── Save to DB ──────────────────────────────────────────────
        existing = db.query(models.AIAnalysis).filter(
            models.AIAnalysis.letter_id == letter_id
        ).first()
        if existing:
            existing.translation_zh = result.get("translation_zh")
            existing.summary_zh = result.get("summary_zh")
            existing.violation_type = result.get("violation_type")
            existing.risk_level = result.get("risk_level")
            existing.key_findings = result.get("key_findings")
        else:
            analysis = models.AIAnalysis(
                letter_id=letter_id,
                translation_zh=result.get("translation_zh"),
                summary_zh=result.get("summary_zh"),
                violation_type=result.get("violation_type"),
                risk_level=result.get("risk_level"),
                key_findings=result.get("key_findings"),
            )
            db.add(analysis)

        # Also update letter violation_type field
        letter.violation_type = result.get("violation_type")

        db.commit()
        print(f"  ✓  Saved AIAnalysis to DB for letter {letter_id}")
        return result

    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()


def batch_analyze(limit: int = 10, skip_done: bool = True, dry_run: bool = False):
    """
    Find letters with full_text but no AIAnalysis, run pipeline.
    """
    db = SessionLocal()
    try:
        q = db.query(models.WarningLetter).filter(
            models.WarningLetter.full_text.isnot(None),
            models.WarningLetter.full_text != "",
        )
        if skip_done:
            q = q.filter(
                ~models.WarningLetter.id.in_(
                    db.query(models.AIAnalysis.letter_id)
                )
            )
        letters = q.limit(limit).all()
        total = q.count()

        print(f"\n🔍 Found {len(letters)} letters to analyze (total candidates: {total})")
        print(f"   Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print(f"   Models: translate=qwq-32b, classify=llama-3.3-70b, summarize=qwen2.5-coder-32b")
        print()

        success = 0
        failed = 0
        for i, letter in enumerate(letters, 1):
            print(f"[{i}/{len(letters)}] Processing letter {letter.id}: {letter.company_name[:50]}")
            result = analyze_letter(letter.id, dry_run=dry_run)
            if "error" in result and "not found" not in result["error"] and "no full_text" not in result["error"]:
                print(f"   ❌ Error: {result['error'][:100]}")
                failed += 1
            else:
                if "error" in result:
                    print(f"   ⚠️  {result['error'][:80]}")
                success += 1
            time.sleep(1)  # rate limit

        print(f"\n📊 Batch complete: {success} success, {failed} failed")
        return {"success": success, "failed": failed}

    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="FDA Warning Letter LLM Analysis")
    parser.add_argument("--limit", type=int, default=10, help="Max letters to analyze")
    parser.add_argument("--id", type=int, help="Analyze specific letter ID only")
    parser.add_argument("--dry-run", action="store_true", help="Don't save to DB")
    args = parser.parse_args()

    if args.id:
        result = analyze_letter(args.id, dry_run=args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        batch_analyze(limit=args.limit, dry_run=args.dry_run)
