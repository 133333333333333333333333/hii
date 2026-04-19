from flask import Flask, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import json
import os

app = Flask(__name__, static_folder='.')
CORS(app)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_BASE_URL = os.environ.get('BASE_URL', 'https://api.deepseek.com')

if not OPENAI_API_KEY:
    raise RuntimeError('Missing required environment variable: OPENAI_API_KEY')

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

@app.route('/')
@app.route('/index.html')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({"message": "API is working!", "status": "success"})

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    if data and 'message' in data:
        return jsonify({"echo": data['message']})
    return jsonify({"error": "No message provided"}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=1000,
            temperature=0.7
        )
        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat-stream', methods=['POST'])
def chat_stream():
    data = request.get_json()
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    def generate():
        try:
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": user_input}],
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)