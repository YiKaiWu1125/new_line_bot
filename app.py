from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

#*****my ******************
now_time = 0#time.ctime(time.time())
mesg = "null"
state = 0
#***************************

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('uBMwvneIDSUwbILRpCR6HXEEE9OYnLjwFAWKn8oQKJEq21XzkDG1h3r8trcPBb+mINyOkBQWh6TUVh4eLkza+cPIEAsoHFqNYebQzm2L+1yIWcB0BVthoaAJgnKOC1VYwixu/GpktuF1RK9DkujugQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('61f940a9219aca48b8bcafa751c7561e')

@app.route('/')
def hello_world():
    return "Hello, World!"

from flask import jsonify
@app.route('/getjson')
def getjson():
    global mesg
    global now_time
    #print("now time is :")
    #print(now_time)
    #print("\n and message is : ") 
    #print(mesg)
    json = {"time" :now_time , "message" :mesg}
    return jsonify(json)

# 監聽所有來自 /callback 的 Post Request
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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    #if '最新合作廠商' in msg:
    #    message = imagemap_message()
    #    line_bot_api.reply_message(event.reply_token, message)
    #elif '最新活動訊息' in msg:
    #    message = buttons_message()
    #    line_bot_api.reply_message(event.reply_token, message)
    #elif '註冊會員' in msg:
    #    message = Confirm_Template()
    #    line_bot_api.reply_message(event.reply_token, message)
    #elif '旋轉木馬' in msg:
    #    message = Carousel_Template()
    #    line_bot_api.reply_message(event.reply_token, message)
    #elif '圖片畫廊' in msg:
    #    message = test()
    #    line_bot_api.reply_message(event.reply_token, message)
    #elif '功能列表' in msg:
    #    message = function_list()
    #    line_bot_api.reply_message(event.reply_token, message)
    #else:
    #    message = TextSendMessage(text=msg)
    #    line_bot_api.reply_message(event.reply_token, message)
    global state
    if state == 1:
        state = 0
        it = "您要記帳的項目:" + msg +"\n請輸入花費金額\nEX(888))"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=it))
    elif '伙食' in msg:
        state = 1
        it = "您要記帳的類別:" + msg +"\n請輸入時間與花費項目\nEX(2022.03.33 晚餐)"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=it))
    elif '零食' in msg:
        state = 1
        it = "您要記帳的類別:" + msg +"\n請輸入時間與花費項目\nEX(2022.03.33 晚餐)"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=it))
    
    elif '飲料' in msg:
        state = 1
        it = "您要記帳的類別:" + msg +"\n請輸入時間與花費項目\nEX(2022.03.33 晚餐)"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=it))
    elif '其他花費' in msg:
        state = 1
        it = "您要記帳的類別:" + msg +"\n請輸入時間與花費項目\nEX(2022.03.33 晚餐)"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=it))
    else:
        it = "已收到:" + msg +"\n請輸入要記帳的類別\n伙食、零食、飲料、其他花費"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=it))
    global mesg
    global now_time
    mesg = msg
    now_time = time.ctime(time.time())

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
