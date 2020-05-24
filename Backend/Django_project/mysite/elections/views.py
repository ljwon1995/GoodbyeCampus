from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect, Http404
from django.http import JsonResponse
import datetime
import socket
import crawlers
from .models import Compulsory, Substitute, Subject

funclist = []   #질문 대답 함수 리스트
takeList = []   #사용자가 들은 과목 리스트

requirements = {}   #각 년도별 졸업요건
requirements["2010"] = {}
requirements["2011"] = {}
requirements["2012"] = {}
requirements["2013"] = {}
requirements["2014"] = {}
requirements["2015"] = {}
requirements["2016"] = {}
requirements["2017"] = {}
requirements["2018"] = {}
requirements["2019"] = {}
requirements["2020"] = {}


requirements["2010"]["totalCredits"]=132         #Total required credits
requirements["2010"]["numCoreGE"]=3              #Number of core General Education courses to take
requirements["2010"]["GECreditsLimit"]=52        #Maximum General Education courses credit
requirements["2010"]["majorCredits"]=66          #Total credits required for major courses
requirements["2010"]["exclusiveGECredits"]=6     #Total credits for exclusive General Education courses
requirements["2010"]["bsmCredits"]=18            #Total credits for bsm courses
requirements["2010"]["designSubjectsCredits"]=12 #Total credits required for design courses
requirements["2010"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2010) # List of compulsory subjects for the year

requirements["2011"]["totalCredits"]=132
requirements["2011"]["numCoreGE"]=3
requirements["2011"]["GECreditsLimit"]=45
requirements["2011"]["majorCredits"]=66
requirements["2011"]["exclusiveGECredits"]=6
requirements["2011"]["bsmCredits"]=18
requirements["2011"]["designSubjectsCredits"]=12
requirements["2011"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2011)

requirements["2012"]["totalCredits"]=132
requirements["2012"]["numCoreGE"]=3
requirements["2012"]["GECreditsLimit"]=45
requirements["2012"]["majorCredits"]=66
requirements["2012"]["exclusiveGECredits"]=6
requirements["2012"]["bsmCredits"]=18
requirements["2012"]["designSubjectsCredits"]=12
requirements["2012"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2012)

requirements["2013"]["totalCredits"]=140
requirements["2013"]["numCoreGE"]=3
requirements["2013"]["GECreditsLimit"]=45
requirements["2013"]["majorCredits"]=84
requirements["2013"]["exclusiveGECredits"]=6
requirements["2013"]["bsmCredits"]=18
requirements["2013"]["designSubjectsCredits"]=12
requirements["2013"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2013)

requirements["2014"]["totalCredits"]=140
requirements["2014"]["numCoreGE"]=3
requirements["2014"]["GECreditsLimit"]=45
requirements["2014"]["majorCredits"]=84
requirements["2014"]["exclusiveGECredits"]=6
requirements["2014"]["bsmCredits"]=18
requirements["2014"]["designSubjectsCredits"]=12
requirements["2014"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2014)

requirements["2015"]["totalCredits"]=140
requirements["2015"]["CoreGE"]=["토대기반","존재구축","소통융합","실천"] #General Education course for each area (one or more required)
requirements["2015"]["GECreditsLimit"]=45
requirements["2015"]["majorCredits"]=84
requirements["2015"]["MACHGE"]=4        #MACH liberal arts credits to be taken => 2 courses
requirements["2015"]["MACHPrac"]=2      #Total MACH practice credits to be taken => 2 courses
requirements["2015"]["exclusiveGECredits"]=6
requirements["2015"]["bsmCredits"]=18
requirements["2015"]["designSubjectsCredits"]=12
requirements["2015"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2015)

