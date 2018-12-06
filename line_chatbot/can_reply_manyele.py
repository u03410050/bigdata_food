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
    image_url_1 = "https://i.imgur.com/eTldj2E.png?1"
    image_url_2 = "https://i.imgur.com/mB9yDO0.png"
    click_link_1 = "https://www.facebook.com/ntustcc"
    click_link_2 = "https://www.facebook.com/ntustcc"
    carousel_template = template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=image_url_1,
                    title='template-1',
                    text='text-1',
                    actions=[
                        PostbackTemplateAction(
                            label='postback-1',
                            text='postback text1',
                            data='result=1'
                        ),
                        MessageTemplateAction(
                            label='message-1',
                            text='message text1'
                        ),
                        URITemplateAction(
                            label='uri-1',
                            uri=click_link_1
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=image_url_2,
                    title='template-2',
                    text='text-2',
                    actions=[
                        PostbackTemplateAction(
                            label='postback-2',
                            text='postback text2',
                            data='result=2'
                        ),
                        MessageTemplateAction(
                            label='message-2',
                            text='message text2'
                        ),
                        URITemplateAction(
                            label='link-2',
                            uri=click_link_2
                        )
                    ]
                )]
            )
   # print("event =", event)
    print("event =", event)
#     alt_text 因template只能夠在手機上顯示，因此在PC版會使用alt_Text替代
    line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text="Carousel Template Example", template=carousel_template))


if __name__ == "__main__":
    app.run(port="6655")