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
from flask import jsonify
import json, requests
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
    global mesg
    global now_time
    mesg = msg
    now_time = time.ctime(time.time())
    try:
        url = requests.get("http://218.161.40.232:8081/line_bot_return")
        text =  url.text
        data = json.loads(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="伺服器連線中斷中\n請重新啟動伺服器後再重新嘗試"))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=data['message']))
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="伺服器連線中斷中\n請重新啟動伺服器後再重新嘗試"))
    
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
