import requests
from bs4 import BeautifulSoup
import html5lib
import json
import time

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

informList = ['pobtnm', 'sbjtclss', 'clssnm'] #'pnt', 'remk'
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

    for year in range(2013,2021):
        for semester in range(1,3):
            if year == 2013 or year == 2014:
                r = s.post('http://sugang.cau.ac.kr/TIS/std/usk/sUskSif001/selectSbjt.do', headers=h, 
                data='''<map><year value='''+'"'+str(year)+'"'+'''/><campfg value="1"/><course value="3"/><gb value="3"/><colgcd value="3B300"/><shtm value='''+'"'+str(semester)+'"'+'''/><sust value="3B360"/><search_gb value="ELSE"/><kornm value=""/></map>''')
                soup = BeautifulSoup(r.text, 'html.parser')
                target = soup.find('vector')
                for item in target:
                    dic = {}
                    dic['year'] = str(year)
                    for element in informList:
                        dic[element] = item.select_one(element)['value'].strip()
                    myList.append(dic)

            elif year >= 2015 and year <= 2018:
                for big in ['3B300', '3B400']:
                    if big == '3B300':
                        r = s.post('http://sugang.cau.ac.kr/TIS/std/usk/sUskSif001/selectSbjt.do', headers=h, 
                        data='''<map><year value='''+'"'+str(year)+'"'+'''/><campfg value="1"/><course value="3"/><gb value="3"/><colgcd value='''+'"'+big+'"'+'''/><shtm value='''+'"'+str(semester)+'"'+'''/><sust value="3B360"/><search_gb value="ELSE"/><kornm value=""/></map>''')
                        soup = BeautifulSoup(r.text, 'html.parser')
                        target = soup.find('vector')
                        for item in target:
                            dic = {}
                            dic['year'] = str(year)
                            for element in informList:
                                dic[element] = item.select_one(element)['value'].strip()
                            myList.append(dic)
                    else:
                        for small in ['3B420','3B421','3B422']:
                            r = s.post('http://sugang.cau.ac.kr/TIS/std/usk/sUskSif001/selectSbjt.do', headers=h, 
                            data='''<map><year value='''+'"'+str(year)+'"'+'''/><campfg value="1"/><course value="3"/><gb value="3"/><colgcd value='''+'"'+big+'"'+'''/><shtm value='''+'"'+str(semester)+'"'+'''/><sust value='''+'"'+small+'"'+'''/><search_gb value="ELSE"/><kornm value=""/></map>''')
                            soup = BeautifulSoup(r.text, 'html.parser')
                            target = soup.find('vector')
                            for item in target:
                                dic = {}
                                dic['year'] = str(year)
                                for element in informList:
                                    dic[element] = item.select_one(element)['value'].strip()
                                myList.append(dic)
            elif year >= 2019:
                if year==2020 and semester==2:
                    break
                
                r = s.post('http://sugang.cau.ac.kr/TIS/std/usk/sUskSif001/selectSbjt.do', headers=h, 
                data='''<map><year value='''+'"'+str(year)+'"'+'''/><campfg value="1"/><course value="3"/><gb value="3"/><colgcd value="3B500"/><shtm value='''+'"'+str(semester)+'"'+'''/><sust value="3B510"/><search_gb value="ELSE"/><kornm value=""/></map>''')
                soup = BeautifulSoup(r.text, 'html.parser')
                target = soup.find('vector')
                for item in target:
                    dic = {}
                    dic['year'] = str(year)
                    for element in informList:
                        dic[element] = item.select_one(element)['value'].strip()
                    myList.append(dic)

newList = []
for item in myList:
    if item not in newList:
        newList.append(item)
print(len(myList))
print(len(newList))
f = open('/home/ubuntu/test.txt', mode='at', encoding='utf-8')
f.write(str(len(myList)))
f.write('\n')
f.write(str(len(newList)))
f.write('\n')
for item in newList:
    for key in item.keys():
        f.write(item[key])
        f.write('\t')
    f.write('\n\n')

f.close()

end_time = time.time()
print(end_time-start_time)

