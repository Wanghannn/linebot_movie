import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

#========本週新片======== https://movies.yahoo.com.tw/movie_thisweek.html
def newmovie_crawler(newmovie_list, page):
    global newmovie_dict
    newmovie_re=requests.get('https://movies.yahoo.com.tw/movie_thisweek.html?page=' + str(page))
    newmovie_soup = BeautifulSoup(newmovie_re.text, 'html.parser')
    newmovie_spans = newmovie_soup.find_all('div', class_='release_info_text')
    for i in newmovie_spans:
        newmovie = i.find('div', 'release_movie_name').a.text.strip()
        newmovie_list.append(newmovie)
    if len(newmovie_soup.find_all('li', class_='nexttxt disabled')) == 0:
        page += 1
        newmovie_crawler(newmovie_list, page)
    else:
        newmovie_dict = dict(zip(list(range(1, 21)), newmovie_list))

def get_newmovie():
    msg = '以下是本週新片：\n（可直接輸入[電影ID]查詢場次）'
    #爬蟲爬出來
    # list_newmovie = {'id:1':'奇異博士', 'id:2':'媽的多重宇宙', 'id:3':'...'}
    newmovie_list = []
    newmovie_crawler(newmovie_list, 1)
    list_item = newmovie_dict.items()
    for id, name in list_item:
        msg += ("\n[%s] %s" % (id, name)) 
    return msg
#=======================


#========排行榜========== https://movies.yahoo.com.tw/chart.html
def get_rankmovie():
    msg = '以下是今日排行榜：\n（可直接輸入[電影ID]查詢場次）'
    #爬蟲爬出來
    # list_rankmovie = {'id:1':'奇異博士', 'id:2':'媽的多重宇宙', 'id:3':'...'}
    rank_list = []
    rank_re = requests.get('https://movies.yahoo.com.tw/chart.html')
    rank_soup = BeautifulSoup(rank_re.text, 'html.parser')
    rank_spans = rank_soup.find_all('div', class_='rank_list table rankstyle1')
    for i in rank_spans:
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
def get_allmovie():
    global all_movie_id
    all_movie_id = all_movie()
    msg = '請輸入想看的[電影全名]\n===================='
    #爬蟲爬出來
    #list_allmovie = {'id:1':'奇異博士', 'id:2':'媽的多重宇宙', 'id:3':'...'}
    list_item = all_movie_id.items()
    for name, id in list_item:
        msg += ("\n%s" % (name)) 
    return msg
#=======================


#========查詢3、4相關Function========

# 基本參數
movies_id = {}
all_movie_id = {}
cinema_id = defaultdict(dict)
places_id = {}
num = {
    '一月': 1,
    '二月': 2,
    '三月': 3,
    '四月': 4,
    '五月': 5,
    '六月': 6,
    '七月': 7,
    '八月': 8,
    '九月': 9,
    '十月': 10,
    '十一月': 11,
    '十二月': 12
}

# 取得所有Movie dict(參數：all_movie_id)
def all_movie():
    url = 'https://movies.yahoo.com.tw/ajax/in_theater_movies'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    json_data = resp.json()
    for number, movie in json_data.items():
        all_movie_id[movie] = number
    return all_movie_id

#  取得電影播放“地區”列表
def get_city(movie):
    """
    # choose movie -> choose city -> choose date -> output: theater and time
    """
    if movie == "":
        return "get_city() Error"
    # choose city
    # headers
    headers = {
        'authority': 'movies.yahoo.com.tw',
        'method': 'GET',
        'path': '/api/v1/areas_by_movie_theater?movie_id=' + all_movie_id[movie],
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': 'BX=fjkbgg9fb0c1k&b=3&s=ge; rxx=2iwvattyf9w.1x0bsdn3&v=1; A1=d=AQABBDQwsF4CEHDjEfJP3ksyjgDNeYJw0fkFEgEBAQEQwV6eX2BYb2UB_SMAAAcINDCwXoJw0fk&S=AQAAAg7KPjSv_-09B72obpPLkRw; A3=d=AQABBDQwsF4CEHDjEfJP3ksyjgDNeYJw0fkFEgEBAQEQwV6eX2BYb2UB_SMAAAcINDCwXoJw0fk&S=AQAAAg7KPjSv_-09B72obpPLkRw; GUC=AQEBAQFewRBfnkIiCgSc; A1S=d=AQABBDQwsF4CEHDjEfJP3ksyjgDNeYJw0fkFEgEBAQEQwV6eX2BYb2UB_SMAAAcINDCwXoJw0fk&S=AQAAAg7KPjSv_-09B72obpPLkRw&j=WORLD; yvapF=%7B%22vl%22%3A1%2C%22rvl%22%3A1%7D; avi=eyJpdiI6IjJ0S2U1NGNLRWthbDVuXC9scmFDV013PT0iLCJ2YWx1ZSI6IklDN0lLK01mR0JNVXNnZFFZRnRaTUE9PSIsIm1hYyI6IjVjOTBmMzI2YmNkMTMyMWU1NzFkZjA2OWZiOTMxY2U3ZmMwZDNjNmI0ZmI4OGJjZTNlM2ZlOGMyZTJiNDM4NTkifQ%3D%3D; browsed_movie=eyJpdiI6InlpR09JckVmTEZLZUh6amdYbVRNTVE9PSIsInZhbHVlIjoiXC9FSGRqUVhRY1FKY3puSTVCTXJhTFRDTG1iMGFHVVdUWVR4XC9ESHF0K1RlbnhrWVpyNTFkSDJScW5FamV5MmhaWEp2ZmJ2V3B3Skhka2owWWl6MGRaY1c0UHpJXC8zeXdXSUU1UjM1VnRSS3JTVnN2eStlM0ZHV0dWQnhjeTBrVVUiLCJtYWMiOiJlNmQ2NWY2Y2NjZWQ4YzMxZGYxZWI0MTI5ZTNiMGVmY2E5NWIwOTgyYmZlNDEzY2NmODVkZGU0MTlmY2Y0NmZkIn0%3D; cmp=t=1594541794&j=0',
        'dnt': '1',
        'mv-authorization': '21835b082e15b91a69b3851eec7b31b82ce82afb',
        'referer': 'https://movies.yahoo.com.tw/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56',
    }
    url = 'https://movies.yahoo.com.tw/api/v1/areas_by_movie_theater'
    payload = {'movie_id': all_movie_id[movie]}
    resp = requests.get(url, params=payload, headers=headers)
    msg = '請輸入想看電影的[地區]\n===================='
    for cities in resp.json():
        msg += ("\n%s" % (cities['title']))  
    return msg   

# 取得電影可看“日期”列表
def get_date(movie):
    url = 'https://movies.yahoo.com.tw/movietime_result.html'
    payload = {'movie_id': all_movie_id[movie]}
    resp = requests.get(url, params=payload)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    movie_date = soup.find_all("label", attrs={'for': re.compile("date_[\d]")})   # get the date of today
    list_date = []
    msg = "請輸入想看電影的[日期]\n===================="
    for date in movie_date:
        msg += "\n{} {}".format(date.p.string, date.h3.string)
        list_date.append("{} {}".format(date.p.string, date.h3.string))
    # search_date = input('choose a date you would like to search').split()
    # date = '2022-{}-{}'.format(str('%02d' % num[search_date[0]]), search_date[1])
    return msg, list_date
#==================================