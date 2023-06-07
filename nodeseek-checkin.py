#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cron: 1 7 * * *
new Env('NodeSeek签到');
"""

import time
import requests
import base64
import json
import os
from datetime import datetime
from typing import BinaryIO , Dict , List , Union


local_cookies = os.environ["local_cookies"]

def checkin():
    url="https://www.nodeseek.com/api/attendance?random=false";
    hearder={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36','Cookie':local_cookies}
    res = requests.post(url=url, headers=hearder, verify=False).text
    print(res)

if __name__ == '__main__':
    checkin()
