import requests
from bs4 import BeautifulSoup
import html5lib
import json
import time

ID = input('id입력 : ')
PW = input('비번입력 : ')
start_time = time.time()
h = {
    'Accept' : '*/*',
    'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}

d = {
    'autoLogin' : 'Y',
    'userID' : ID, 
    'password' : PW,
    'credType' : 'BASIC',
    'retURL' : 'http://mportal.cau.ac.kr/common/auth/SSOlogin.do?redirectUrl=/main.do',
    'pwdTag' : 'password',
    'redirectUrl' : '/main.do'
}

with requests.Session() as s:
    url = 'https://sso2.cau.ac.kr/SSO/AuthWeb/Logon.aspx?ssosite=mportal.cau.ac.kr'
    r = s.post(url, data=d, headers=h)
    bs = BeautifulSoup(r.text, "html5lib")
    inputs = bs.select('input')
    for i in range(2):
        
        data = dict()

        for j in inputs:
            #print(j)
            try:
                data[j['name']] = j['value']
            except: 
                pass
        if i==0:
            url = "https://sso2.cau.ac.kr/SSO/AuthWeb/LogonDomain.aspx"
            r = s.post(url, data=data, headers=h)
            inputs = BeautifulSoup(r.text, "html5lib").select('input')
        else:
            url = "https://sso2.cau.ac.kr/SSO/AuthWeb/NACookieManage.aspx"
            r = s.post(url, data=data, headers=h)
    r = s.get('https://mportal.cau.ac.kr/index.do', headers=h)
    r = s.post('https://mportal.cau.ac.kr/std/usj/sUsjGdc003/index.do', data={
        'menuId' : '150202'
    }, headers=h)

    r = s.post('https://mportal.cau.ac.kr/std/usj/sUsjGdc003/selectGrade.ajax', data={
        'I_G_FLAG': 'S',
        'I_STD_NO': '20143583', # 이 payload에 정확히 뭔값 넣는거지?
        'I_ENG_GB': 'N',
        'I_SHYR': '4'
    },headers={
        'Accept' : '*/*',
        'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    })

    result = s.post('https://mportal.cau.ac.kr/std/usj/sUsjGdc003/selectGrade.ajax', json={
        'I_G_FLAG': 'S',
        'I_STD_NO': '20143583',
        'I_ENG_GB': 'N',
        'I_SHYR': '4'
    })
    result = json.loads(result.text)
    result = result['rtnmap']
    result = result["O_RETURNVALUE_01"]

    i = 1 
    for item in result:
        print(str(i)+' : ' + item['kor_nm'])
        i+=1

end_time = time.time()
print('Time taken : ' + str(end_time-start_time))
