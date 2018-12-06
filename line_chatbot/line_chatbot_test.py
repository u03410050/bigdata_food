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

line_bot_api = LineBotApi('fOlK9YHAIOLtWUjBi6us9g6S/Ol2rO3jeVA+efQW6GlPLrtqKnOKzdPUsimgpBYURzWK0ywASA4SLzzFlhWNEMjc++GVnafZED7bLoYVEx1kpLzC1QToiQkM3gcaKNdHEPCjXUzzTbhHpXD0ZKAn2gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cde4c774cd125085e3e3a5559304736e')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(port="6655")