# 获取特定的商店的评论
import os
import csv
from itertools import islice
import requests, json, time


def getfile(path):
    """获取特定路径下的所有文件"""
    for root, dirs, files in os.walk(path):
        L = list()
        for file in files:
            L.append(os.path.join(root,file))

        return L

if __name__ == "__main__":
    if not os.path.exists("comments"):
        os.makedirs("comments")

    L = getfile("data")
    former_url = "https://www.meituan.com/meishi/api/poi/getMerchantComment"

    # user-Agent
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

    # 添加cookie信息,似乎也可以不用添加cookie
    cookies_str = "_lxsdk_cuid=16ccbec81f6c8-09a76746427104-7373e61-144000-16ccbec81f6c8; __mta=42900890.1566789370756.1566789370756.1566789370756.1; client-id=0bc9e08a-88e9-44a6-9021-c4108f370a72; _hc.v=855087fe-e3ad-c8f9-9abd-86f0c42cd7dd.1566790954; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; mtcdn=K; ci=57; rvct=57%2C1; uuid=4483b661-f854-47b1-b097-79727fd0a686; IJSESSIONID=10e51xuggau3i1gfe698o4ahqz; iuuid=1D19F5F6762FF4BE4647DD0F76D42CD274B0D193F4EE512E61C1A7395CD97D41; cityname=%E6%AD%A6%E6%B1%89; _lxsdk=1D19F5F6762FF4BE4647DD0F76D42CD274B0D193F4EE512E61C1A7395CD97D41; _ga=GA1.2.1599517707.1566958874; _gid=GA1.2.3324680.1566958874; lat=30.616741; lng=114.360937; _lxsdk_s=16cd5fcd572-b56-c3e-943%7C%7C13"
    cookies_dict = {}
    for cookie in cookies_str.split(";"):
        k,v = cookie.split("=", 1)
        cookies_dict[k.strip()] = v.strip()

    
    for item in L:
        csv_file = csv.reader(open(item,"r",encoding="utf-8"))
        # 跳过表头读取文件
        for line in islice(csv_file,1,None):
            name = line[1] # 商店名字
            id = line [0] # 商店id
            allCommentNums = line[3] # 商店总的评论数

            # 这里有个问题，如果某个商家的评论数过多，一页可能显示不完全，这个时候可以采取分页处理
            # 或者我们不需要那么多信息，直接指定一个值，我这边指定200.
            if int(allCommentNums) >= 200:
                allCommentNums = 200
            
            # Query String parameters
            payload = {"uuid":"4483b661-f854-47b1-b097-79727fd0a686","paltform":"1","partner":"126","originUrl":"https://www.meituan.com/meishi/"+str(id)+"/","riskLevel":"1","optimusCode":"10", \
            "id":str(id),"userId":"","offset":"0","pageSize":str(allCommentNums),"sortType":"1"}

            page = requests.get(url = former_url, params = payload,cookies = cookies_dict, headers = headers)
            print(page.url)
            print(page.status_code)
            fetch_comments = json.loads(page.text)["data"]["comments"]

            # 获取评论的内容
            data = list()
            data.append("comment,star") 
            for item in fetch_comments:
                if item["comment"] == "":
                    data.append("该用户没有评论汉字"+","+str(item["star"]))
                else:
                    data.append(item["comment"].replace("\n"," ")+"\t"+str(item["star"]))

            # 写入文件
            with open("comments/"+str(id)+".csv","w",encoding="utf -8") as f:
                f.write("\n".join(data))
            
            # 睡眠一段时间
            time.sleep(3)
        break

