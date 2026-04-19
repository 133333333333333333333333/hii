from openai import OpenAI

client = OpenAI(
    api_key="sk-d5b0afe06e8b4cc8afe47fbb2fa0adee",
    base_url="https://api.deepseek.com"   # DeepSeek地址
)
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "什么是RAG？"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
