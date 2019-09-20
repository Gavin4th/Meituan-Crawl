# 登录后的页面
import requests
from bs4 import BeautifulSoup
import json, os, time


def crawl(num):
    url = 'https://wh.meituan.com/meishi/pn'+str(num)+'/'

    # 构造cookie信息,从对应网站上复制下来即可,不过我们好像不太需要

    # cookies_str = '填写cookie信息'
    # cookies_dict = {}
    # for cookie in cookies_str.split(";"):
    #     k, v = cookie.split("=", 1)
    #     cookies_dict[k.strip()] = v.strip()

    # 其它请求头信息，添加设备信息即可正常访问网站
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

    # 访问页面
    # page = requests.get(url = url, cookies = cookies_dict, headers = headers) # 有cookie
    page = requests.get(url = url, headers = headers) # 无cookie 登录

    print(page.url)
    print(page.status_code)
    print(page.headers)
    for k,v in page.headers.items():
        print(k,":\t",v)
    
    soup = BeautifulSoup(page.text,"html.parser")
    soup = soup.find_all("script")
    # 然后自己去找吧,ahh
    result = soup[14].get_text().strip()
    result = result[19:-1]
    result = json.loads(result)
    result = result['poiLists']['poiInfos'] 
    """
    {'poiId': 193327411, 'frontImg': 'https://img.meituan.net/600.600/msmerchant/8b668090d6db86a076e2aef08ab94c7030044.jpg',
    'title': '么肆烤肉（大花岭店）', 'avgScore': 4, 'allCommentNum': 5, 'address': '洪山区大桥新区武昌大道888号',
    'avgPrice': 74, 'dealList': [], 'hasAds': True, 'adsClickUrl':
    'none'}
    """
    
    # 将所需要的文件写入csv文件
    contents = list()
    # 表头
    contents.append("poiId,title,avgScore,allCommentNum,address,avgPrice")
    # 内容
    for item in result:
        contents.append(str(item["poiId"])+","+item["title"]+","+str(item["avgScore"])+"," \
        +str(item["allCommentNum"])+","+item["address"]+","+str(item["avgPrice"]))
    
    with open("data/"+"page"+str(num)+".csv","w",encoding="utf-8") as f:
        f.write("\n".join(contents))

    print("page{} 写入完毕".format(num))
    time.sleep(3)
    


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    for num in range(1,10):
        crawl(num)