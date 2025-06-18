from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import os

app = Flask(__name__)

# 用環境變數讀取你的憑證（這一步我們還沒設定，先放空值不影響測試）
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "dummy"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET", "dummy"))

@app.route("/callback", methods=['POST'])
def callback():
    print("📩 收到 LINE webhook 進來了")
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    print("📩 收到 LINE 傳來的內容：")
    print(body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 驗證失敗（這是預期的，因為我們還沒設定憑證）")
        abort(400)

    return 'OK'

@app.route("/")
def index():
    return "LINE Bot Webhook 測試中"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
