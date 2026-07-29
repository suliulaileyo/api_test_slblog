import requests


def login():
    json = {
        "account": "2594359191@qq.com",
        "captchaKey": "",
        "captchaVerification": "",
        "code": "",
        "email": "",
        "isDistributor": "true",
        "newPassword": "",
        "password": "Cf@2000...",
        "scene": 1,
        "username": ""
    }

    res = requests.post(url="http://192.168.101.156:8080/cloudstorage-api/app-api/member/auth/email-login",headers={"Content-Type": "application/json"},json=json)
    print(res.json())

login()