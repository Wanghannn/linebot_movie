import requests
from bs4 import BeautifulSoup

#========本週新片======== https://movies.yahoo.com.tw/movie_thisweek.html

def crawler(newmovie_list, page):
  newmovie_re=requests.get('https://movies.yahoo.com.tw/movie_thisweek.html?page=' + str(page))
  newmovie_soup = BeautifulSoup(newmovie_re.text, 'html.parser')
  newmovie_spans = newmovie_soup.find_all('div', class_='release_info_text')
  for i in newmovie_spans:
    newmovie = i.find('div', 'release_movie_name').a.text.strip()
    newmovie_list.append(newmovie)
  if len(newmovie_soup.find_all('li', class_='nexttxt disabled')) == 0:
    page += 1
    crawler(newmovie_list, page)
  else:
    newmovie_dict = dict(zip(list(range(1, 50)), newmovie_list))
    return newmovie_dict

def grt_newmovie():
    msg = '以下是本週新片：\n（可直接輸入[電影ID]查詢場次）'
    #爬蟲爬出來
    # list_newmovie = {'id:1':'奇異博士', 'id:2':'媽的多重宇宙', 'id:3':'...'}
    newmovie_list = []
    list_newmovie = crawler(newmovie_list, 1)
    list_item = list_newmovie.items()
    for id, name in list_item:
        msg += ("\n[%s] %s" % (id, name)) 
    return msg
#=======================


#========排行榜========== https://movies.yahoo.com.tw/chart.html
def grt_rankmovie():
    msg = '以下是今日排行榜：\n（可直接輸入[電影ID]查詢場次）'
    #爬蟲爬出來
    # list_rankmovie = {'id:1':'奇異博士', 'id:2':'媽的多重宇宙', 'id:3':'...'}
    rank_list = []
    re = requests.get('https://movies.yahoo.com.tw/chart.html')
    soup = BeautifulSoup(re.text, 'html.parser')
    spans = soup.find_all('div', class_='rank_list table rankstyle1')
    for i in spans:
        rank_first = i.find('h2')
        rank_others = i.find_all(class_='rank_txt')
    rank_list.append(rank_first.text.strip())
    rank_list += list(map(lambda rank_others: rank_others.text.strip(), rank_others))
    rank_dict = dict(zip(list(range(1, 21)), rank_list))
    
    list_item = rank_dict.items()
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

