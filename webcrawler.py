import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
from fake_useragent import UserAgent

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
def get_city():
    global places_id, cinema_id
    places_id, cinema_id = places()
    list_city = list(places_id.keys())
    msg = '請輸入想去的影廳所在[地區]\n====================：'
    list_item = places_id.items()
    for name, id in list_item:
        msg += ("\n%s" % (name)) 
    return msg, list_city

def get_cinema(city):
    msg = "請輸入想查詢的[影廳]\n===================="
    for cinema in cinema_id[city].keys():
        msg += "\n" + cinema
    return msg

# 輸入（地區、影廳），回傳（該影廳當日播映電影＆播映時間）
def get_movie_time(city, cinema):
    """
    choose city -> choose theater -> output: all the movie shown in cinemas
    lst: movie time, lst=[(movie,[time]), ]
    """
    lst = []
    soup = read_url('https://movies.yahoo.com.tw/theater_result.html/id='+cinema_id[city][cinema])
    movies = soup.find_all('div', class_='release_info_text')
    if movies:
        for movie in movies:
            name = movie.find('div', class_='theaterlist_name').a.text
            time = []
            for i in movie.select('.theater_time > li'):
                time.append(i.text)
            lst.append((name, time))

        # print the movie and its play time
        msg = "{}\t{}\n".format(city, cinema)
        msg += "====================" 
        for i in lst:
            msg += "\n" + (i[0])     # movie
            for j in i[1]:           # time
                j = j.replace("\n", "")
                j = j.replace(" ", "")
                msg += "\n" + (j)
            msg += "\n===================="
    else:
        msg = ("抱歉！\n{}-{} 今日沒有播映電影\n請選擇其他[地區]或[影城]".format(city, cinema))
        msg += "\n===================="
        
    return msg + "\n重置查詢請輸入:電影"
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

def get_city_msg():
    global places_id, cinema_id
    places_id, cinema_id = places()
    list_city = list(places_id.keys())
    msg = '請輸入想看電影的[地區]\n注意！該地區不一定有播你想看的電影\n===================='
    list_item = places_id.items()
    for name, id in list_item:
        msg += ("\n%s" % (name)) 
    return msg, list_city

# 輸入（電影、地區、時間），回傳（該地區影廳＆播映時間）
def get_cinema_time(movie, city, search_date):
    url = "https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie"
    search_date = search_date.split()
    date = '2022-{}-{}'.format(str('%02d' % num[search_date[0]]), search_date[1])
    payload = {'movie_id': all_movie_id[movie],
               'date': date,
               'area_id': places_id[city],
               'theater_id': '',
               'datetime': '',
               'movie_type_id': ''}
    resp = requests.get(url, params=payload)
    json_data = resp.json()
    soup = BeautifulSoup(json_data['view'], 'lxml')
    html_elem = soup.find_all("ul", attrs={'data-theater_name': re.compile(".*")})
    msg = "{}\t{}\n{}\n".format(date, city, movie)
    msg += "===================="
    if html_elem:
        for the in html_elem:
            theater = the.find("li", attrs={"class": "adds"})
            msg += ("\n電影院： {}".format(theater.find("a").text))
            # info裡面分別包含每一間戲院的場次資訊
            info = the.find_all(class_="gabtn")
            for i in info:
                msg += "\n" + (i["data-movie_time"])
            msg += "\n===================="
    else:
        msg = ("抱歉！\n{}\n {}\n目前沒有在{}的影廳播映資訊\n請選擇其他[地區]、[時間]或[電影]".format(date, movie, city))
        msg += "\n===================="
        
    return msg + "\n重置查詢請輸入:電影"
#=======================


#========查詢3、4相關Function========

# 基本參數
movies_id = {}
all_movie_id = {}
places_id = {}
cinema_id = defaultdict(dict)
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

# 讀取url
def read_url(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, parser='html.parser', features='lxml')
    return soup

# 取得所有Movie dict(參數：all_movie_id)
def all_movie():
    url = 'https://movies.yahoo.com.tw/ajax/in_theater_movies'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    json_data = resp.json()
    for number, movie in json_data.items():
        all_movie_id[movie] = number
    return all_movie_id

#  取得所有“地區”＆“對應影廳” dict (參數：places_id, cinema_id)
def places():
    """
    cinema id and city id
    place_id = {city:id}
    cinema_id = {city : {theater : id} }
    """
    soup = read_url('https://movies.yahoo.com.tw/theater_list.html')
    all_theaters = soup.find_all('div', class_='l_box_inner')
    for theaters in all_theaters:
        place_theater = theaters.find_all('div', class_='theater_content')
        for theater in place_theater:
            # get the city id
            place_id = theater.get('data-area')
            place = theater.find('div', class_='theater_top').text
            places_id[place] = place_id

            # get the theater id
            theater_names = theater.find_all('div', class_='name')
            for theater_name in theater_names:
                cinema = theater_name.a.text
                theater_id = theater_name.a.get('href').split('=')[-1]
                cinema_id[place][cinema] = theater_id
    
    return places_id, cinema_id

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

# 取得地區列表
def getAllCity():
    global places_id, cinema_id
    places_id, cinema_id = places()
    list_city = list(places_id.keys())
    return list_city
#==================================