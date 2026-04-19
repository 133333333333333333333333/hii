import requests

# 示例：用免费天气API（不需要key）
url = "https://api.open-meteo.com/v1/forecast?latitude=31.23&longitude=121.47&current_weather=true"
resp = requests.get(url)
data = resp.json()
print(data["current_weather"]["temperature"])