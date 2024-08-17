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
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 GLS/100.10.9989.100")
    options.add_argument("--disable-popup-blocking")

    # 获取驱动版本
    version = get_driver_version()
    print("driver_version=%d" % version, flush=True)
    
    # 创建驱动
    driver = uc.Chrome(version_main=version, options=options)
    
    # 记得写完整的url 包括http和https
    driver.get(r'https://weread.qq.com/web/reader/98f3201071a2456898fff22')

    # 首先清除由于浏览器打开已有的
    driver.delete_all_cookies()

    # 读取cookie
    # with open('cookies.txt','r') as f:
    #     # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    #     cookies_list = json.load(f)

    #     #方法2删除该字段
    #     for cookie in cookies_list:
    #         # 该字段有问题所以删除就可以 
    #         # if 'expiry' in cookie:
    #         #     del cookie['expiry']
    #         driver.add_cookie(cookie)


    # input('载入cookie前')

    # 读取及载入cookie
    cookies_list = json.loads(cookie_string)
    for cookie in cookies_list:
        driver.add_cookie(cookie)

    # 刷新网页
    driver.refresh()

    # 等待10秒
    time.sleep(10)

    # input('登录后')

    try:
        element = driver.find_element(By.XPATH, "//*[@id='routerView']/div/div[1]/div[1]/div/div[2]/div")
        print("登录成功！", flush=True)
    except NoSuchElementException:
        exit("登录失败！")

    # 创建一个 ActionChains 对象
    actions = ActionChains(driver)

    pages = random.randint(80, 150)
    for i in range(pages):
        try:
            # 查找并点击指定的元素(下一页按钮)
            element = driver.find_element(By.XPATH, "//*[@id='routerView']/div/div[1]/div[2]/div/div[2]/div[4]/div[2]/button/span[1]")
            # element.click()
            actions.send_keys(Keys.ARROW_RIGHT).perform()
            print("下一页！ i=%d" % i, flush=True)
        except NoSuchElementException:
            # 查找并点击指定的元素(上一页按钮)
            # element = driver.find_element(By.XPATH, "//*[@id='routerView']/div/div[1]/div[2]/div/div[2]/div[4]/div[1]/button/span[2]")
            # element.click()
            actions.send_keys(Keys.ARROW_LEFT).perform()
            print("上一页！ i=%d" % i, flush=True)
        time.sleep(random.randint(20, 60))

    driver.refresh()
    time.sleep(10)
        

    # 退出
    # driver.close()
    driver.quit()
    


if __name__ == "__main__":
    b64str = sys.argv[1]
    assert b64str
    
    # # 编码
    # message = "Hello, World!"
    # message_bytes = message.encode()
    # base64_bytes = base64.b64encode(message_bytes)
    # base64_message = base64_bytes.decode()
    # print(base64_message)

    # 解码
    base64_message = b64str
    base64_bytes = base64_message.encode()
    message_bytes = base64.b64decode(base64_bytes)
    cookie_string = message_bytes.decode()
    # print(cookie_string)

    weread(cookie_string)