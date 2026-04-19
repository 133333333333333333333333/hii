from openai import OpenAI

client = OpenAI(
    api_key="sk-d5b0afe06e8b4cc8afe47fbb2fa0adee",
    base_url="https://api.deepseek.com"   # DeepSeek地址
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "什么是RAG？"}],
    stream=False
)
print(response.choices[0].message.content)