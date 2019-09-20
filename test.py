#导入必要的包
import requests
from bs4 import BeautifulSoup


# 武汉理工大学科url
url = 'https://www.whut.edu.cn/'
# 发起访问请求
page = requests.get(url = url)
# 输出返回信息
print(page.url)
print(page.status_code)
for k,v in page.headers.items():
    print(k,":\t",v)
# 初始化soup对象
soup = BeautifulSoup(page.text,"html.parser")
# 找到class属性为art_list的标签，实质是获取所有的学校动态
soup = soup.find("ul",{"class":"art_list"})
# 找到上面一层标签下的所有li标签，并输出其中的title内容
soup = soup.find_all("li")
for item in soup:
    result = item.find('a')
    print(result.get('href')+"\t"+result.get('title'))
