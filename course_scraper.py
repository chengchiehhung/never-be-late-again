from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json

# Login to YZU's portal homepage
with requests.Session() as s:
    url = "https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx"
    page = requests.get(url)
    print(page.text)
    soup = BeautifulSoup(page.content, 'lxml')

    with open("info.json") as f:
            data = json.load(f)
    payload_loginPage = {
        'Txt_UserID': data['account'],
        'Txt_Password': data['password'],
        'ibnSubmit': '登入'
    }

    payload_loginPage["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
    payload_loginPage["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
    payload_loginPage["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]
    s.post(url, data=payload_loginPage)

