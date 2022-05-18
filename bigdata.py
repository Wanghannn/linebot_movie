# 我們自己的程式
def choose_funtion():
    message = TemplateSendMessage(
        alt_text='第一步驟！！！',
        template=ButtonsTemplate(
            thumbnail_image_url="https://pic2.zhimg.com/v2-de4b8114e8408d5265503c8b41f59f85_b.jpg",
            title="今天想查詢什麼？",
            text="選擇今天要查詢的項目",
            actions=[
                MessageTemplateAction(
                    label="1. 查詢本週新片",
                    text="我要看本週新片"
                ),
                MessageTemplateAction(
                    label="2. 查詢排行榜",
                    text="我要看排行榜"
                ),
                MessageTemplateAction(
                    label="3. 我要選影廳",
                    text="有哪些影廳可以選？"
                ),
                MessageTemplateAction(
                    label="4. 我要看電影",
                    text="有什麼電影可以看呢？"
                )
            ]
        )
    )
    return message