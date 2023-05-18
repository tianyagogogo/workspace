#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cron: 1 7,18 * * *
new Env('tly签到');
"""

import time
import requests
import base64
import json
import os
from datetime import datetime
import cloudscraper
from typing import BinaryIO , Dict , List , Union
from notify import send

cookie = os.environ["tly_cookie"]
userid = os.environ["userid"]
apikey = os.environ["apikey"]

scraper = cloudscraper.create_scraper()


def apitruecaptcha(content : BinaryIO) -> str:
    image=base64.b64encode(content)
    url='https://api.apitruecaptcha.org/one/gettext'
    data={
        'data':str(image,'utf-8'),
        'userid':userid,
        'apikey':apikey
    }
    result = requests.post(url, json.dumps(data))
    res=result.json()
    try:
        code = res['result']
    except:
        print(f"api error,{str(res)}")
        code = "XXXX"
    print("apitruecaptcha code: %s" % code)
    return code


def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()




def tly():
    signUrl="https://tly.com/modules/index.php"
    hearder={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','Cookie':cookie}

    res=scraper.get(url=signUrl,headers=hearder).text
    signtime=getmidstring(res,'<p>上次签到时间：<code>','</code></p>')
    timeArray = time.strptime(signtime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    t = int(time.time())

    if t-timeStamp>86400:
        print("距上次签到时间大于24小时啦,可签到")
        #获取验证码图片
        captchaUrl="https://tly.com/other/captcha.php"
        signurl="https://tly.com/modules/_checkin.php?captcha="
        hearder={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36','Cookie':cookie}
        res1=scraper.get(url=captchaUrl,headers=hearder)
        oocr=apitruecaptcha(res1.content)
        res2=scraper.get(url=signurl+oocr.upper(),headers=hearder).text
        print(res2)
        send('tly签到：', res2)
    else:
        print("还未到时间！",t-timeStamp)
        send('tly签到：', "还未到时间！" + str(t-timeStamp))


def main_handler(event, context):
    tly()


if __name__ == '__main__':
    tly()
