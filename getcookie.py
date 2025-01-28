import undetected_chromedriver as uc
import time
import json
import base64
import platform
import subprocess
from datetime import datetime


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
        print('Check chrome version failed:{}'.format(e))
        return 0
    if system == "Linux" or system == "Darwin":
        out = out.decode("utf-8").split(" ")[2].split(".")[0]
    elif system == "Windows":
        out = out.decode("utf-8").split(".")[0]
    # exit(str(int(out)))
    return int(out)

# 填写webdriver的保存目
options = uc.ChromeOptions()
# options.add_argument('--proxy-server=socks5://127.0.0.1:10088')
options.add_argument("--disable-popup-blocking")
driver = uc.Chrome(version_main=get_driver_version(), options=options)

# 记得写完整的url 包括http和https
driver.get('https://weread.qq.com/')

# 首先清除由于浏览器打开已有的cookies
driver.delete_all_cookies()

# 程序打开网页后 “手动登陆账户” 
input("完成登录后，按任意键")

with open('cookies.txt','w') as f:
    # 将cookies保存为json格式
    cookies = json.dumps(driver.get_cookies())
    f.write('\n'+str(datetime.now())+'\n')
    f.write(cookies+'\n')
    print(cookies)

    # 编码
    message = cookies
    message_bytes = message.encode()
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode()
    print(base64_message)
    f.write(base64_message+'\n')

driver.quit()
