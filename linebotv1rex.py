from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('qYZMCa45V0aFy2+LKFvGGu3ar7BaaIy3P2D9YSKjLL4Wj+Oj9WdAt11Gl0HLGFxPSgb9YyzGlrIU6TkYcv/jcUwC8XbH8OGotu9vz+5tyv/yssetoPWMLuMc4PwIBvoUaC1paXTBzn8Ap/Q/LNTrTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('33abfca3af6493bf5d9c4b2649c90c83')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()