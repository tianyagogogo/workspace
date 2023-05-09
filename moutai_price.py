#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cron: 1 7 * * *
new Env('茅台价格')
"""

import requests,time,os,base64
from notify import send

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
today_time=time.strftime('%Y-%m-%d', time.localtime())

def moutai_data():
    url = 'aHR0cHM6Ly9wYXltZW50Lm5qeWh3bC50b3AvYXBpL3Byb3h5L3B1YmxpYy9hcGkvcHJpY2Uvc2VsZWN0UGFnZT9wYWdlPQ=='
    try:
        url=base64.b64decode(url).decode("utf-8")
        r=requests.get(url+'1',headers=headers,timeout=7)
        r.encoding=r.apparent_encoding
        r2 = requests.get(url + '2', headers=headers, timeout=7)
        r2.encoding = r2.apparent_encoding
        mt_data = r.json()['content'] +r2.json()['content']
        return  mt_data
    except Exception as e:
        print(f'接口失效!或者网络问题!\n{e}')

def moutai_Excel():
    title= f"今日茅台行情:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} \n"
    str=""
    mt_data=moutai_data()
    for i in mt_data:
        str+=f"{i['name']} 平均:{i['averagePrice']}元 昨天:{i['yesterdayPrice']}元 \n"
    send(title, str)  # 消息发送

if __name__ == '__main__':
   moutai_Excel()


