from bs4 import BeautifulSoup
import requests
import json

# Login to YZU's portal homepage
with requests.Session() as s:
    url_login = 'https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx'
    page_login = s.get(url_login)
    url_defaultPage = 'https://portalx.yzu.edu.tw/PortalSocialVB/FMain/DefaultPage.aspx'

    headers =  {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        # this is a critical information
        "Cookie": f"ASP.NET_SessionId={s.get(url_defaultPage).cookies.get('ASP.NET_SessionId')}"
    }

    soup = BeautifulSoup(page_login.content, 'lxml')
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
    s.post(url_login, data=payload_loginPage, headers=headers)

    print(s.get(url_defaultPage).text)