requirements["2016"]["totalCredits"]=140
requirements["2016"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2016"]["GECreditsLimit"]=45
requirements["2016"]["majorCredits"]=84
requirements["2016"]["MACHGE"]=4
requirements["2016"]["MACHPrac"]=2
requirements["2016"]["exclusiveGECredits"]=6
requirements["2016"]["bsmCredits"]=18
requirements["2016"]["designSubjectsCredits"]=12
requirements["2016"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2016)

requirements["2017"]["totalCredits"]=140
requirements["2017"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2017"]["GECreditsLimit"]=45
requirements["2017"]["majorCredits"]=84
requirements["2017"]["MACHGE"]=4
requirements["2017"]["MACHPrac"]=2
requirements["2017"]["exclusiveGECredits"]=6
requirements["2017"]["bsmCredits"]=18
requirements["2017"]["designSubjectsCredits"]=12
requirements["2017"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2017)

requirements["2018"]["totalCredits"]=140
requirements["2018"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2018"]["GECreditsLimit"]=45
requirements["2018"]["majorCredits"]=84
requirements["2018"]["MACHGE"]=4
requirements["2018"]["MACHPrac"]=2
requirements["2018"]["exclusiveGECredits"]=6
requirements["2018"]["bsmCredits"]=18
requirements["2018"]["designSubjectsCredits"]=12
requirements["2018"]["avgGrade"]=2.2
requirements["2018"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2018)

requirements["2019"]["totalCredits"]=140
requirements["2019"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2019"]["GECreditsLimit"]=45
requirements["2019"]["majorCredits"]=84
requirements["2019"]["MACHGE"]=2
#requirement_2019["MACHPrac"]=2
requirements["2019"]["exclusiveGECredits"]=6
requirements["2019"]["bsmCredits"]=18
requirements["2019"]["designSubjectsCredits"]=12
requirements["2019"]["avgGrade"]=2.2
requirements["2019"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2019)

requirements["2020"]["totalCredits"]=140
requirements["2020"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2020"]["GECreditsLimit"]=45
requirements["2020"]["majorCredits"]=84
requirements["2020"]["MACHGE"]=2
#requirement_2020["MACHPrac"]=2
requirements["2020"]["exclusiveGECredits"]=6
requirements["2020"]["bsmCredits"]=18
requirements["2020"]["designSubjectsCredits"]=12
requirements["2020"]["avgGrade"]=2.2
requirements["2020"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2020)

class UserData:
    assessed = False
    totalCredits = 0
    satisfyTotalCredits = False
    exclusiveGECredits = 0
    bsmCredits = 0
    numCoreGE = 0
    totalGECredits = 0
    majorCredits = 0
    designSubjectCredits = 0
    avgGrade = 0
    compulsoryNotTaken = []
    coreGE15 = {}
    coreGE15["토대기반"]=False
    coreGE15["존재구축"] = False
    coreGE15["소통융합"] = False
    coreGE15["실천"] = False
    coreGE16 = {}
    coreGE16["도전"] = False
    coreGE16["창의"] = False
    coreGE16["융합"] = False
    coreGE16["신뢰"] = False
    coreGE16["소통"] = False
    machGECredits = 0
    machPracCredits = 0

userData = UserData()

def certainFunction(argList):
    graduationAssessment(argList)
    #Do its logic

def getSubstitutableSubjects(target):
    tlist = []
    tlist.append(target)

    total_idx = 0
    current_idx = 0

    while True:
        if current_idx > total_idx:
            break

        tempList = Substitute.objects.filter(sub_id=tlist[current_idx])

        for j in range(0, len(tempList)):
            if tempList[j].course_id not in tlist:
                tlist.append(tempList[j].course_id)
                total_idx += 1

        current_idx += 1

    return tlist

def getSubstitutingSubjects(target):
    temp = []
    temp.append(target)
    total_idx = 0
    current_idx = 0

    while True:
        if current_idx > total_idx:
            break

        tempList = Substitute.objects.filter(course_id=temp[current_idx])

        for j in range(0, len(tempList)):
            if tempList[j].sub_id not in temp:
                temp.append(tempList[j].sub_id)
                total_idx += 1

        current_idx += 1

    return temp

def checkCompulsorySatisfied(year):
    #Do its logic
    global takeList
    global userData

    compulsoryBools = []
    length = len(requirements[year]["compulsorySubjects"])
    for i in range(0, length):
        compulsoryBools.append(False)

    for i in range(0, len(takeList)):
        tlist = getSubstitutableSubjects(takeList[i]["sbjt_no"])

        flag = True
        for j in range(0, len(tlist)):
            if flag:
                for k in range(0, length):
                    if tlist[j] == requirements[year]["compulsorySubjects"][k].course_id:
                        compulsoryBools[k] = True
                        flag = False
                        break

    notTaken = []
    for i in range(0, len(compulsoryBools)):
        if compulsoryBools[i] == False:
            temp = getSubstitutingSubjects(requirements[year]["compulsorySubjects"][i].course_id)

            notTaken.append(temp)

    userData.compulsoryNotTaken = notTaken

    return ""

def checkMinMaxRequire(year):
    #Do its logic
    global takeList
    global userData


    return ""

def checkGdRequire(year):
    checkCompulsorySatisfied(year)
    checkMinMaxRequire(year)




def graduationAssessment(argList):
    global userData
    global takeList

    ret = ""

    ID = argList[0]
    PW = argList[1]

    #TODO In chatscript need to take ! inputs also
    try:
        if userData.assessed == False:
            takeList, stNum = crawlers.getUserSubject(ID, PW)
            year = stNum[:4]
            checkGdRequire(year)
            userData.assessed = True
        else:
            return "Already Assessed"

    except Exception as e:
        error = e
        return "구현중"

    return "구현중"

def initFunclist():
    funclist.append(("graduationAssessment", graduationAssessment))
    return

#For debugging
def index(request):
    global userData
    takeList, stNum = crawlers.getUserSubject("yey6689", "para3150!")
    year = "2014"
    compulsoryBools = []
    length = len(requirements[year]["compulsorySubjects"])
    for i in range(0, length):
        compulsoryBools.append(False)

    for i in range(0, len(takeList)):
        tlist = getSubstitutableSubjects(takeList[i]["sbjt_no"])

        flag = True
        for j in range(0, len(tlist)):
            if flag:
                for k in range(0, length):
                    if tlist[j] == requirements[year]["compulsorySubjects"][k].course_id:
                        compulsoryBools[k] = True
                        flag = False
                        break

    notTaken = []
    for i in range(0, len(compulsoryBools)):
        if compulsoryBools[i] == False:
            temp = getSubstitutingSubjects(requirements[year]["compulsorySubjects"][i].course_id)

            notTaken.append(temp)

    userData.compulsoryNotTaken = notTaken
    return HttpResponse(userData.compulsoryNotTaken)


def api(request, message):

    HOST = 'ec2-3-21-126-101.us-east-2.compute.amazonaws.com'
    PORT = 1024

    # TODO port is changing every time user sent. So make the way to distinguish user without port number.
    ip = request.META.get('REMOTE_ADDR')
    port = request.META.get('REMOTE_PORT')

    name = ip

    if (message == 'start'):
        initFunclist()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind(('', 0))
        client_socket.connect((HOST, PORT))

        msg = ":reset"
        bot = "HARRY"

        data = name + chr(0) + bot + chr(0) + msg + chr(0);
        client_socket.send(data.encode())
        data = client_socket.recv(50000).decode()
        data = data.split("/")[1]
        client_socket.close()


        return JsonResponse({
            'message': 1,
            'content': data
        })



    bot = "HARRY"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('', 0))
    client_socket.connect((HOST, PORT))

    data = name + chr(0) + bot + chr(0) + message + chr(0);
    client_socket.send(data.encode());

    data = client_socket.recv(10000);
    print('bot : ', data.decode());
    data = data.decode()

    # Data Preprocessing
    tokens = data.split('/')
    type = tokens[0]

    # Find type
    if type == 'f' or type == 'F':
        fname = tokens[1]
        argList = tokens[2:]

        for func in funclist:
            if func[0] == fname:
                response = func[1](argList)

    elif type == 'u' or type == 'U':
        response = tokens[1]

    else:
        response = "Error"

    client_socket.close()
    return JsonResponse({
        'message': 1,
        'content': response
    })

