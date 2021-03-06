from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from bot_template import *
from bigdata import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('Filled your channel access token')
# Channel Secret
handler = WebhookHandler('Filled your channel secret')

# 自訂參數
movie = ""
city = ""
date = ""
cinema = ""
list_date = []
list_city = []
list_cinema = []

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
    global movie, city, date, cinema, list_city, list_date, list_cinema
    msg = event.message.text
    # if 'imagemap_message' in msg:
    #     message = imagemap_message()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif 'buttons_message' in msg:
    #     message = buttons_message()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif 'Confirm_Template' in msg:
    #     message = Confirm_Template()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif 'Carousel_Template' in msg:
    #     message = Carousel_Template()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif 'picture' in msg:
    #     message = picture()
    #     line_bot_api.reply_message(event.reply_token, message)

    # 我們自己的功能
    if '電影' == msg:
        # 重置查詢參數
        movie = ""
        city = ""
        date = ""
        cinema = ""
        message = choose_template()
        line_bot_api.reply_message(event.reply_token, message)
    elif msg in choose():
        message_sent = choose_funtion(msg)
        message = TextSendMessage(text=message_sent)
        line_bot_api.reply_message(event.reply_token, message)
    # 輸入 Movie
    elif msg in getAllMovie(): # 4-1 比對使用者是否輸入正確“電影” -> 回傳全部地區（爬蟲有問題無法針對電影篩選）
        movie = msg
        if movie != "" and city != "" and date != "":
            message_sent = get_cinema_time(movie, city, date)
        else:
            message_sent, list_city = get_city_msg()
        message = TextSendMessage(text=message_sent)
        line_bot_api.reply_message(event.reply_token, message)
    # 輸入 City
    elif msg in getAllCity(): 
        city = msg
        # 四種情況
        # 3-1-1 比對使用者是否輸入正確“地區” -> 回傳可選擇的影廳
        if movie == "" and date == "" and cinema == "":
            message_sent, list_cinema = get_cinema(city)
        # 3-1-2 直接查詢get_movie_time
        elif movie == "" and date == "" and cinema != "":
            message_sent = get_movie_time(city, cinema)
        # 4-2-1 比對使用者是否輸入正確“地區” -> 回傳可看日期
        elif movie != "" and date == "" and cinema == "":
            message_sent, list_date = get_date(movie)
        # 4-2-2 直接查詢get_cinema_time
        elif movie != "" and date != "" and cinema == "":
            message_sent = get_cinema_time(movie, city, date)
        else:
            message_sent = "邏輯錯了QQ"
        message = TextSendMessage(text=message_sent)
        line_bot_api.reply_message(event.reply_token, message)
    # 輸入 cinema
    elif msg in list_cinema:# 3-2 比對使用者是否輸入正確“日期” -> 回傳個影廳播映時間
        cinema = msg
        message_sent = get_movie_time(city, cinema)
        message = TextSendMessage(text=message_sent)
        line_bot_api.reply_message(event.reply_token, message)
    # 輸入 Date
    elif msg in list_date: # 4-3 比對使用者是否輸入正確“日期” -> 回傳個影廳播映時間
        date = msg
        message_sent = get_cinema_time(movie, city, date)
        message = TextSendMessage(text=message_sent)
        line_bot_api.reply_message(event.reply_token, message)
    elif 'emoji_test' == msg:
        message = TextSendMessage(text='$ LINE emoji $', emojis=emoji())
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text='對不起，我聽不懂您的意思\n麻煩您傳送完整內容！')
        line_bot_api.reply_message(event.reply_token, message)

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
