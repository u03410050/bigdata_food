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


from pymongo import MongoClient



app = Flask(__name__)

line_bot_api = LineBotApi('vYqkNAx87hxapaG+dipYm6huf9v4HCJt/ffKiutFeeKwZCjzO2PVzfLuwSDc80T+RzWK0ywASA4SLzzFlhWNEMjc++GVnafZED7bLoYVEx065nXYrJijr5oMs9kD68mS5osFo/zdRAFFCRa6plvgZQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cde4c774cd125085e3e3a5559304736e')



connect= MongoClient("mongodb://tea:tea@localhost:27017/bigdata_beta")
db=connect['bigdata_beta']


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
    print("event =", event)
    
   
    online_users=db.test.find({"商家分類": "麵食點心"})
    
    feed_back=[]
    cnt=0
    
    no_photo_url="https://a.rimg.com.tw/s2/2/78/d4/21722409789652_704_m.jpg"
    ncku_ee_url="https://www.ee.ncku.edu.tw/index.html"
    
    for tmp in online_users:
        if(cnt>4):
            break
        feed_back.append(tmp)
        cnt=cnt+1
    
    
    image_url = []
    click_link= []
    
    for item in feed_back:
        if(item['image']!=None):
            image_url.append(item['image'])
        else:
            image_url.append(no_photo_url)
        
        try:
            click_link.append(item['網址'])
        
        except:
            click_link.append(ncku_ee_url)
        

    for i in image_url:
        print(i)
    for j in click_link:
        print(j)
        
        
 
    
    carousel_template = template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=str(image_url[0]),
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
                            uri=str(click_link[0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=str(image_url[1]),
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
                            uri=str(click_link[1])
                        )
                    ]
                )]
            )
    print("event =", event)
    
#     alt_text 因template只能夠在手機上顯示，因此在PC版會使用alt_Text替代
    line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text="Carousel Template Example", template=carousel_template))


if __name__ == "__main__":
    app.run(port="6655")