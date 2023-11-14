import requests
import pickle
import random
import re
import os
import json
import onetimepass as otp
from time import sleep
from typing import BinaryIO , Dict , List , Union
import base64
import logging
import datetime

host = "https://t66y.com/"

filename = os.environ["filename2"]
checkin_url = os.environ["checkin_url2"]
reply_content = os.environ["reply_content2"]

session = requests.Session()
host_index = f"{host}index.php"
login = f"{host}login.php"
thread0806_url=f"{host}thread0806.php?fid=7"
post_url = f"{host}post.php?"
userAgent : str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
headers= {
    'Host': host.split("//")[1].replace("/", ""),
    'Proxy-Connection': 'keep-alive',
    'Referer': login,
    'User-Agent': userAgent
}


def load_cookies() -> None:
    with open(filename, 'rb') as f:
        try:
            session.cookies.update(pickle.load(f))
            logger.debug(f"load {filename} success")
        except:
            ...


#校验cookies是否有效
def is_valid_cookies() -> bool:
    res = session.get(host_index , headers = headers)
    if res.text.find("上次登錄時間") != -1 :
        return True
    else:
        return False

# 进入thread0806
def toThread0806Page():
    sleep(0.1)
    res = session.get(thread0806_url,headers = headers)
   
# 进入签到页面
def toCheckinPage():
    sleep(0.2)
    print(checkin_url)
    res = session.get(checkin_url,headers = headers)
    print(res.text)


def reply() -> None:
    sleep(0.1)
    title = get_title(checkin_url)
    content = reply_content
    tid = get_tid(checkin_url)
    print(title)

    data = {
        'atc_usesign':'1',
        'atc_convert':'1',
        'atc_autourl': '1',
        'atc_title':  title,
        'atc_content': content ,
        'step': '2',
        'action': 'reply',
        'fid': '23',
        'tid':  tid,
        'atc_attachment': 'none',
        'pid':'',
        'article':'',
        'touid':'',
        'verify':'verify'
    }
    res = session.post(url= post_url , data = data , headers = headers )
    print(res.text)


 #获取给定url的主题名字
def get_title(url) -> str:
    sleep(0.2)
    res = session.get(url = url , headers = headers)
    pat_title = '<b>本頁主題:</b> .*</td>'
    try:
        title = re.search(pat_title, res.text).group(0)
        title = "Re:" + title.replace('<b>本頁主題:</b> ','').replace('</td>','')
    except:
        title = "Re: "
    return title


#从url中提取出tid
def get_tid( url) -> str:
    pat_tid = "/(\d+).html"
    tid = re.search(pat_tid , url).group(1)
    return tid

def today():
    now = datetime.datetime.now()
    today = now.strftime("%d")
    print("今天的日期是：", today)
    return today

if __name__ == "__main__":
    today = today()
    if today == '30' or today == '31':
        print("今天是"+today +"，不执行sleep！")
    else:
        sleep_time = random.randint(50,800)
        print('休眠'+str(sleep_time)+'秒')
        sleep(sleep_time)
    load_cookies()
    is_valid_cookies()
    #toThread0806Page()
    #toCheckinPage()
    reply()
