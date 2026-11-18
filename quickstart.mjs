import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.LLM_GATEWAY_BASE_URL ?? "https://llm-gateway.assemblyai.com/v1",
  apiKey: process.env.ASSEMBLYAI_API_KEY,
});

const response = await client.chat.completions.create({
  model: "qwen3.5-4b-32k-fast",
  messages: [
    {
      role: "system",
      content:
        "Rewrite raw dictation as clean text. Remove filler words, fix punctuation, " +
        "and keep the speaker's final intent when they correct themselves.",
    },
    {
      role: "user",
      content:
        "um so we got through six of the eight, oh no, five of the eight " +
        "assessments and uh the last three are waiting on security",
    },
  ],
  max_tokens: 300,
  temperature: 0.2,
});

console.log(response.choices[0].message.content);
console.log(response.usage);
