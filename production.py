"""A production-shaped rewrite call for qwen3.5-4b-32k-fast on LLM Gateway.

- max_tokens sized to the job (the gateway reserves it against your tokens-per-minute limit)
- a fallback model in case the primary request fails
- client-side retries with backoff (the OpenAI SDK honors Retry-After on 429)
- request_id logged with model, region and timestamp for support tickets
- optional streaming for live formatting
"""
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone

from openai import OpenAI

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("rewrite")

BASE_URL = os.environ.get("LLM_GATEWAY_BASE_URL", "https://llm-gateway.assemblyai.com/v1")
MODEL = os.environ.get("REWRITE_MODEL", "qwen3.5-4b-32k-fast")
FALLBACK_MODEL = os.environ.get("REWRITE_FALLBACK_MODEL", "gemini-2.5-flash-lite")

SYSTEM_PROMPT = (
    "Rewrite raw dictation as clean, formatted text. Remove filler words, fix punctuation, "
    "and resolve self-corrections to the speaker's final intent. Return only the rewritten text."
)

client = OpenAI(
    base_url=BASE_URL,
    api_key=os.environ["ASSEMBLYAI_API_KEY"],
    max_retries=3,
    timeout=10.0,
)


def rewrite(raw_text: str) -> str:
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        max_tokens=400,
        temperature=0.2,
        extra_body={"fallbacks": [{"model": FALLBACK_MODEL}]},
    )
    log.info(json.dumps({
        "request_id": getattr(response, "request_id", None),
        "model_requested": MODEL,
        "model_served": response.model,
        "base_url": BASE_URL,
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "latency_s": round(time.perf_counter() - started, 3),
        "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
        "completion_tokens": response.usage.completion_tokens if response.usage else None,
    }))
    return response.choices[0].message.content


def rewrite_stream(raw_text: str) -> None:
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        max_tokens=400,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()


if __name__ == "__main__":
    text = sys.stdin.read().strip() or open("sample_dictation.txt").read().strip()
    if "--stream" in sys.argv:
        rewrite_stream(text)
    else:
        print(rewrite(text))
