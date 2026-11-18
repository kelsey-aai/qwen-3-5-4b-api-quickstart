"""Print Qwen3.5 4B Fast's Voice Standard Bench results from the public models endpoint (no API key needed)."""
import json
import urllib.request

URL = "https://llm-gateway.assemblyai.com/v1/models"

with urllib.request.urlopen(URL, timeout=30) as resp:
    models = json.load(resp)["data"]

qwen = next(m for m in models if m["id"] == "qwen3.5-4b-32k-fast")
print(f"{qwen['name']}  provider={qwen['default_provider']['name']}  "
      f"context={qwen['context_length']}  regions={qwen['available_regions']}")
print(f"price per 1M tokens: prompt ${qwen['pricing']['global']['prompt']}, "
      f"completion ${qwen['pricing']['global']['completions']}")
print(f"{'bucket':>7} {'score':>5} {'p50 s':>6} {'p95 s':>6} {'ttft s':>6} {'$/hr':>8}")
for row in qwen["performance"]["data"]:
    print(f"{row['bucket']:>7} {row['quality_score']:>5} {row['latency']['p50']:>6} "
          f"{row['latency']['p95']:>6} {row['ttft']['p50']:>6} {row['cost_per_hour_usd']:>8}")
