# Railway DeepSeek Demo App

一个集成 DeepSeek AI 的 Flask 应用，用于测试 Railway 部署。

## 本地运行

1. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

2. 设置环境变量：

   ```bash
   export OPENAI_API_KEY="your_deepseek_api_key"
   export BASE_URL="https://api.deepseek.com"  # 可选，默认值
   ```

3. 运行应用：

   ```bash
   python app.py
   ```

4. 访问 http://localhost:5001

## 部署到 Railway

1. 注册并登录 [Railway.app](https://railway.app)

2. 创建新项目，从 GitHub 导入此仓库

3. Railway 会自动检测 Python 项目并安装依赖

4. 在 Railway 项目设置中添加环境变量：
   - `OPENAI_API_KEY`: 你的 DeepSeek API Key
   - `BASE_URL`: `https://api.deepseek.com` (可选)

5. 部署完成，获得域名如 https://your-app.up.railway.app

## API 端点

- `GET /` - 主页
- `GET /api/test` - 测试 API
- `POST /api/echo` - 回显消息，body: `{"message": "hello"}`
- `POST /api/chat` - 与 DeepSeek 聊天，body: `{"message": "你好"}`
- `POST /api/chat-stream` - 流式聊天，body: `{"message": "讲个故事"}`
