# encoding=utf8

import undetected_chromedriver as uc
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
import platform
import subprocess
import base64
import io
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def get_driver_version():
    system = platform.system()
    if system == "Linux": # github actions linux 系统没有图形化界面，该选项不能直接用
        cmd = r'google-chrome --version'
    elif system == "Darwin":
        cmd = r'''/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'''
    elif system == "Windows":
        cmd = r'''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"'''

    try:
        out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    except IndexError as e:
        exit('Check chrome version failed:{}'.format(e))
    if system == "Linux" or system == "Darwin":
        out = out.decode("utf-8").split(" ")[2].split(".")[0]
    elif system == "Windows":
        out = out.decode("utf-8").split(".")[0]
    
    return int(out)

def weread(cookie_string):
    # 设置驱动选项
    options = uc.ChromeOptions()
    # options.add_argument('--proxy-server=socks5://127.0.0.1:10088')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0")
    options.add_argument("--disable-popup-blocking")

    # 获取驱动版本
    version = get_driver_version()
    print("driver_version=%d" % version, flush=True)
    
    # 创建驱动
    driver = uc.Chrome(version_main=version, options=options)

    # 记得写完整的url 包括http和https
    driver.get(r'https://weread.qq.com')

    # 首先清除由于浏览器打开已有的
    driver.delete_all_cookies()

    # 读取及载入cookie
    if cookie_string.startswith("cookie:"):
        cookie_string = cookie_string[len("cookie:"):]
    cookie_string = cookie_string.replace("/","%2")
    cookie_dict = [ 
        {"name" : x.split('=')[0].strip(), "value": x.split('=')[1].strip()} 
        for x in cookie_string.split(';')
    ]

    driver.delete_all_cookies()
    for cookie in cookie_dict:
        driver.add_cookie({
            "domain": "weread.qq.com",
            "name": cookie["name"],
            "value": cookie["value"],
            "path": "/",
        })

    # 记得写完整的url 包括http和https
    driver.get(r'https://weread.qq.com/web/reader/47532ac05c659b47554a825k283328802332838023a7529')

    # 等待10秒
    time.sleep(10)

    # input('登录后')

    try:
        element = driver.find_element(By.XPATH, "//*[@id='routerView']/div/div[1]/div[1]/div/div[2]/div")
        print("Login successful", flush=True)
    except NoSuchElementException:
        exit("Login failed")

    # 创建一个 ActionChains 对象
    actions = ActionChains(driver)

    pages = random.randint(50, 100)
    for i in range(pages):
        try:
            # 查找并点击指定的元素(下一页按钮)
            element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div[5]/div[2]/button")
            
            # element.click()
            actions.send_keys(Keys.ARROW_RIGHT).perform()
            print("next_page i=%d" % i, flush=True)
        except NoSuchElementException:
            exit('err: No next page button!')
            # 查找并点击指定的元素(上一页按钮)
            # element = driver.find_element(By.XPATH, "//*[@id='routerView']/div/div[1]/div[2]/div/div[2]/div[4]/div[1]/button/span[2]")
            # element.click()
            actions.send_keys(Keys.ARROW_LEFT).perform()
            print("pre_page i=%d" % i, flush=True)
        time.sleep(random.randint(30, 60))
    print("done!", flush=True)
    driver.refresh()
    time.sleep(10)
        

    # 退出
    # driver.close()
    driver.quit()
    


if __name__ == "__main__":
    cookie_string = sys.argv[1]
    assert cookie_string

    weread(cookie_string)
