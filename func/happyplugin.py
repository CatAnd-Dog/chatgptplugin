import requests

def get163(name,proxy=None):
    ulr="http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={}&type=1&offset=0&total=true".format(name)
    port={
        "http":proxy
    }

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        "Cache-Control" : "no-cache",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/search/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    response=requests.get(url=ulr,headers=headers,proxies=port).json()

    songs=response["result"]["songs"]
    song_data=[]
    for data in songs:
        song_data.append([data["name"],data["id"],data["fee"]])

    return song_data


