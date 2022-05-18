
#========本週新片======== https://movies.yahoo.com.tw/movie_thisweek.html
def grt_newmovie():
    msg = '以下是本週新片：\n（可直接輸入[電影ID]查詢場次）'
    #爬蟲爬出來
    list_newmovie = {'id:1':'奇異博士', 'id:2':'媽的多重宇宙', 'id:3':'...'}
    
    list_item = list_newmovie.items()
    for id, name in list_item:
        msg += ("\n[%s] %s" % (id, name)) 
    return msg
#=======================


#========排行榜========== https://movies.yahoo.com.tw/chart.html
def grt_rankmovie():
    msg = '以下是今日排行榜：\n（可直接輸入[電影ID]查詢場次）'
    #爬蟲爬出來
    list_rankmovie = {'id:1':'奇異博士', 'id:2':'媽的多重宇宙', 'id:3':'...'}
    
    list_item = list_rankmovie.items()
    for id, name in list_item:
        msg += ("\n[%s] %s" % (id, name)) 
    return msg
#=======================


#========影廳列表========
def get_theater():
    msg = '請輸入想去的[影廳ID]：'
    #爬蟲爬出來
    dict_theater = {'id:1':'國賓影城(台北長春廣場)', 'id:2':'欣欣秀泰影城', 'id:3':'...'}
    
    list_item = dict_theater.items()
    for id, name in list_item:
        msg += ("\n[%s] %s" % (id, name)) 
    return msg
#=======================


#========電影列表========
def grt_allmovie():
    msg = '請輸入想看的[電影ID]'
    #爬蟲爬出來
    list_allmovie = {'id:1':'奇異博士', 'id:2':'媽的多重宇宙', 'id:3':'...'}
    
    list_item = list_allmovie.items()
    for id, name in list_item:
        msg += ("\n[%s] %s" % (id, name)) 
    return msg
#=======================

