#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# 基本定義
choose_msg = ['我要看本週新片', '我要看排行榜', '有哪些影廳可以選？', '有什麼電影可以看呢？']
emoji_list = [
    {
        "index": 0,
        "productId": "5ac1bfd5040ab15980c9b435",
        "emojiId": "001"
    },
    {
        "index": 13,
        "productId": "5ac1bfd5040ab15980c9b435",
        "emojiId": "002"
    }
]

#======回傳給主程式======

def choose():
    return choose_msg

def emoji():
    return emoji_list

#======回傳給主程式======



#======我們自己的Function==========

# 輸入 “電影”
def choose_template():
    message = TemplateSendMessage(
        alt_text='第一步驟！！',
        template=ButtonsTemplate(
            thumbnail_image_url="https://s.yimg.com/ny/api/res/1.2/gYptwTe_GuD1aZN_DmlCTw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTY0NztjZj13ZWJw/https://s.yimg.com/uu/api/res/1.2/0QivNJNruxR08UT8.qIfVw--~B/aD02MTk7dz05MTg7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/ko/cts.com.tw/a9ff7f108a81a2b8192980951465d87d",
            title="今天想查詢什麼？",
            text="選擇今天要查詢的項目",
            actions=[
                MessageTemplateAction(
                    label="1. 查詢本週新片",
                    text=choose_msg[0]
                ),
                MessageTemplateAction(
                    label="2. 查詢排行榜",
                    text=choose_msg[1]
                ),
                MessageTemplateAction(
                    label="3. 我要選影廳",
                    text=choose_msg[2]
                ),
                MessageTemplateAction(
                    label="4. 我要看電影",
                    text=choose_msg[3]
                )
            ]
        )
    )
    return message

# 選擇查詢
def choose_funtion(msg):
    message = ""
    if msg == choose_msg[0]:
        message = "提供新片列表"
    elif msg == choose_msg[1]:
        message = "提供排名列表"
    elif msg == choose_msg[2]:
        message = "提供當天可看電影及時間"
    elif msg == choose_msg[3]:
        message = "提供當天播映影廳及時間"
    else:
        message = "出錯了QQ"
    return message

#======我們自己的程式==========