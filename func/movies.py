import requests
from bs4 import BeautifulSoup

base_url = "https://y80s.tv"


# 获取播放地址
def get_movie_info(id):
    source_list=[]
    url=base_url +id.strip() + "/play/h-1"
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find_all("a",{"class": "a movie_a"})
    for i in data:
        source_list.append("{}：{}".format(i.text,i["href"][7:]))

    return source_list


def get_movie_list(name):
    moves= []
    url=base_url+"/movie/search/"
    data = {
        "search_typeid": 1,
        "skey": name,
        "Input": "搜索",
    }

    response = requests.post(url, data=data)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find("ul", {"class": "me1 clearfix"})
    data = data.find_all("li")
    for i in data:
        j = i.find("a")
        source=get_movie_info(j["href"])
        moves.append([[ j.find("img")["_src"],j["title"]],source])
    return moves


def get_move_iframe(source):
    url=base_url+"/movie/" + source
    print(url)
    re = requests.get(url)
    re.encoding = "utf-8"
    soup = BeautifulSoup(re.text, "html.parser")
    data = soup.find("iframe")
    return data["src"]
