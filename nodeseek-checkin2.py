from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import random
import traceback
from fake_useragent import UserAgent
import os


username = os.environ["nodeseek_username"]
password= os.environ["nodeseek_password"]

def toNodeSeek():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    # 沙盒模式运行
    option.add_argument('no-sandbox')
    # 大量渲染时候写入/tmp而非/dev/shm
    option.add_argument('disable-dev-shm-usage')
    #user_agent = UserAgent.random
    #option.add_argument('--user-agent=%s' % user_agent)

    # 指定驱动路径
    browser = webdriver.Chrome('/usr/bin/chromedriver',options=option)
    #browser = webdriver.Chrome(options=option)
    #browser.set_page_load_timeout(3)
    url_login='https://www.nodeseek.com/signIn.html'
    browser.get(url_login)
    browser.find_element(By.ID,'Form_Name').send_keys(username)
    browser.find_element(By.ID,'Form_Password').send_keys(username)
    browser.find_element(By.ID,'Form_ApplyforMembership').click()
    
    url_attendance ='https://www.nodeseek.com/api/attendance?random=false'
    browser.get(url_attendance)
    print(browser.title)

    # 关闭浏览器
    browser.quit()


if __name__ == "__main__":
    toNodeSeek()