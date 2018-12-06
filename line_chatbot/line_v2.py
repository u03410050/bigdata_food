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
    ipeen_url="http://www.ipeen.com.tw/tainan/channel/F"
    
    for tmp in online_users:
        if(cnt>4):
            break
        if(tmp['nckuee_nearby_walk']==1):
            feed_back.append(tmp)
            cnt=cnt+1
    
    
    image_url = []
    click_link= []
    shop_name=[]
    shop_site=[]
    
    for item in feed_back:
        image_url.append(item['image'])
 
        try:
            click_link.append(item['網址'])
        
        except:
            click_link.append(ipeen_url)
            
        shop_name.append(item['商家名稱'])
        try:
            shop_site.append(item['地址'])
        
        except:
            shop_site.append("無")
        

    
    for i in image_url:
        print(i)
 
    
    carousel_template = template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=str(image_url[0]),
                    title=shop_name[0],
                    text=shop_site[0],
                    actions=[
                        PostbackTemplateAction(
                            label='喜歡',
                            text='喜歡',
                            data='result=1'
                        ),
                        MessageTemplateAction(
                            label='不喜歡',
                            text='不喜歡'
                        ),
                        URITemplateAction(
                            label='此店的愛評網連結',
                            uri=str(click_link[0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=str(image_url[1]),
                    title=shop_name[1],
                    text=shop_site[1],
                    actions=[
                        PostbackTemplateAction(
                            label='喜歡',
                            text='喜歡',
                            data='result=1'
                        ),
                        MessageTemplateAction(
                            label='不喜歡',
                            text='不喜歡'
                        ),
                        URITemplateAction(
                            label='此店的愛評網連結',
                            uri=str(click_link[1])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=str(image_url[2]),
                    title=shop_name[2],
                    text=shop_site[2],
                    actions=[
                        PostbackTemplateAction(
                            label='喜歡',
                            text='喜歡',
                            data='result=1'
                        ),
                        MessageTemplateAction(
                            label='不喜歡',
                            text='不喜歡'
                        ),
                        URITemplateAction(
                            label='此店的愛評網連結',
                            uri=str(click_link[2])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=str(image_url[3]),
                    title=shop_name[3],
                    text=shop_site[3],
                    actions=[
                        PostbackTemplateAction(
                            label='喜歡',
                            text='喜歡',
                            data='result=1'
                        ),
                        MessageTemplateAction(
                            label='不喜歡',
                            text='不喜歡'
                        ),
                        URITemplateAction(
                            label='此店的愛評網連結',
                            uri=str(click_link[3])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=str(image_url[4]),
                    title=shop_name[4],
                    text=shop_site[4],
                    actions=[
                        PostbackTemplateAction(
                            label='喜歡',
                            text='喜歡',
                            data='result=1'
                        ),
                        MessageTemplateAction(
                            label='不喜歡',
                            text='不喜歡'
                        ),
                        URITemplateAction(
                            label='此店的愛評網連結',
                            uri=str(click_link[4])
                        )
                    ]
                )]
            )
    print("event =", event)
    
#     alt_text 因template只能夠在手機上顯示，因此在PC版會使用alt_Text替代
    line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text="Carousel Template Example", template=carousel_template))


if __name__ == "__main__":
    app.run(port="6655")