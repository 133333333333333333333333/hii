from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})   # 允许所有域名跨域


client = OpenAI(api_key="sk-d5b0afe06e8b4cc8afe47fbb2fa0adee", base_url="https://api.deepseek.com")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"reply": response.choices[0].message.content})

# 输出格式 带有data: 前缀
@app.route('/chat-stream', methods=['POST'])
def chat_stream():
    data = request.get_json()
    prompt = data.get('prompt', '')
    def generate():
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"
    return Response(generate(), mimetype="text/event-stream;; charset=utf-8")

# @app.route('/chat-stream', methods=['POST'])
# def chat_stream():
#     data = request.get_json()
#     prompt = data.get('prompt', '')

#     def generate():
#         stream = client.chat.completions.create(
#             model="deepseek-chat",
#             messages=[{"role": "user", "content": prompt}],
#             stream=True
#         )
#         for chunk in stream:
#             if chunk.choices[0].delta.content:
#                 # 直接输出文本内容，不加任何前缀和后缀
#                 yield chunk.choices[0].delta.content

#     # 使用 stream_with_context 保证流式传输，设置正确的 Content-Type
#     return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(port=5001)