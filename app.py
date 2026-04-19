from flask import Flask, Response, request, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import json
import os

app = Flask(__name__, static_folder='.')
CORS(app)

client = OpenAI(
    api_key="sk-d5b0afe06e8b4cc8afe47fbb2fa0adee",
    base_url="https://api.deepseek.com"
)

# 提供静态 HTML 页面
@app.route('/')
@app.route('/index.html')
def index():
    return send_from_directory('.', 'index.html')

# 流式 API（供前端 JavaScript 调用）
@app.route('/chat-stream', methods=['POST'])
def chat_stream():
    data = request.get_json()
    user_input = data.get('message', '')
    
    def generate():
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": user_input}],
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
        yield "data: [DONE]\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)