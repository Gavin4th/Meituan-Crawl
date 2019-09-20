# 登录前的页面

import requests
from bs4 import BeautifulSoup


url = 'https://wh.meituan.com/meishi/'
r = requests.get(url)

print
soup = BeautifulSoup(r.text,"html.parser")

with open("未登录.txt","w",encoding="utf-8") as f:
    f.write(r.url+"\n"+soup.prettify())

