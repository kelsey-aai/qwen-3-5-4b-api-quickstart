import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("LLM_GATEWAY_BASE_URL", "https://llm-gateway.assemblyai.com/v1"),
    api_key=os.environ["ASSEMBLYAI_API_KEY"],
)

response = client.chat.completions.create(
    model="qwen3.5-4b-32k-fast",
    messages=[
        {
            "role": "system",
            "content": "Rewrite raw dictation as clean text. Remove filler words, "
            "fix punctuation, and keep the speaker's final intent when they correct themselves.",
        },
        {
            "role": "user",
            "content": "um so we got through six of the eight, oh no, five of the eight "
            "assessments and uh the last three are waiting on security",
        },
    ],
    max_tokens=300,
    temperature=0.2,
)

print(response.choices[0].message.content)
print(response.usage)
