import requests
from bs4 import BeautifulSoup
import html5lib
import json
import time
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
from elecions.models import Substitute

if __name__=='__main__':
    start_time = time.time()
    h = {
        'Accept' : '*/*',
        'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    d = {
        'userID' : '', #ID
        'password' : '', #PW
        'credType' : 'BASIC',
        'retURL' : 'http://sugang.cau.ac.kr/TIS/regCourse.jsp',
        'usercred':''
    }

    myList = []

    with requests.Session() as s:
        url = 'https://sso2.cau.ac.kr/SSO/AuthWeb/Logon.aspx?ssosite=sugang.cau.ac.kr'
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
        

        for code in range(55390,100000):
            source = str(code).zfill(5)
            print(code)
            r = s.post('http://sugang.cau.ac.kr/TIS/std/usk/sUskSif003/selectList.do', data='''<map><s_gb value="2"/><s_txt value='''+'"'+source+'"'+'''/></map>''', headers=h)

            soup = BeautifulSoup(r.text, 'html.parser')
            target = soup.find('vector')
            if len(target) == 0:
                continue
            print('step#'+source+'...')
            for item in target:        
                tmpList = []    
                tmpList.append(item.select_one('sbjtnoold')['value'])
                tmpList.append(item.select_one('sbjtnmold')['value'])
                tmpList.append(item.select_one('sbjtno')['value'])
                tmpList.append(item.select_one('sbjtnm')['value'])
                if tmpList in myList:
                    continue
                else:
                    myList.append(tmpList)
                
                    Substitute(course_id=tmpList[0], course_title=tmpList[1], sub_id=tmpList[2], sub_title=tmpList[3]).save()

   # newList = []

    #for item in myList:
    #    if item in newList:
    #        continue

    #    else:
    #        newList.append(item)

   # return newList

#if __name__=='__main__':
 #   sub_dict = func()
    
 #   print('enter')
 #   for c_i, c_t, s_i, s_t in sub_dict.items():
 #       Substitute(course_id=c_i, course_title= c_t, sub_id=s_i, sub_title=s_t).save()    

        



