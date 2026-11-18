# Qwen 3.5 4B API quickstart (AssemblyAI LLM Gateway)

Call **Qwen3.5 4B Fast** (`qwen3.5-4b-32k-fast`) through AssemblyAI's OpenAI-compatible [LLM Gateway](https://www.assemblyai.com/products/llm-gateway), then take the same call to production.

Companion code for the blog post [Qwen 3.5 4B API](https://www.assemblyai.com/blog/qwen-4b-llm-gateway).

## What's here

| File | What it does |
| --- | --- |
| `quickstart.py` | First request with the OpenAI Python SDK |
| `quickstart.mjs` | First request with the OpenAI Node SDK |
| `quickstart.sh` | First request with curl |
| `production.py` | Production-shaped rewrite: sized `max_tokens`, a fallback model, retries, `request_id` logging, optional `--stream` |
| `qwen_benchmark.py` | Prints Qwen3.5 4B Fast's Voice Standard Bench rows from the public models endpoint (no key needed) |
| `sample_dictation.txt` | Raw dictation used by `production.py` |

## Setup

1. Sign up at https://www.assemblyai.com/dashboard/signup and copy your API key. The same key works for every LLM Gateway model.
2. `cp .env.example .env` and set `ASSEMBLYAI_API_KEY` (export it in your shell, or load it with your tool of choice).

### Python

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python quickstart.py
python production.py < sample_dictation.txt
python production.py --stream < sample_dictation.txt
python qwen_benchmark.py
```

### Node.js (18+)

```bash
npm install
node quickstart.mjs
```

### curl

```bash
./quickstart.sh
```

## Notes

- Base URL: `https://llm-gateway.assemblyai.com/v1` (US, default) or `https://llm-gateway.eu.assemblyai.com/v1` (EU). Qwen3.5 4B Fast is listed in both regions.
- Supported parameters: `max_tokens`, `temperature`, `stream`. No tool calling or `response_format`; route those steps to another Gateway model.
- Context window: 32,768 tokens; max completion 8,192 tokens.
- `production.py` passes the Gateway's `fallbacks` array through the OpenAI SDK's `extra_body`. The default fallback, `gemini-2.5-flash-lite`, is available in the US and EU.
- Docs: [Quickstart](https://www.assemblyai.com/docs/llm-gateway/quickstart), [Rate limits](https://www.assemblyai.com/docs/llm-gateway/rate-limits), [Fallbacks](https://www.assemblyai.com/docs/llm-gateway/fallback), [Choose a model](https://www.assemblyai.com/docs/llm-gateway/choose-a-model).

## License

MIT
