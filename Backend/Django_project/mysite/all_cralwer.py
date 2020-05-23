import requests
from bs4 import BeautifulSoup
import html5lib
import json
import time
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
from elections.models import Subject

if __name__=='__main__':
    print('start')
    category = {
        "00000" : ["3A110", "3A120", "3A130", "3A132", "3A133", "3A134", "3A140", "3A142", "3A143", "3A144", "3A150", "3A160", "3A170", "3A180", "3A190", "3A200"],
        "3A300" : ["3A310", "3A320", "3A330", "3A340", "3A350", "3A352", "3A353", "3A354", "3A355", "3A360", "3A362", "3A363", "3A370", "3A380", "3A390", "3A400", "3A410", "3A411", "3A412"],
        "3A500" : ["3A510","3A520", "3A530", "3A540", "3A550"],
        "3B100" : ["3B110", "3B120", "3B130", "3B132", "3B133", "3B140", "3B150", "3B152", "3B153", "3B160", "3B162", "3B163", "3B170", "3B180", "3B190"],
        "3B300" : ["3B310", "3B312", "3B313", "3B314", "3B320", "3B322", "3B323", "3B330", "3B340", "3B350", "3B360", "3B362", "3B370", "3B372", "3B373", "3B374", "3B375", "3B380", "3B382", "3B383", "3B384", "3B390", "3B391", "3B392", "3B393"],
        "3B400" : ["3B410", "3B420", "3B421", "3B422", "3B430", "3B431", "3B432", "3B433", "3B450", "3B460"],
        "3B500" : ["3B510"],
        "3C100" : ["3D110", "3C112", "3C115", "3C120", "3C130", "3C140", "3C150", "3C160", "3C170", "3C180", "3C190", "3C200", "3C210", "3C220", "3C230"],
        "3D100" : ["3D110", "3D112", "3D113", "3D114"],
        "3D500" : ["3D510"],
        "3D600" : ["3D520", "3D530"],
        "3F400" : ["3F430", "3F440", "3F450", "3F460"],
        "3E100" : ["3E110", "3E112", "3E113", "3E114", "3E115", "3E116", "3E117", "3E120", "3E122", "3E123", "3E124", "3E130", "3E132", "3E133", "3E134", "3E135", "3E136", "3E137", "3E138", "3E139", "3E140", "3E142", "3E143", "3E144", "3E145", "3E150", "3E152", "3E153", "3E160", "3E170", "3E180", "3E190", "3E192", "3E193", "3E194"],
        "3D300" : ["3D310", "3D320"],
        "30140" : ["30146", "30147",  "30148",  "30149",  "30150", "30167", "30168",  "30169",  "30170", "30171", "30177", "30178", "31001", "31002", "31003"],
        "30180" : ["30183", "30184", "30193", "30194", "30195", "30196"],
        "30220" : ["30229", "30230", "30237", "30238", "30246", "30247", "30253", "30254", "30255", "30257", "30258",  "30259",  "30260",  "30261",  "30262",  "30263"],
        "30270" : ["30279", "30280", "30281", "30282", "30283"],
        "30290" : ["30294"],
        "30300" : ["30306", "30307", "30308", "30309", "30311", "30313", "30317"],
        "30330" : ["30336"],
        "30390" : ["30396", "30397", "30398"],
        "30410" : ["30415", "30416"],
        "30640" : ["30643", "30644", "30645", "30646", "30647", "30650", "30651"],
        "30680" : ["30682"],
        "30690" : ["30692"],
        "30700" : ["30702"],
        "3M100" : ["3M130"]
    }
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

    informList = ['colgnm','sustnm','pobtnm','shyr','profnm','ltbdrm', 'sbjtclss', 'clssnm', 'pnt', 'remk']
    myList = []

    with requests.Session() as s:
        url = 'https://sso2.cau.ac.kr/SSO/AuthWeb/Logon.aspx?ssosite=sugang.cau.ac.kr'
        r = s.post(url, data=d, headers=h)
        bs = BeautifulSoup(r.text, "html5lib")
        inputs = bs.select('input')
        for i in range(2):
            print("enter1")
 
            data = dict()

            for j in inputs:
                print(j)
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

        for year in range(2010,2021,1):
            print("enter2")
            for semester in ["1","S","2","W"]:
                for colgcd in category.keys():
                    for sust in category[colgcd]:
                        if colgcd == "00000":
                            r = s.post('http://sugang.cau.ac.kr/TIS/std/usk/sUskSif001/selectSbjt.do', headers=h,
                            data ='''<map><year value='''+'"'+str(year)+'"'+'''/><campfg value="1"/><course value="3"/><gb value="3"/><colgcd value="00000"/><shtm value='''+'"'+str(semester)+'"'+'''/><sust value='''+'"'+sust+'"'+'''/><search_gb value="00000"/><kornm value=""/></map>''')
                            soup = BeautifulSoup(r.text, 'html.parser')
                            target = soup.find('vector') 
                            if len(target) == 0:
                                continue
                            for item in target:
                                dic = {}
                                dic["year"] = str(year)
                                dic["semester"] = semester
                                for element in informList:
                                    try:
                                        dic[element] = item.select_one(element)['value'].strip()
                                    except:
                                        dic[element] = "None"
                                #dic가 myList에 없을때 DB에 저장하는거 짜셈
                                if dic in myList:
                                    continue
                                else:
                                    print(str(year)+":"+semester+":"+dic["clssnm"])
                                    myList.append(dic)
                                    Subject(course_year=dic["year"], course_semester=dic["semester"], course_colgnm=dic["colgnm"], course_sustnm=dic["sustnm"], course_pobjnm=dic["pobtnm"], course_shyr=dic["shyr"], course_profnm=dic["profnm"], course_ltbdrm=dic["ltbdrm"], course_sbjtclss=dic["sbjtclss"], course_clssnm=dic["clssnm"], course_pnt=dic["pnt"], course_remk=dic["remk"]).save()
                        else:
                            r = s.post('http://sugang.cau.ac.kr/TIS/std/usk/sUskSif001/selectSbjt.do', headers=h,
                            data ='''<map><year value='''+'"'+str(year)+'"'+'''/><campfg value="1"/><course value="3"/><gb value="3"/><colgcd value='''+'"'+colgcd+'"'+'''/><shtm value='''+'"'+str(semester)+'"'+'''/><sust value='''+'"'+sust+'"'+'''/><search_gb value="ELSE"/><kornm value=""/></map>''')
                            soup = BeautifulSoup(r.text, 'html.parser')
                            target = soup.find('vector')    
                            if len(target) == 0:
                                continue
                            for item in target:
                                dic = {}
                                dic["year"] = str(year)
                                dic["semester"] = semester
                                for element in informList:
                                    try:
                                        dic[element] = item.select_one(element)['value'].strip()
                                    except:
                                        dic[element] = "None"
                                #dic가 myList에 없을때 DB에 저장하는거 짜셈
                                if dic in myList:
                                    continue
                                else:
                                    print(str(year)+":"+semester+":"+dic["clssnm"])
                                    myList.append(dic)
                                    Subject(course_year=dic["year"], course_semester=dic["semester"], course_colgnm=dic["colgnm"], course_sustnm=dic["sustnm"], course_pobjnm=dic["pobtnm"], course_shyr=dic["shyr"], course_profnm=dic["profnm"], course_ltbdrm=dic["ltbdrm"], course_sbjtclss=dic["sbjtclss"], course_clssnm=dic["clssnm"], course_pnt=dic["pnt"], course_remk=dic["remk"]).save()
 
