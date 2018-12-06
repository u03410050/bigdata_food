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

from linebot.models import TemplateSendMessage, CarouselTemplate, CarouselColumn, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction

from linebot.exceptions import LineBotApiError
app = Flask(__name__)

line_bot_api = LineBotApi('fOlK9YHAIOLtWUjBi6us9g6S/Ol2rO3jeVA+efQW6GlPLrtqKnOKzdPUsimgpBYURzWK0ywASA4SLzzFlhWNEMjc++GVnafZED7bLoYVEx1kpLzC1QToiQkM3gcaKNdHEPCjXUzzTbhHpXD0ZKAn2gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cde4c774cd125085e3e3a5559304736e')

to="U18a62884b1484c6697dae15ec5cb0435"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    try:
        line_bot_api.push_message("U18a62884b1484c6697dae15ec5cb0435", TextSendMessage(text='台科大電腦研習社'))
    except LineBotApiError as e:
    # error handle
        raise e

#圖片訊息
# ImageSendMessage物件中的輸入
# original_content_url 以及 preview_image_url都要寫才不會報錯。
#輸入的網址要是一個圖片，應該說只能是一個圖片，不然不會報錯但是傳過去是灰色不能用的圖
    
    image_url = "https://i.imgur.com/eTldj2E.png?1"
    try:
        line_bot_api.push_message("U18a62884b1484c6697dae15ec5cb0435", ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
    except LineBotApiError as e:
    # error handle
        raise e

    return 'OK'


#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
   


if __name__ == "__main__":
    app.run(port="6655")