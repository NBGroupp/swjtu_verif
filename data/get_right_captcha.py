#coding: utf8
import requests
from pre_operation import pre_operation
from time import sleep
from pytesser import pytesser
from PIL import Image


dean_url = 'http://jiaowu.swjtu.edu.cn/servlet/UserLoginSQLAction'
captcha_url = 'http://jiaowu.swjtu.edu.cn/servlet/GetRandomNumberToJPEG'
fake_id = '2000123456'
fake_passwd = '123456'

login_data = {
    "user_id": fake_id,
    "password": fake_passwd,
    "ranstring": '',
    "user_type": 'student'
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Host": "jiaowu.swjtu.edu.cn",
    "Origin": "http://jiaowu.swjtu.edu.cn",
    "Referer": "http://jiaowu.swjtu.edu.cn/service/login.jsp",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def isalpha(text):
    
    for ch in text:
        
        if not ch.isalpha():
            return 0
    
    return 1

def recognize(pic_name):

    im = pre_operation(pic_name)

    text = pytesser.image_to_string(im).strip()
    
    if(len(text) == 4 and isalpha(text)):
        print(text)
        return text.upper()
    return None


def download_captcha():

    s = requests.session()
    s.headers = headers
    r = s.get(captcha_url)
    with open('temp_pic', 'wb') as pic:
        pic.write(r.content)
    return s, 'temp_pic'

def try_login():

    s, captcha_file = download_captcha()
    res = recognize(captcha_file)
    if res:
        login_data['ranstring'] = res
        r = s.post(dean_url, data=login_data)
        
        content = r.content.decode('gbk')
        if '密码不正确' in content:
            print('sucess\n')
            return captcha_file, res
        else:
            print('识别错误\n')
    else:
        print('无法识别')
    return None, None

if __name__ == '__main__':
    while(1):
        try:
            # sleep(0.1)
            captcha_file, captcha_name = try_login()
            if(captcha_file):
                with open(captcha_file, 'rb') as o_pic:
                    data = o_pic.read()
                with open('success/' + captcha_name + '.jpg', 'wb') as n_pic:
                    n_pic.write(data)
        except Exception as e:
            print(e)
            sleep(5)


