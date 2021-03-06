from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect, Http404
from django.http import JsonResponse
import datetime
import socket
import crawlers
from .models import Compulsory, Substitute, Subject
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
import random
import time

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
requirements["2010"]["majorBasicCredits"]=14
requirements["2010"]["majorCompulsoryCredits"]=12
requirements["2010"]["exclusiveGECredits"]=6     #Total credits for exclusive General Education courses
requirements["2010"]["bsmCredits"]=18            #Total credits for bsm courses
requirements["2010"]["designSubjectCredits"]=12 #Total credits required for design courses
requirements["2010"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2010) # List of compulsory subjects for the year
requirements["2010"]["others"]="졸업 인정제에 따라 영어 원어 강의 3과목 이수 또는 TOEIC 700점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격\n" + "졸업시험과 졸업 논문, 지도 교수와의 4회 이상의 상담"

requirements["2011"]["totalCredits"]=132
requirements["2011"]["numCoreGE"]=3
requirements["2011"]["GECreditsLimit"]=45
requirements["2011"]["majorCredits"]=66
requirements["2011"]["majorBasicCredits"]=14
requirements["2011"]["majorCompulsoryCredits"]=12
requirements["2011"]["exclusiveGECredits"]=6
requirements["2011"]["bsmCredits"]=18
requirements["2011"]["designSubjectCredits"]=12
requirements["2011"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2011)
requirements["2011"]["others"]="졸업 인정제에 따라 영어 원어 강의 3과목 이수 또는 TOEIC 700점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격\n" + "졸업시험과 졸업 논문 제출, 지도 교수와의 4회 이상의 상담"

requirements["2012"]["totalCredits"]=132
requirements["2012"]["numCoreGE"]=3
requirements["2012"]["GECreditsLimit"]=45
requirements["2012"]["majorCredits"]=66
requirements["2012"]["majorBasicCredits"]=14
requirements["2012"]["majorCompulsoryCredits"]=12
requirements["2012"]["exclusiveGECredits"]=6
requirements["2012"]["bsmCredits"]=18
requirements["2012"]["designSubjectCredits"]=12
requirements["2012"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2012)
requirements["2012"]["others"]="졸업 인정제에 따라 영어 원어 강의 3과목 이수 또는 TOEIC 700점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격과\n" + "한자 3급에 해당하는 자격이 필요,"+ "졸업시험과 졸업 논문 제출, 지도 교수와의 4회 이상의 상담"

requirements["2013"]["totalCredits"]=140
requirements["2013"]["numCoreGE"]=3
requirements["2013"]["GECreditsLimit"]=45
requirements["2013"]["majorCredits"]=84
requirements["2013"]["majorBasicCredits"]=14
requirements["2013"]["majorCompulsoryCredits"]=12
requirements["2013"]["exclusiveGECredits"]=6
requirements["2013"]["bsmCredits"]=18
requirements["2013"]["designSubjectCredits"]=12
requirements["2013"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2013)
requirements["2013"]["others"]="졸업 인정제에 따라 영어 원어 강의 3과목 이수 또는 TOEIC 700점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격과\n" + "한자 3급에 해당하는 자격이 필요,"+ "졸업논문 또는 그의 대체로 TOPCIT 시험 180점 이상, 졸업 시험 응시, 지도 교수와의 4회 이상의 상담"


requirements["2014"]["totalCredits"]=140
requirements["2014"]["numCoreGE"]=3
requirements["2014"]["GECreditsLimit"]=45
requirements["2014"]["majorCredits"]=84
requirements["2014"]["majorBasicCredits"]=14
requirements["2014"]["majorCompulsoryCredits"]=12
requirements["2014"]["exclusiveGECredits"]=6
requirements["2014"]["bsmCredits"]=18
requirements["2014"]["designSubjectCredits"]=12
requirements["2014"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2014)
requirements["2014"]["others"]="졸업 인정제에 따라 영어 원어 강의 3과목 이수 또는 TOEIC 700점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격과\n" + "한자 3급에 해당하는 자격이 필요,"+ "졸업논문 또는 그의 대체로 TOPCIT 시험 180점 이상, 졸업 시험 응시, 지도 교수와의 4회 이상의 상담"


requirements["2015"]["totalCredits"]=140
requirements["2015"]["CoreGE"]=["토대기반","존재구축","소통융합","실천"] #General Education course for each area (one or more required)
requirements["2015"]["GECreditsLimit"]=45
requirements["2015"]["majorCredits"]=84
requirements["2015"]["majorBasicCredits"]=14
requirements["2015"]["majorCompulsoryCredits"]=12
requirements["2015"]["MACHGE"]=4        #MACH liberal arts credits to be taken => 2 courses
requirements["2015"]["MACHPrac"]=2      #Total MACH practice credits to be taken => 2 courses
requirements["2015"]["exclusiveGECredits"]=6
requirements["2015"]["bsmCredits"]=18
requirements["2015"]["designSubjectCredits"]=12
requirements["2015"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2015)
requirements["2015"]["others"]="졸업 인정제에 따라 영어 원어 강의 3과목 이수 또는 TOEIC 700점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격과\n" + "한자 3급에 해당하는 자격이 필요,"+ "졸업논문 또는 그의 대체로 TOPCIT 시험 180점 이상, 졸업 시험 응시, 지도 교수와의 4회 이상의 상담"


requirements["2016"]["totalCredits"]=140
requirements["2016"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2016"]["GECreditsLimit"]=45
requirements["2016"]["majorCredits"]=84
requirements["2016"]["majorBasicCredits"]=14
requirements["2016"]["majorCompulsoryCredits"]=12
requirements["2016"]["MACHGE"]=4
requirements["2016"]["MACHPrac"]=2
requirements["2016"]["exclusiveGECredits"]=6
requirements["2016"]["bsmCredits"]=18
requirements["2016"]["designSubjectCredits"]=12
requirements["2016"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2016)
requirements["2016"]["others"]="졸업 인정제에 따라 영어 원어 강의 3과목 이수 또는 TOEIC 700점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격과\n" + "한자 3급에 해당하는 자격이 필요,"+ "졸업논문 또는 그의 대체로 TOPCIT 시험 점수 180점 이상, 졸업 시험 응시, 지도 교수와의 4회 이상의 상담"


requirements["2017"]["totalCredits"]=140
requirements["2017"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2017"]["GECreditsLimit"]=45
requirements["2017"]["majorCredits"]=84
requirements["2017"]["majorBasicCredits"]=14
requirements["2017"]["majorCompulsoryCredits"]=12
requirements["2017"]["MACHGE"]=4
requirements["2017"]["MACHPrac"]=2
requirements["2017"]["exclusiveGECredits"]=6
requirements["2017"]["bsmCredits"]=18
requirements["2017"]["designSubjectCredits"]=12
requirements["2017"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2017)
requirements["2017"]["others"]="졸업 인정제에 따라 영어 원어 강의 3과목 이수 또는 TOEIC 700점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격과\n" + "한자 3급에 해당하는 자격이 필요,"+ "졸업논문 또는 그의 대체로 TOPCIT 시험 점수 180점 이상, 졸업 시험 응시, 지도 교수와의 4회 이상의 상담"


requirements["2018"]["totalCredits"]=140
requirements["2018"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2018"]["GECreditsLimit"]=45
requirements["2018"]["majorCredits"]=84
requirements["2018"]["majorBasicCredits"]=14
requirements["2018"]["majorCompulsoryCredits"]=12
requirements["2018"]["MACHGE"]=4
requirements["2018"]["MACHPrac"]=2
requirements["2018"]["exclusiveGECredits"]=6
requirements["2018"]["bsmCredits"]=18
requirements["2018"]["designSubjectCredits"]=12
requirements["2018"]["avgGrade"]=2.2
requirements["2018"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2018)
requirements["2018"]["others"]="졸업 인정제에 더해 영어 원어 강의 3과목 이수 또는 TOEIC 750점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격 및 토스 5급 자격이나 전공 영어 강의 3과목 이수 그리고\n" + "한자 3급에 해당하는 자격이 필요,"+ "졸업논문 또는 그의 대체로 TOPCIT 시험 점수 180점 이상, 졸업 시험 응시, 지도 교수와의 4회 이상의 상담"


requirements["2019"]["totalCredits"]=140
requirements["2019"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2019"]["GECreditsLimit"]=45
requirements["2019"]["majorCredits"]=84
requirements["2019"]["majorBasicCredits"]=14
requirements["2019"]["majorCompulsoryCredits"]=12
requirements["2019"]["MACHGE"]=2
#requirement_2019["MACHPrac"]=2
requirements["2019"]["exclusiveGECredits"]=6
requirements["2019"]["bsmCredits"]=18
requirements["2019"]["designSubjectCredits"]=12
requirements["2019"]["avgGrade"]=2.2
requirements["2019"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2019)
requirements["2019"]["others"]="졸업 인정제에 더해 영어 원어 강의 3과목 이수 또는 TOEIC 750점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격 및 토스 5급 자격이나 전공 영어 강의 3과목 이수 그리고\n" + "한자 3급에 해당하는 자격이 필요,"+ "졸업논문 또는 그의 대체로 TOPCIT 시험 점수 270점 이상(TOPCIT 제출 필수), 졸업 시험 응시, 지도 교수와의 4회 이상의 상담"


requirements["2020"]["totalCredits"]=140
requirements["2020"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2020"]["GECreditsLimit"]=45
requirements["2020"]["majorCredits"]=84
requirements["2020"]["majorBasicCredits"]=14
requirements["2020"]["majorCompulsoryCredits"]=12
requirements["2020"]["MACHGE"]=2
#requirement_2020["MACHPrac"]=2
requirements["2020"]["exclusiveGECredits"]=6
requirements["2020"]["bsmCredits"]=18
requirements["2020"]["designSubjectCredits"]=12
requirements["2020"]["avgGrade"]=2.2
requirements["2020"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2020)
requirements["2020"]["others"]="졸업 인정제에 더해 영어 원어 강의 3과목 이수 또는 TOEIC 750점 이상 이나 그와 동등한 수준의 다른 영어 시험 자격 및 토스 5급 자격이나 전공 영어 강의 3과목 이수 그리고\n" + "한자 3급에 해당하는 자격이 필요,"+ "졸업논문 또는 그의 대체로 TOPCIT 시험 점수 270점 이상(TOPCIT 제출 필수), 졸업 시험 응시, 지도 교수와의 4회 이상의 상담"

majorCompulsoryList = []
majorCompulsoryList.append(["13601","알고리즘"])
majorCompulsoryList.append(["21427","컴퓨터구조"])
majorCompulsoryList.append(["22405","프로그래밍언어론"])
majorCompulsoryList.append(["40989","자료구조"])

funclist = []   #질문 대답 함수 리스트
test_flag = False

# Save {ID : UserData}
userGraduInfo = dict()
test_takeList = []

@csrf_exempt
def course(request):

    if request.method == 'POST':

        ret_course = None
        serial = None
        test = json.loads(request.body)

        if test['type'] == 'All':
            temp = test['data']
            if temp[4] == "":
                ret_course = Subject.objects.filter(course_year=temp[0], course_semester=temp[1], course_colgnm=temp[2], course_sustnm=temp[3])
            else:
                ret_course = Subject.objects.filter(course_year=temp[0], course_semester=temp[1], course_clssnm__contains=temp[4])
            serial = serializers.serialize('json', ret_course)

        else :
            ret_course = None
            data = test['data']
            mode = test['mode']
            if mode == "과목코드" :
                ret_course = Substitute.objects.filter(Q(course_id=data) | Q(sub_id=data)).distinct()
            else :
                ret_course = Substitute.objects.filter(Q(course_title__contains=data) | Q(sub_title__contains=data)).distinct()

            serial = serializers.serialize('json', ret_course)

    return HttpResponse(serial, content_type="text/json-comment-filtered")

            


@csrf_exempt
def delete(request):

    if request.method == 'POST':
        test = json.loads(request.body)

        if test['type'] == "All":
            for item in test['data']:
                Subject.objects.get(pk=item).delete()    

        else:
            for item in test['data']:
                Substitute.objects.get(pk=item).delete()        

    return HttpResponse("success")

@csrf_exempt
def add(request):

    if request.method == 'POST':

        bring = json.loads(request.body)
        
        if bring['type'] == 'All':
            item = bring['data']
            Subject(course_year = item[0],
                    course_semester = item[1],
                    course_colgnm = item[4],
                    course_sustnm = item[5],
                    course_pobjnm = item[3],
                    course_shyr = item[2],
                    course_profnm = item[7],
                    course_ltbdrm = item[8],
                    course_sbjtclss = item[9],
                    course_clssnm = item[6],
                    course_pnt = item[10],
                    course_remk = item[11]).save()

        else:
            item = bring['data']
            Substitute(course_id=item[0],
                    course_title=item[1],
                    sub_id=item[2],
                    sub_title=item[3]
            ).save()
            

    return HttpResponse('success')



class UserData:
    st_id = ""
    year = ""
    totalCredits = 0
    totalCreditsMore = 0
    totalCreditsSatisfied = False
    exclusiveGECredits = 0
    exclusiveGECreditsList = []
    exclusiveGECreditsMore = 0
    exclusiveGECreditsSatisfied = False
    bsmCredits = 0
    bsmCreditsList = []
    bsmCreditsMore = 0
    bsmCreditsSatisfied = False
    numCoreGE = 0
    numCoreGEList = []
    numCoreGEMore = 0
    numCoreGESatisfied = False
    totalGECredits = 0
    totalGECreditsList = []
    #totalGECreditsSatisfied = False
    majorCredits = 0
    majorCreditsList = []
    majorCreditsMore = 0
    majorCreditsSatisfied = False
    majorBasicCredits = 0
    majorBasicCreditsList = []
    majorBasicCreditsMore = 0
    majorBasicCreditsSatisfied = False
    majorCompulsoryCredits = 0
    majorCompulsoryCreditsList = []
    majorCompulsoryCreditsMore = 0
    majorCompulsoryCreditsSatisfied = False
    designSubjectCredits = 0
    designSubjectCreditsList = []
    designSubjectCreditsMore = 0
    designSubjectCreditsSatisfied = False
    avgGrade = 0
    pfCredits = 0
    avgGradeMore = 0
    avgGradeSatisfied = False
    compulsoryNotTaken = []
    takeListAdaptedRetaken = []
    compulsoryResult = ""
    compulsorySatisfied = False
    coreGE15 = {}
    coreGE15["토대기반"]=False
    coreGE15["존재구축"] = False
    coreGE15["소통융합"] = False
    coreGE15["실천"] = False
    coreGE15_satisfied = False
    coreGE16to20 = {}
    coreGE16to20["도전"] = False
    coreGE16to20["창의"] = False
    coreGE16to20["융합"] = False
    coreGE16to20["신뢰"] = False
    coreGE16to20["소통"] = False
    coreGE16to20_satisfied = False
    machGECredits = 0
    machGECreditsList = []
    machGECreditsMore = 0
    machGECreditsSatisfied = False
    machPracCredits = 0
    machPracCreditsList = []
    machPracCreditsMore = 0
    machPracCreditsSatisfied = False




def certainFunction(argList):
    graduationAssessment(argList)
    #Do its logic

# target이 대체 가능한 과목들 리턴
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

#target을 대체 가능한 과목들 리턴
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

#재수강인 과목 판단 후 재수강 반영한 수강 과목 리스트에 추가/수정
def checkNotRetaken(target, index, takeList, takeListAdaptedRetaken, subsFoundlist):
    func_flag = True

    #tareget의 대체 과목 파악
    substitute = getSubstitutableSubjects(target)

    # target과 같은 과목 코드로 대체 과목을 찾은 적이 있다면 이 target은 재수강한 과목이다
    if substitute not in subsFoundlist:
        subsFoundlist.append(substitute)
    else:
        #기존에 있는 재수강 반영 수강 과목 리스트에 target의 내용으로 덮어씌우기
        idx = 0
        for i in range(0, len(takeListAdaptedRetaken)):
            if takeListAdaptedRetaken[i]["sbjt_no"] == target:
                idx = i
                break

        takeListAdaptedRetaken[idx] = takeList[index]
        func_flag = False



    # 대체과목리스트에 있는 항목이 수강한 과목 중에 있다면? => target은 재수강
    # 같은 과목 코드 재수강 ->
    for_flag = True
    for i in range(1, len(substitute)):
        if for_flag:
            for j in range(0, len(takeList)):
                if substitute[i] == takeList[j]["sbjt_no"]:
                    idx = 0
                    for k in range(0, len(takeListAdaptedRetaken)):
                        if takeListAdaptedRetaken[k]["sbjt_no"] == substitute[i]:
                            idx = k
                            break
                    try:
                        takeListAdaptedRetaken[idx] = takeList[index]
                    except Exception as e:
                        str(e)

                    func_flag = False
                    for_flag = False
                    break

    if func_flag == True and takeList[index] not in takeListAdaptedRetaken:
        takeListAdaptedRetaken.append(takeList[index])

    return func_flag

def checkCompulsorySatisfied(year, userData, takeList):
    #Do its logic

    compulsoryBools = []
    length = len(requirements[year]["compulsorySubjects"])
    for i in range(0, length):
        compulsoryBools.append(False)

    for i in range(0, len(takeList)):
        if takeList[i]["g_grd"] != "F ":
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

    if len(userData.compulsoryNotTaken) == 0:
        userData.compulsorySatisfied = True
    else:
        st = ""
        for i in range(0, len(userData.compulsoryNotTaken)):
            sbjt = Subject.objects.filter(course_sbjtclss__startswith=userData.compulsoryNotTaken[i][0])
            
            if i == len(userData.compulsoryNotTaken) - 1:
                st += sbjt[0].course_clssnm
            else:
                st += sbjt[0].course_clssnm + "\n"

        userData.compulsoryResult += "필수 과목 중 아직 수강하지 않은 과목이 있습니다.\n 수강하지 않은 필수 과목 :\n" + st + "\n"
    return ""

def checkMinMaxRequire(year, userData, takeList):

    if int(year) <= 2014:
        checkLte2014(year, userData, takeList)
    else:
        checkGt2014(year, userData, takeList)

    return ""



def checkGt2014(year, userData, takeList):
    st = ""  # 분석 결과
    takeListAdaptedRetaken = []
    subsFoundlist = []

    # ------요건 분석 로직 ------------
    for i in range(0, len(takeList)):
        if takeList[i]["g_grd"] != 'F ':
            if (checkNotRetaken(takeList[i]["sbjt_no"], i, takeList, takeListAdaptedRetaken, subsFoundlist)):
                sInfo = Subject.objects.filter(course_sbjtclss__startswith=takeList[i]["sbjt_no"],
                                               course_year=takeList[i]["re_year"])

                # 핵심 교양 종류 파악
                if year == "2015":
                    for j in range(0, len(sInfo)):
                        if "토대기반" in sInfo[j].course_remk:
                            userData.coreGE15["토대기반"]=True
                        if "존재구축" in sInfo[j].course_remk:
                            userData.coreGE15["존재구축"]=True
                        if "소통융합" in sInfo[j].course_remk:
                            userData.coreGE15["소통융합"]=True
                        if "실천" in sInfo[j].course_remk:
                            userData.coreGE15["실천"]=True

                else:
                    for j in range(0, len(sInfo)):
                        if "도전" in sInfo[j].course_remk:
                            userData.coreGE16to20["도전"]=True
                        if "창의" in sInfo[j].course_remk:
                            userData.coreGE16to20["창의"]=True
                        if "융합" in sInfo[j].course_remk:
                            userData.coreGE16to20["융합"]=True
                        if "신뢰" in sInfo[j].course_remk:
                            userData.coreGE16to20["신뢰"]=True
                        if "소통" in sInfo[j].course_remk:
                            userData.coreGE16to20["소통"]=True


                # 교양 학점 더하기 및 들은 교양 과목 리스트에 추가
                for j in range(0, len(sInfo)):
                    if "교양" in sInfo[j].course_pobjnm:
                        userData.totalGECredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.totalGECreditsList.append(takeList[i])
                        break

                # 전공 학점 더하기 및 들은 전공 과목 리스트에 추가
                for j in range(0, len(sInfo)):
                    if "전공" in sInfo[j].course_pobjnm and "기초" not in sInfo[j].course_pobjnm:
                        userData.majorCredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.majorCreditsList.append(takeList[i])
                        break

                # 전공기초 학점 더하기
                for j in range(0, len(sInfo)):
                    if "전공기초" in sInfo[j].course_pobjnm:
                        userData.majorBasicCredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.majorBasicCreditsList.append(takeList[i])
                        break

                # 전공필수 학점 더하기
                for j in range(0, len(sInfo)):
                    if "전공필수" in sInfo[j].course_pobjnm:
                        userData.majorCompulsoryCredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.majorCompulsoryCreditsList.append(takeList[i])
                        break

                # 총 학점 더하기
                userData.totalCredits += int(takeList[i]["acq_pnt"])

                # 전문교양 학점 더하기
                for j in range(0, len(sInfo)):
                    if "전문교양" in sInfo[j].course_remk and ("컴퓨터" in sInfo[j].course_remk or "소프트" in sInfo[j].course_remk or "ICT" in sInfo[j].course_remk):
                        # st += sInfo[j].course_clssnm + "   "
                        # st += sInfo[j].course_remk + "   "
                        userData.exclusiveGECredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.exclusiveGECreditsList.append(takeList[i])
                        break

                # BSM 학점 더하기
                for j in range(0, len(sInfo)):
                    if "BSM" in sInfo[j].course_remk:
                        userData.bsmCredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.bsmCreditsList.append(takeList[i])
                        break

                # 설계 학점 더하기
                for j in range(0, len(sInfo)):
                    if "설계" in sInfo[j].course_remk:  # and "컴퓨터" in sInfo[j].course_remk:
                        # st += sInfo[j].course_clssnm + "   "
                        # st += sInfo[j].course_remk + "   "
                        string = sInfo[j].course_remk
                        credit = ""
                        for k in range(0, len(string)):
                            if string[k] == "설" and string[k + 1] == "계":
                                credit += string[k + 2]
                                break

                        userData.designSubjectCredits += int(credit)
                        userData.designSubjectCreditsList.append((takeList[i], credit))

                        break

                # MACH 교양 학점 더하기
                for j in range(0, len(sInfo)):
                    if "MACH교양" in sInfo[j].course_remk:
                        userData.machGECredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.machGECreditsList.append(takeList[i])
                        break

                # MACH 실습 학점 더하기기
                for j in range(0, len(sInfo)):
                    if "MACH실습" in sInfo[j].course_remk:
                        userData.machPracCredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.machPracCreditsList.append(takeList[i])
                        break

    userData.takeListAdaptedRetaken = takeListAdaptedRetaken
    for i in range(0, len(userData.takeListAdaptedRetaken)):
        # 평학 계산
        try:
            if takeListAdaptedRetaken[i]["grd_mak"] != "P/F":
                userData.avgGrade += float(takeListAdaptedRetaken[i]["acq_pnt"]) * float(
                    takeListAdaptedRetaken[i]["grd_mak"])
            else:
                userData.pfCredits += takeListAdaptedRetaken[i]["acq_pnt"]
        except Exception as e:
            st += str(e)
    # ------ 요견 판별 로직 ----------

    # 핵심 교양 각 영역별 만족 판별
    if year == "2015":
        if userData.coreGE15["토대기반"] == True and userData.coreGE15["존재구축"] == True and userData.coreGE15["소통융합"] == True and userData.coreGE15["실천"] == True:
            userData.coreGE15_satisfied=True
        else:
            userData.coreGE15_satisfied=False
    else:
        if userData.coreGE16to20["도전"] == True and userData.coreGE16to20["창의"] == True and userData.coreGE16to20[
"융합"] == True and userData.coreGE16to20["신뢰"] == True and userData.coreGE16to20["소통"]:
            userData.coreGE16to20_satisfied = True
        else:
            userData.coreGE16to20 = False

    # 총 교양 과목 학점이 45이상 이면 45헉점만 인정
    diff = 0
    if userData.totalGECredits > requirements[year]["GECreditsLimit"]:
        temp = userData.totalGECredits
        diff = temp - requirements[year]["GECreditsLimit"]
        userData.totalGECredits = requirements[year]["GECreditsLimit"]

    # 전공 학점 만족 판별
    if userData.majorCredits >= requirements[year]["majorCredits"]:
        userData.majorCreditsSatisfied = True
    else:
        userData.majorCreditsMore = requirements[year]["majorCredits"] - userData.majorCredits
        #st += "전공 과목 불만족\n 전공 과목 학점을 " + str(requirements[year]["majorCredits"] - userData.majorCredits) + "만큼 더 취득하셔야 합니다."

    # 전공 기초 학점 만족 판별
    if userData.majorBasicCredits >= requirements[year]["majorBasicCredits"]:
        userData.majorBasicCreditsSatisfied = True
    else:
        userData.majorBasicCreditsMore = requirements[year]["majorBasicCredits"] - userData.majorBasicCredits
        #st += "전공 기초 과목 불만족\n 전공 기초 과목 학점을 " + str(requirements[year]["majorBasicCredits"] - userData.majorBasicCredits) + "만큼 더 취득하셔야 합니다."

    # 전공 필수 학저 만족 판별별
    if userData.majorCompulsoryCredits >= requirements[year]["majorCompulsoryCredits"]:
        userData.majorCompulsoryCreditsSatisfied = True
    else:
        userData.majorCompulsoryCreditsMore = requirements[year]["majorCompulsoryCredits"] - userData.majorCompulsoryCredits
        #st += "전공 필수 과목 불만족\n 전공 필수 과목 학점을 " + str(requirements[year]["majorCompulsoryCredits"] - userData.majorCompulsoryCredits) + "만큼 더 취득하셔야 합니다."

    # 총 학점 만족 판별
    userData.totalCredits = userData.totalCredits - diff
    if userData.totalCredits >= requirements[year]["totalCredits"]:
        userData.totalCreditsSatisfied = True
    else:
        userData.totalCreditsMore = requirements[year]["totalCredits"] - userData.totalCredits
        #st += "총 학점 불만족\n 총 학점을 " + str(requirements[year]["totalCredits"] - userData.totalCredits) + "만큼 더 취득하셔야 합니다."

    # 평균 학점 계산
    try:
        avg = userData.avgGrade / (userData.totalCredits - userData.pfCredits)
        userData.avgGrade = round(avg, 2)
        print(userData.totalCredits)
    except Exception as e:
        print(userData.totalCredits)

    if int(year) >= 2018:
        if userData.avgGrade >= requirements[year]["avgGrade"]:
            userData.avgGradeSatisfied = True
        else:
            userData.avgGradeMore = requirements[year]["avgGrade"] - userData.avgGrade

    # 전문 교양 학점 만족 판별
    if userData.exclusiveGECredits >= requirements[year]["exclusiveGECredits"]:
        userData.exclusiveGECreditsSatisfied = True
    else:
        userData.exclusiveGECreditsMore = requirements[year]["exclusiveGECredits"] - userData.exclusiveGECredits
        #st += "전문 교양 학점 불만족\n 전문 교양 과목 학점을 " + str(requirements[year]["exclusiveGECredits"] - userData.exclusiveGECredits) + "만큼 더 취득하셔야 합니다."

    # BSM 학점 만족 판별
    if userData.bsmCredits >= requirements[year]["bsmCredits"]:
        userData.bsmCreditsSatisfied = True
    else:
        userData.bsmCreditsMore = requirements[year]["bsmCredits"] - userData.bsmCredits;
        #st += "BSM 학점 불만족\n BSM 과목 학점을 " + str(requirements[year]["bsmCredits"] - userData.bsmCredits) + "만큼 더 취득하셔야 합니다."

    # 설계 학점 만족 판별
    if userData.designSubjectCredits >= requirements[year]["designSubjectCredits"]:
        userData.designSubjectCreditsSatisfied = True
    else:
        userData.designSubjectCreditsMore = requirements[year]["designSubjectCredits"] - userData.designSubjectCredits
        #st += "설계 학점 불만족\n 설계 과목 학점을 " + str(requirements[year]["designSubjectCredits"] - userData.designSubjectCredits) + "만큼 더 취득하셔야 합니다."

    #MACH 교양 학점 만족 판별
    if userData.machGECredits >= requirements[year]["MACHGE"]:
        userData.machGECreditsSatisfied = True
    else:
        userData.machGECreditsMore = requirements[year]["MACHGE"] - userData.machGECredits

    if int(year) >= 2015 and int(year) <= 2018:
        #MACH 실습 학점 만족 판별
        if userData.machPracCredits >= requirements[year]["MACHPrac"]:
            userData.machPracCreditsSatisfied = True
        else:
            userData.machPracCreditsMore = requirements[year]["MACHPrac"] - userData.machPracCredits

    return ""


def checkLte2014(year, userData, takeList):
    st = ""  # 분석 결과
    takeListAdaptedRetaken = []
    subsFoundlist = []

    # ------요건 분석 로직 ------------
    for i in range(0, len(takeList)):
        if takeList[i]["g_grd"] != 'F ':
            if (checkNotRetaken(takeList[i]["sbjt_no"], i, takeList, takeListAdaptedRetaken, subsFoundlist)):
                sInfo = Subject.objects.filter(course_sbjtclss__startswith=takeList[i]["sbjt_no"],
                                                   course_year=takeList[i]["re_year"])

                # 핵심 교양 갯수 더하기
                for j in range(0, len(sInfo)):
                    if "핵심" in sInfo[j].course_remk and "컴퓨터" in sInfo[j].course_remk:
                        userData.numCoreGE += 1
                        userData.numCoreGEList.append(takeList[i])
                        break

                # 교양 학점 더하기 및 들은 교양 과목 리스트에 추가
                for j in range(0, len(sInfo)):
                    if "교양" in sInfo[j].course_pobjnm:
                        userData.totalGECredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.totalGECreditsList.append(takeList[i])
                        break

                # 전공 학점 더하기 및 들은 전공 과목 리스트에 추가
                for j in range(0, len(sInfo)):
                    if "전공" in sInfo[j].course_pobjnm and "기초" not in sInfo[j].course_pobjnm:
                        userData.majorCredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.majorCreditsList.append(takeList[i])
                        break

                # 전공기초 학점 더하기
                for j in range(0, len(sInfo)):
                    if "전공기초" in sInfo[j].course_pobjnm:
                        userData.majorBasicCredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.majorBasicCreditsList.append(takeList[i])
                        break

                # 전공필수 학점 더하기
                for j in range(0, len(sInfo)):
                    if "전공필수" in sInfo[j].course_pobjnm:
                        userData.majorCompulsoryCredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.majorCompulsoryCreditsList.append(takeList[i])
                        break

                # 총 학점 더하기
                userData.totalCredits += int(takeList[i]["acq_pnt"])


                # 전문교양 학점 더하기
                for j in range(0, len(sInfo)):
                    if "전문교양" in sInfo[j].course_remk and "컴퓨터" in sInfo[j].course_remk:
                        # st += sInfo[j].course_clssnm + "   "
                        # st += sInfo[j].course_remk + "   "
                        userData.exclusiveGECredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.exclusiveGECreditsList.append(takeList[i])
                        break

                # BSM 학점 더하기
                for j in range(0, len(sInfo)):
                    if "BSM" in sInfo[j].course_remk:
                        userData.bsmCredits += int(sInfo[j].course_pnt.split("-")[0])
                        userData.bsmCreditsList.append(takeList[i])
                        break

                # 설계 학점 더하기
                for j in range(0, len(sInfo)):
                    if "설계" in sInfo[j].course_remk:  # and "컴퓨터" in sInfo[j].course_remk:
                        # st += sInfo[j].course_clssnm + "   "
                        # st += sInfo[j].course_remk + "   "
                        string = sInfo[j].course_remk
                        credit = ""
                        for k in range(0, len(string)):
                            if string[k] == "설" and string[k + 1] == "계":
                                credit += string[k + 2]
                                break

                        userData.designSubjectCredits += int(credit)
                        userData.designSubjectCreditsList.append((takeList[i], credit))

                        break

    userData.takeListAdaptedRetaken = takeListAdaptedRetaken
    for i in range(0, len(userData.takeListAdaptedRetaken)):
        # 평학 계산
        try:
            if takeListAdaptedRetaken[i]["grd_mak"] != "P/F":
                userData.avgGrade += float(takeListAdaptedRetaken[i]["acq_pnt"]) * float(takeListAdaptedRetaken[i]["grd_mak"])
            else:
                userData.pfCredits += takeListAdaptedRetaken[i]["acq_pnt"]
        except Exception as e:
            st += str(e)
    # ------ 요견 판별 로직 ----------

    # 핵심 교양 학점 만족 판별
    if userData.numCoreGE >= requirements[year]["numCoreGE"]:
        userData.numCoreGESatisfied = True
    else:
        userData.numCoreGEMore = requirements[year]["numCoreGE"] - userData.numCoreGE
        #st += "핵심 교양 불만족\n 핵심 교양 과목을 " + str(equirements[year]["numCoreGE"] - userData.numCoreGE) + "개 이상 더 들으셔야 합니다."

    # 총 교양 과목 학점이 45이상 이면 45헉점만 인정
    diff = 0
    if userData.totalGECredits > requirements[year]["GECreditsLimit"]:
        temp = userData.totalGECredits
        diff = temp - requirements[year]["GECreditsLimit"]
        userData.totalGECredits = requirements[year]["GECreditsLimit"]

    # 전공 학점 만족 판별
    if userData.majorCredits >= requirements[year]["majorCredits"]:
        userData.majorCreditsSatisfied = True
    else:
        userData.majorCreditsMore = requirements[year]["majorCredits"] - userData.majorCredits
        #st += "전공 과목 불만족\n 전공 과목 학점을 " + str(requirements[year]["majorCredits"] - userData.majorCredits) + "만큼 더 취득하셔야 합니다."

    # 전공 기초 학점 만족 판별
    if userData.majorBasicCredits >= requirements[year]["majorBasicCredits"]:
        userData.majorBasicCreditsSatisfied = True
    else:
        userData.majorBasicCreditsMore = requirements[year]["majorBasicCredits"] - userData.majorBasicCredits
        #st += "전공 기초 과목 불만족\n 전공 기초 과목 학점을 " + str(requirements[year]["majorBasicCredits"] - userData.majorBasicCredits) + "만큼 더 취득하셔야 합니다."

    if userData.majorCompulsoryCredits >= requirements[year]["majorCompulsoryCredits"]:
        userData.majorCompulsoryCreditsSatisfied = True
    else:
        userData.majorCompulsoryCreditsMore = requirements[year]["majorCompulsoryCredits"] - userData.majorCompulsoryCredits
        #st += "전공 필수 과목 불만족\n 전공 필수 과목 학점을 " + str(requirements[year]["majorCompulsoryCredits"] - userData.majorCompulsoryCredits) + "만큼 더 취득하셔야 합니다."

    # 총 학점 만족 판별
    userData.totalCredits = userData.totalCredits - diff
    if userData.totalCredits>= requirements[year]["totalCredits"]:
        userData.totalCreditsSatisfied = True
    else:
        userData.totalCreditsMore = requirements[year]["totalCredits"] - (userData.totalCredits - diff)
        #st += "총 학점 불만족\n 총 학점을 " + str(requirements[year]["totalCredits"] - userData.totalCredits) + "만큼 더 취득하셔야 합니다."

    # 평균 학점 계산
    avg = userData.avgGrade / (userData.totalCredits - userData.pfCredits)
    userData.avgGrade = round(avg, 2)

    # 전문 교양 학점 만족 판별
    if userData.exclusiveGECredits >= requirements[year]["exclusiveGECredits"]:
        userData.exclusiveGECreditsSatisfied = True
    else:
        userData.exclusiveGECreditsMore = requirements[year]["exclusiveGECredits"] - userData.exclusiveGECredits
        #st += "전문 교양 학점 불만족\n 전문 교양 과목 학점을 " + str(requirements[year]["exclusiveGECredits"] - userData.exclusiveGECredits) + "만큼 더 취득하셔야 합니다."

    # BSM 학점 만족 판별
    if userData.bsmCredits >= requirements[year]["bsmCredits"]:
        userData.bsmCreditsSatisfied = True
    else:
        userData.bsmCreditsMore = requirements[year]["bsmCredits"] - userData.bsmCredits
        #st += "BSM 학점 불만족\n BSM 과목 학점을 " + str(requirements[year]["bsmCredits"] - userData.bsmCredits) + "만큼 더 취득하셔야 합니다."

    # 설계 학점 만족 판별
    if userData.designSubjectCredits >= requirements[year]["designSubjectCredits"]:
        userData.designSubjectCreditsSatisfied = True
    else:
        userData.designSubjectCreditsMore = requirements[year]["designSubjectCredits"] - userData.designSubjectCredits
        #st += "설계 학점 불만족\n 설계 과목 학점을 " + str(requirements[year]["designSubjectCredits"] - userData.designSubjectCredits) + "만큼 더 취득하셔야 합니다."


    return st




# check_funclist = [] #년도별 요건 분석 함수 리스트
# #check_funclist.append(("2013",check2013))
# check_funclist.append(("lte2014",checkLte2014))


def checkGdRequire(year, userData, takeList):
    checkCompulsorySatisfied(year, userData, takeList)
    checkMinMaxRequire(year, userData, takeList)




#TODO Answer whole things
def graduationAvailability(argList):
    graduationAssessment(argList)
    global userGraduInfo

    #TODO 사용자 고유 번호에 맞는 ID 가져와야 함
    ID = argList[0]

    # 필수 과목 메세지
    st = userGraduInfo[ID].compulsoryResult

    # 총 학점  언급
    if userGraduInfo[ID].totalCreditsSatisfied == False:
        st += "총 학점 조건을 만족하시지 못합니다.\n 총 학점을 " + str(userGraduInfo[ID].totalCreditsMore) + "만큼 더 취득하셔야 합니다.\n"

    # 전문 교양 학점 언급
    if userGraduInfo[ID].exclusiveGECreditsSatisfied == False:
        st += "전문 교양 학점 조건을 만족하시지 못합니다.\n 전문 교양 학점을 " + str(userGraduInfo[ID].exclusiveGECreditsMore) + "만큼 더 취득하셔야 합니다.\n"

    # BSM 학점 언급
    if userGraduInfo[ID].bsmCreditsSatisfied == False:
        st += "BSM 학점 조건을 만족하시지 못합니다.\n BSM 학점을 " + str(userGraduInfo[ID].bsmCreditsMore) + "만큼 더 취득하셔야 합니다.\n"

    # 핵심 교양 학점 언급
    if int(userGraduInfo[ID].year) <= 2014:
        if userGraduInfo[ID].numCoreGESatisfied == False:
            st += "핵심 교양 학점 조건을 만족하시지 못합니다.\n 핵심 교양 과목을 " + str(userGraduInfo[ID].numCoreGEMore) + "만큼 더 수강하셔야 합니다.\n"

    elif int(userGraduInfo[ID].year) == 2015:
        if userGraduInfo[ID].coreGE15_satisfied == False:
            st += "핵심 교양 학점 조건을 만족하시지 못합니다.\n "
            if userGraduInfo[ID].coreGE15["토대기반"] == False:
                st += "[토대기반] "
            if userGraduInfo[ID].coreGE15["존재구축"] == False:
                st += "[존재구축] "
            if userGraduInfo[ID].coreGE15["소통융합"] == False:
                st += "[소통융합] "
            if userGraduInfo[ID].coreGE15["실천"] == False:
                st += "[실천] "
            st += "영역의 교양과목을 각각 1과목 이상 수강하셔야 합니다.\n"

    else:
        if userGraduInfo[ID].coreGE16to20_satisfied == False:
            st += "핵심 교양 학점 조건을 만족하시지 못합니다.\n "
            if userGraduInfo[ID].coreGE16to20["도전"] == False:
                st += "[도전] "
            if userGraduInfo[ID].coreGE16to20["창의"] == False:
                st += "[창의] "
            if userGraduInfo[ID].coreGE16to20["융합"] == False:
                st += "[융합] "
            if userGraduInfo[ID].coreGE16to20["신뢰"] == False:
                st += "[신뢰] "
            if userGraduInfo[ID].coreGE16to20["소통"] == False:
                st += "[소통] "
            st += "영역의 교양과목을 각각 1과목 이상 수강하셔야 합니다.\n"

    # 전공 학점 언급
    if userGraduInfo[ID].majorCreditsSatisfied == False:
        st += "전공 학점 조건을 만족하시지 못합니다.\n 전공 학점을 " + str(userGraduInfo[ID].majorCreditsMore) + "만큼 더 취득하셔야 합니다.\n"

    # 전공기초 학점 언급
    if userGraduInfo[ID].majorBasicCreditsSatisfied == False:
        st += "전공기초 학점 조건을 만족하시지 못합니다.\n 전공기초 학점을 " + str(userGraduInfo[ID].majorBasicCreditsMore) + "만큼 더 취득하셔야 합니다.\n"

    # 전공필수 학점 언급
    if userGraduInfo[ID].majorBasicCreditsSatisfied == False:
        st += "전공필수 학점 조건을 만족하시지 못합니다.\n 전공필수 학점을 " + str(userGraduInfo[ID].majorCompulsoryCreditsMore) + "만큼 더 취득하셔야 합니다.\n"

    # 설계 학점 언급
    if userGraduInfo[ID].designSubjectCreditsSatisfied == False:
        st += "설계 학점 조건을 만족하시지 못합니다.\n 설계 학점을 " + str(
            userGraduInfo[ID].designSubjectCreditsMore) + "만큼 더 취득하셔야 합니다.\n(설계 학점은 설계 과목의 학점이 아니고 설계 과목마다 정해져 있습니다)\n"

    # 평점 언급
    if int(userGraduInfo[ID].year) >= 2018:
        if userGraduInfo[ID].avgGradeSatisfied == False:
            st += "평균 학점 조건을 만족하시지 못합니다.\n 평균 학점을 " + str(userGraduInfo[ID].avgGradeMore) + "만큼 더 올리셔야 합니다.\n"

    # MACH 교양 실습 언급
    if int(userGraduInfo[ID].year) >= 2015:
        if userGraduInfo[ID].machGECreditsSatisfied == False:
            st += "MACH 교양 학점 조건을 만족하시지 못합니다.\n MACH 교양 학점을 " + str(userGraduInfo[ID].machGECreditsMore) + "만큼 더 취득하셔야 합니다.\n"

        if userGraduInfo[ID].machPracCreditsSatisfied == False:
            st += "MACH 실습 학점 조건을 만족하시지 못합니다.\n MACH 실습 학점을 " + str(userGraduInfo[ID].machPracCreditsMore) + "만큼 더 취득하셔야 합니다.\n"

    st += "이에 더해,\n"
    st += requirements[userGraduInfo[ID].year]["others"] + "\n"
    st += "상기의 조건들을 만족하시면 졸업이 가능하십니다.\n"
    return st

#TODO Answer how more credits achieved
def moreTotCredit(argList):
    graduationAssessment(argList)
    global userGraduInfo

    # TODO 사용자 고유 번호에 맞는 ID 가져와야 함
    ID = argList[0]
    st = ""

    st += "수강하셔야 하는 총 학점은 " + str(requirements[userGraduInfo[ID].year]["totalCredits"]) + "입니다.\n"
    st += "현재 " + str(userGraduInfo[ID].totalCredits) + "학점을 수강하셨고 앞으로" + str(userGraduInfo[ID].totalCreditsMore) + "학점을 더 수강하셔야 합니다.\n"
    st += "수강하신 교양 과목 학점은 " + str(userGraduInfo[ID].totalGECredits) + " 학점, 전공 과목 학점은 " + str(userGraduInfo[ID].majorCredits) + "학점, 전공기초 과목 학점은 " + str(userGraduInfo[ID].majorBasicCredits) + " 학점, 자유선택 과목 학점은 " + str(userGraduInfo[ID].totalCredits - userGraduInfo[ID].totalGECredits - userGraduInfo[ID].majorCredits - userGraduInfo[ID].majorBasicCredits) + " 입니다.\n"
    return st


#TODO
def moreMajorCredit(argList):
    graduationAssessment(argList)
    global userGraduInfo

    # TODO 사용자 고유 번호에 맞는 ID 가져와야 함
    ID = argList[0]
    st = ""

    st += "수강하셔야 하는 총 전공 학점은 " + str(requirements[userGraduInfo[ID].year]["majorCredits"]) + "입니다.\n"
    st += "현재 " + str(userGraduInfo[ID].majorCredits) + "학점을 수강하셨고 앞으로 " + str(
        userGraduInfo[ID].majorCreditsMore) + "학점을 더 수강하셔야 합니다.\n"
    st += "수강하신 전공기초 과목 학점은 " + str(userGraduInfo[ID].majorBasicCredits) + " 학점, 전공필수 과목 학점은 " + str(userGraduInfo[ID].majorCompulsoryCredits) + " 학점 입니다.\n"

    return st

#TODO
def askCompul(argList):
    graduationAssessment(argList)

    ID = argList[0]
    st = ""

    st += "수강해야 할 필수 과목은 \n"
    for i in range(0, len(requirements[userGraduInfo[ID].year]["compulsorySubjects"])):
        st += requirements[userGraduInfo[ID].year]["compulsorySubjects"][i].course_title + "\n"

    st += " 이며 이 중 전공필수 과목은 \n"
    for i in range(0, len(majorCompulsoryList)):
        st += majorCompulsoryList[i][1] + "\n"
        

    st += " 입니다.\n\n"
    if len(userGraduInfo[ID].compulsoryNotTaken) == 0:
        st += " 모든 필수 과목을 다 수강하셨습니다.\n"
    else:
        majorCompul = []
        for i in range(0, len(userGraduInfo[ID].compulsoryNotTaken)):
            if True:
                temp = Compulsory.objects.filter(course_id=userGraduInfo[ID].compulsoryNotTaken[i][0])
                st += temp[0].course_title + "\n"
                for j in range(0, len(majorCompulsoryList)):
                    if userGraduInfo[ID].compulsoryNotTaken[i][0] == majorCompulsoryList[j][0]:
                        majorCompul.append(majorCompulsoryList[j][1])

        st += " 과목을 수강하지 않으셨습니다. \n이 중 전공필수 과목은 "
        if len(majorCompul) == 0:
            st += "없습니다."
        else:
            for i in range(len(majorCompul)):
                if True:
                    st += majorCompul[i] + "\n"
            st += "입니다."
    return st
#TODO
def askConsult(argList):
    graduationAssessment(argList)

    ID = argList[0]
    st = requirements[userGraduInfo[ID].year]["others"] +"\n"
    st += "위의 조항에 따라 지도 교수와의 4회 이상의 상담이 필요합니다."

    return st
#TODO
def askGradPaper(argList):
    graduationAssessment(argList)

    ID = argList[0]
    if int(userGraduInfo[ID].year) >= 2013:
        st = requirements[userGraduInfo[ID].year]["others"] + "\n"
        st += "위의 조항에 따라 TOPCIT 시험에서 일정 점수 이상을 취득하시면 졸업 논문 대체가 가능합니다.\n"
    else:
        st = requirements[userGraduInfo[ID].year]["others"] + "\n"
        st = "위의 조항에 따라 졸업 논문을 제출하셔야 합니다.\n"

    return st

#TODO
def askChinese(argList):
    graduationAssessment(argList)

    ID = argList[0]
    if int(userGraduInfo[ID].year) >= 2012:
        st = requirements[userGraduInfo[ID].year]["others"] + "\n"
        st += "위의 조항에 따라 한자 3급에 해당하는 자격이 필요합니다.\n"
    else:
        st = "한자 자격증을 취득하실 필요가 없습니다."

    return st
    

#TODO
def askEnglish(argList):
    graduationAssessment(argList)

    ID = argList[0]
    st = requirements[userGraduInfo[ID].year]["others"] + "\n"
    st += "위의 조항에 따른 영어 시험 관련 성적이나 특정 영어 과목 수강이 필요합니다.\n"

    return st

#TODO
def askTopcit(argList):
    graduationAssessment(argList)

    ID = argList[0]
    if int(userGraduInfo[ID].year) >= 2013:
        st = requirements[userGraduInfo[ID].year]["others"] + "\n"
        st += "위의 조항에 따라 TOPCIT 시험에서 일정 점수 이상을 취득하셔야 졸업 논문이 대체 가능합니다.\n"
    else:
        st = "TOPCIT으로 졸업 논문 대체를 하실 수 없습니다.\n 졸업 논문을 제출하셔야 합니다.\n"

    return st

#TODO
def askGradTest(argList):
    graduationAssessment(argList)

    ID = argList[0]
    st = requirements[userGraduInfo[ID].year]["others"] + "\n"
    st += "위의 조항에 따라 졸업 시험을 응시하셔야 졸업이 가능합니다."

    return st


def graduationAssessment(argList):

    ret = ""

    try:
        ID = argList[0]
        PW = argList[1].replace(' ', '')

        if ID not in userGraduInfo:
            userData = UserData()
            try:
                takeList, stNum = crawlers.getUserSubject(ID, PW)
            except Exception as e:
                return "ID와 PW가 맞지 않습니다. 다시 질문 해 주세요"
            year = stNum[:4]
            userData.st_id += stNum
            userData.year += year
            checkGdRequire(year, userData, takeList)
            userGraduInfo[ID] = userData

        else:
            return ret

    except Exception as e:
        return str(e)




def initFunclist():
    funclist.append(("graduationAvailability", graduationAvailability))
    funclist.append(("moreTotCredit", moreTotCredit))
    funclist.append(("moreMajorCredit", moreMajorCredit))
    funclist.append(("askCompul", askCompul))
    funclist.append(("askConsult", askConsult))
    funclist.append(("askGradPaper", askGradPaper))
    funclist.append(("askChinese", askChinese))
    funclist.append(("askEnglish", askEnglish))
    funclist.append(("askTopcit", askTopcit))
    funclist.append(("askGradTest", askGradTest))


    return

#For debugging
def index(request):

    st = ""
    test_idx = 1
    global userGraduInfo
    ID = ""
    message = "start"
    response = ""

    if message == "start":
        response = "테스트를 시작합니다."

    message = "anal"

    if message == "anal":
        response = "인격을 생성합니다."

        userData = UserData()
        ID = "test" + str(test_idx)
        string_pool = "0123456789"
        stNum = str(random.randint(2010, 2020)) + random.choice(string_pool) + random.choice(
            string_pool) + random.choice(string_pool) + random.choice(string_pool)

        year = stNum[:4]
        userData.st_id += stNum
        userData.year += year

        takeList = []

        # 만족 판단에 쓸 userData
        checkUser = UserData()

        # 확률 표본 생성
        prob = []
        for i in range(0, 100):
            if (i < 80):  # 90%로 0
                prob.append(0)
            else:  # 10%로 1
                prob.append(1)

        random.shuffle(prob)

        plus_prob = []
        for i in range(0, 10):
            if (i < 5):  # 50%로 0
                plus_prob.append("+")
            else:  # 50%로 1
                plus_prob.append("")

        random.shuffle(plus_prob)

        # 확률에 따라 졸업요건 만족 불만족 판단

        # 필수 리스트
        if (random.choice(prob) == 0):
            for i in range(0, len(requirements[year]["compulsorySubjects"])):
                temp = Subject.objects.filter(
                    course_sbjtclss__startswith=requirements[year]["compulsorySubjects"][i].course_id)
                if temp[0].course_pnt.split("-")[0] != ".5":
                    dict = {}
                    dict["sbjt_no"] = requirements[year]["compulsorySubjects"][i].course_id
                    dict["kor_nm"] = requirements[year]["compulsorySubjects"][i].course_title
                    dict["re_year"] = year
                    dict["acq_pnt"] = temp[0].course_pnt.split("-")[0]
                    grd_pool = "ABCD"
                    dict["g_grd"] = random.choice(grd_pool) + random.choice(plus_prob)
                    grade = 0
                    if dict["g_grd"][0] == "A":
                        grade = 4.0
                    elif dict["g_grd"][0] == "B":
                        grade = 3.0
                    elif dict["g_grd"][0] == "C":
                        grade = 2.0
                    elif dict["g_grd"][0] == "D":
                        grade = 1.0

                    if len(dict["g_grd"]) != 1:
                        grade += 0.5

                    dict["grd_mak"] = grade

                    takeList.append(dict)
                    checkCourse(dict, checkUser, year)

        # 전공 학점
        sInfo = Subject.objects.filter(Q(course_pobjnm="전공") | Q(course_pobjnm="전공필수"),
                                       Q(course_sustnm__startswith="소프트") | Q(course_sustnm__startswith="컴퓨터"),
                                       course_year=year)
        if (random.choice(prob) == 0):
            rand_credits = random.randint(requirements[year]["majorCredits"], requirements[year]["majorCredits"] + 10)
        else:
            rand_credits = random.randint(requirements[year]["majorCredits"] - 5,
                                          requirements[year]["majorCredits"] - 3)

        while (checkUser.majorCredits < rand_credits):
            temp = random.choice(sInfo)
            dict = {}

            flag = True
            for i in range(0, len(takeList)):
                if takeList[i]["sbjt_no"] == temp.course_sbjtclss.split("-")[0]:
                    flag = False
                    break

            if flag:
                dict["sbjt_no"] = temp.course_sbjtclss.split("-")[0]
                dict["kor_nm"] = temp.course_clssnm
                dict["re_year"] = year
                dict["acq_pnt"] = temp.course_pnt.split("-")[0]
                grd_pool = "ABCD"
                dict["g_grd"] = random.choice(grd_pool) + random.choice(plus_prob)
                grade = 0
                if dict["g_grd"][0] == "A":
                    grade = 4.0
                elif dict["g_grd"][0] == "B":
                    grade = 3.0
                elif dict["g_grd"][0] == "C":
                    grade = 2.0
                elif dict["g_grd"][0] == "D":
                    grade = 1.0

                if len(dict["g_grd"]) != 1:
                    grade += 0.5

                dict["grd_mak"] = grade

                takeList.append(dict)
                checkCourse(dict, checkUser, year)

        # 전공기초 학점
        sInfo = Subject.objects.filter(Q(course_sustnm__startswith="소프트") | Q(course_sustnm__startswith="컴퓨터"),
                                       course_pobjnm="전공기초", course_year=year)
        if (random.choice(prob) == 0):
            rand_credits = random.randint(requirements[year]["majorBasicCredits"],
                                          requirements[year]["majorBasicCredits"])
        else:
            rand_credits = random.randint(requirements[year]["majorBasicCredits"] - 6,
                                          requirements[year]["majorBasicCredits"] - 2)

        while checkUser.majorBasicCredits <= rand_credits:
            temp = random.choice(sInfo)
            dict = {}

            flag = True
            for i in range(0, len(takeList)):
                if takeList[i]["sbjt_no"] == temp.course_sbjtclss.split("-")[0]:
                    flag = False
                    break

            if flag:
                dict["sbjt_no"] = temp.course_sbjtclss.split("-")[0]
                dict["kor_nm"] = temp.course_clssnm
                dict["re_year"] = year
                dict["acq_pnt"] = temp.course_pnt.split("-")[0]
                grd_pool = "ABCD"
                dict["g_grd"] = random.choice(grd_pool) + random.choice(plus_prob)
                grade = 0
                if dict["g_grd"][0] == "A":
                    grade = 4.0
                elif dict["g_grd"][0] == "B":
                    grade = 3.0
                elif dict["g_grd"][0] == "C":
                    grade = 2.0
                elif dict["g_grd"][0] == "D":
                    grade = 1.0

                if len(dict["g_grd"]) != 1:
                    grade += 0.5

                dict["grd_mak"] = grade

                takeList.append(dict)
                checkCourse(dict, checkUser, year)

        # 교양 학점
        sInfo = Subject.objects.filter(course_pobjnm="교양", course_year=year)
        rand_credits = random.randint(35, 45)

        while (checkUser.totalGECredits < rand_credits):
            temp = random.choice(sInfo)
            dict = {}

            flag = True
            for i in range(0, len(takeList)):
                if takeList[i]["sbjt_no"] == temp.course_sbjtclss.split("-")[0]:
                    flag = False
                    break

            if flag:
                dict["sbjt_no"] = temp.course_sbjtclss.split("-")[0]
                dict["kor_nm"] = temp.course_clssnm
                dict["re_year"] = year
                dict["acq_pnt"] = temp.course_pnt.split("-")[0]
                grd_pool = "ABCD"
                dict["g_grd"] = random.choice(grd_pool) + random.choice(plus_prob)
                grade = 0
                if dict["g_grd"][0] == "A":
                    grade = 4.0
                elif dict["g_grd"][0] == "B":
                    grade = 3.0
                elif dict["g_grd"][0] == "C":
                    grade = 2.0
                elif dict["g_grd"][0] == "D":
                    grade = 1.0

                if len(dict["g_grd"]) != 1:
                    grade += 0.5

                dict["grd_mak"] = grade

                takeList.append(dict)
                checkCourse(dict, checkUser, year)

        checkGdRequire(year, userData, takeList)
        userGraduInfo[ID] = userData
        test_idx += 1

        st += "학번: " + userGraduInfo[ID].st_id + "\n" + "수강한 과목:\n"
        for i in range(0, len(takeList)):
            st += takeList[i]["kor_nm"] + "(" + takeList[i]["acq_pnt"] + "학점)" + ": " + takeList[i]["g_grd"] + "\n"

    message = "makingStudent"

    if message == "makingStudent":
        response = "생성 완료\n"
        response += st

    message = "totalCredits"
    if message == "totalCredits":
        response = "해당 학번의 학생은 총 " + str(requirements[userGraduInfo[ID].year]["totalCredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].totalCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].totalCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].totalCredits) + " 학점을 수강하였고 " + str(userGraduInfo[ID].totalCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    message = "exclusiveGECredits"
    if message == "exclusiveGECredits":
        response = "해당 학번의 학생은 전문 교양을 " + str(requirements[userGraduInfo[ID].year]["exclusiveGECredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].exclusiveGECreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].exclusiveGECredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].exclusiveGECredits) + " 학점을 수강하였고 " + str(userGraduInfo[ID].exclusiveGECreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    message = "BSMCredits"
    if message == "BSMCredits":
        response = "해당 학번의 학생은 BSM 과목을 " + str(requirements[userGraduInfo[ID].year]["bsmCredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].bsmCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].bsmCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].bsmCredits) + " 학점을 수강하였고 " + str(userGraduInfo[ID].bsmCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    message = "coreGECredits"
    if message == "coreGECredits":
        if int(userGraduInfo[ID].year) <= 2014:
            response = "해당 학번의 학생은 핵심 교양을 " + str(requirements[userGraduInfo[ID].year]["numCoreGE"]) + " 과목 이상 수강해야 합니다.\n"
            if userGraduInfo[ID].numCoreGESatisfied:
                response += "이 학생은 총 " + str(userGraduInfo[ID].numCoreGE) + " 과목을 수강하였으므로 위 조건을 만족합니다.\n"
            else:
                response += "이 학생은 총 " + str(userGraduInfo[ID].numCoreGE) + " 과목을 수강하였고 " + str(
                    userGraduInfo[ID].numCoreGEMore) + "과목을 더 수강해야 위 조건을 만족합니다.\n"
        elif int(userGraduInfo[ID].year) == 2015:
            response = "해당 학번의 학생은 토대기반, 존재구축, 소통융합, 실천 영역의 핵심 교양을 각각 1과목 이상 수강해야 합니다.\n"
            if  userGraduInfo[ID].coreGE15_satisfied:
                response += "이 학생은 모든 영역의 핵심 교양을 수강하였습니다.\n"
            else:
                response += "이 학생은 4가지 영역 중 "
                if userGraduInfo[ID].coreGE15["토대기반"] == False:
                    response += "[토대기반]"
                if userGraduInfo[ID].coreGE15["존재구축"] == False:
                    response += "[존재구축]"
                if userGraduInfo[ID].coreGE15["소통융합"] == False:
                    response += "[소통융합]"
                if userGraduInfo[ID].coreGE15["실천"] == False:
                    response += "[실천]"
                response += " 영역의 핵심 교양을 수강해야 위 조건을 만족합니다.\n"

        else:
            response = "해당 학번의 학생은 도전, 창의, 융합, 신뢰, 소통 영역의 핵심 교양을 각각 1과목 이상 수강해야 합니다.\n"
            if  userGraduInfo[ID].coreGE16to20_satisfied:
                response += "이 학생은 모든 영역의 핵심 교양을 수강하였습니다.\n"
            else:
                response += "이 학생은 5가지 영역 중 "
                try:
                    if userGraduInfo[ID].coreGE16to20["도전"] == False:
                        response += "[도전]"
                    if userGraduInfo[ID].coreGE16to20["창의"] == False:
                        response += "[창의]"
                    if userGraduInfo[ID].coreGE16to20["융합"] == False:
                        response += "[융합]"
                    if userGraduInfo[ID].coreGE16to20["신뢰"] == False:
                        response += "[신뢰]"
                    if userGraduInfo[ID].coreGE16to20["소통"] == False:
                        response += "[소통]"
                except Exception as e:
                    str(e)
                    #response = userGraduInfo[ID].coreGE16to20["도전"]


                response += " 영역의 핵심 교양을 수강해야 위 조건을 만족합니다.\n"

    message = "majorCredits"
    if message == "majorCredits":
        response = "해당 학번의 학생은 전공 과목을 " + str(requirements[userGraduInfo[ID].year]["majorCredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].majorCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorCredits) + " 학점을 수강하였고 " + str(userGraduInfo[ID].majorCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    message = "majorBasicCredits"
    if message == "majorBasicCredits":
        response = "해당 학번의 학생은 전공 기초 과목을 " + str(requirements[userGraduInfo[ID].year]["majorBasicCredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].majorBasicCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorBasicCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorBasicCredits) + " 학점을 수강하였고 " + str(userGraduInfo[ID].majorBasicCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    message = "majorCompulsoryCredits"
    if message == "majorCompulsoryCredits":
        response = "해당 학번의 학생은 전공 필수 과목을 " + str(requirements[userGraduInfo[ID].year]["majorCompulsoryCredits"]) + " 학점 수강해야 합니다. \n"
        if userGraduInfo[ID].majorCompulsoryCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorCompulsoryCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorCompulsoryCredits) + " 학점을 수강하였고 " + str(userGraduInfo[ID].majorCompulsoryCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    message = "designSubjectCredits"
    if message == "designSubjectCredits":
        response = "해당 학번의 학생은 수강한 설계 과목들의 설계 점수의 총합이 " + str(requirements[userGraduInfo[ID].year]["designSubjectCredits"]) + " 이상이 되어야 합니다. \n"
        if userGraduInfo[ID].majorCompulsoryCreditsSatisfied:
            response += "이 학생의 설계 점수는 총 " + str(userGraduInfo[ID].majorCompulsoryCredits) + " 점 이므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생의 설계 점수는 총 " + str(userGraduInfo[ID].majorCompulsoryCredits) + " 점이며 " + str(userGraduInfo[ID].majorCompulsoryCreditsMore) + " 점을 더 취득해야 위 조건을 만족합니다.\n"

    message = "avgGrade"
    if message == "avgGrade":
        if int(userGraduInfo[ID].year) >= 2018:
            response = "해당 학번의 학생은 평균 학점이 " + str(requirements[userGraduInfo[ID].year]["avgGrade"]) + " 이상이 되어야 합니다. \n"
            if userGraduInfo[ID].majorCompulsoryCreditsSatisfied:
                response += "이 학생의 평균 학점은 " + str(userGraduInfo[ID].avgGrade) + " 이므로 위 조건을 만족합니다.\n"
            else:
                response += "이 학생의 평균 학점은 " + str(userGraduInfo[ID].avgGrade) + " 이며 평균 학점을 " + str(userGraduInfo[ID].avgGradeMore) + " 만큼 더 올리셔야 위 조건을 만족합니다.\n"

    message = "compulsoryNotTaken"
    if message == "compulsoryNotTaken":
        response = "해당 학번의 학생이 들어야하는 필수 과목 리스트는 다음과 같습니다.\n"
        for item in requirements[userGraduInfo[ID].year]["compulsorySubjects"]:
            response += item.course_title + "\n"

        if userGraduInfo[ID].compulsorySatisfied:
            response += "이 학생은 모든 필수 과목을 전부 수강했습니다.\n"
        else:
            response += "이 학생은 " + userGraduInfo[ID].compulsoryResult + "\n"

    message = "machGE"
    if message == "machGE":
        if int(userGraduInfo[ID].year) >= 2015:
            response = "해당 학번의 MACH 교양 과목을 " + str(requirements[userGraduInfo[ID].year]["MACHGE"]) + " 학점 이상 수강해야 합니다. \n"
            if userGraduInfo[ID].machGECreditsSatisfied:
                response += "이 학생은 총 " + str(userGraduInfo[ID].machGECredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
            else:
                response += "이 학생은 총 " + str(userGraduInfo[ID].machGECredits) + " 학점을 수강하였고 " + str(userGraduInfo[ID].machGECreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다\n"


    message = "machPrac"
    if message == "machPrac":
        if int(userGraduInfo[ID].year) >= 2015 and int(userGraduInfo[ID].year) < 2019:
            response = "해당 학번의 MACH 교양 과목을 " + str(requirements[userGraduInfo[ID].year]["MACHPrac"]) + " 학점 이상 수강해야 합니다. \n"
            if userGraduInfo[ID].machPracCreditsSatisfied:
                response += "이 학생은 총 " + str(userGraduInfo[ID].machPracCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
            else:
                response += "이 학생은 총 " + str(userGraduInfo[ID].machPracCredits) + " 학점을 수강하였고 " + str(userGraduInfo[ID].machPracCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다\n"

    message = "others"
    if message == "others":
        response = "이에 더해,\n"
        response += requirements[userGraduInfo[ID].year]["others"] + "\n"
        response += "상기의 조건들을 만족해야 졸업이 가능합니다.\n"

    return ""

def api(request, message):
    try:
        protocol, message = message.split("$", maxsplit=1)

        HOST = 'ec2-3-21-126-101.us-east-2.compute.amazonaws.com'
        PORT = 1024

    

        if (protocol == 'start'):
            name = message
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


        elif (protocol == 'notfirst'):
            name, message = message.split("$", maxsplit = 1)

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
    except Exception as e:
        return JsonResponse({
            'message': 1,
            'content': "ERROR in api " + str(e)
        })

st = ""
test_idx = 1
ID = ""
def startTest(request, message):
    global st
    global test_idx
    global ID
    global userGraduInfo

    response = ""

    if message == "start":
        response = "테스트를 시작합니다."
    
    if message == "anal":
        response = "인격을 생성합니다."
        st = ""
        userData = UserData()
        ID = "test" + str(test_idx)
        string_pool = "0123456789"
        stNum = str(random.randint(2010, 2020)) + random.choice(string_pool) + random.choice(
            string_pool) + random.choice(string_pool) + random.choice(string_pool)
       
        year = stNum[:4]
        userData.st_id += stNum
        userData.year += year

        takeList = []

        # 만족 판단에 쓸 userData
        checkUser = UserData()

        # 확률 표본 생성
        prob = []
        for i in range(0, 100):
            if (i < 80):  # 90%로 0
                prob.append(0)
            else:  # 10%로 1
                prob.append(1)

        random.shuffle(prob)

        plus_prob = []
        for i in range(0, 10):
            if (i < 5):  # 50%로 0
                plus_prob.append("+")
            else:  # 50%로 1
                plus_prob.append("")

        random.shuffle(plus_prob)

        # 확률에 따라 졸업요건 만족 불만족 판단

        # 필수 리스트
        if (random.choice(prob) == 0):
            for i in range(0, len(requirements[year]["compulsorySubjects"])):
                temp = Subject.objects.filter(
                    course_sbjtclss__startswith=requirements[year]["compulsorySubjects"][i].course_id)
                if temp[0].course_pnt.split("-")[0] != ".5":
                    dict = {}
                    dict["sbjt_no"] = requirements[year]["compulsorySubjects"][i].course_id
                    dict["kor_nm"] = requirements[year]["compulsorySubjects"][i].course_title
                    dict["re_year"] = year
                    dict["acq_pnt"] = temp[0].course_pnt.split("-")[0]
                    grd_pool = "ABCD"
                    dict["g_grd"] = random.choice(grd_pool) + random.choice(plus_prob)
                    grade = 0
                    if dict["g_grd"][0] == "A":
                        grade = 4.0
                    elif dict["g_grd"][0] == "B":
                        grade = 3.0
                    elif dict["g_grd"][0] == "C":
                        grade = 2.0
                    elif dict["g_grd"][0] == "D":
                        grade = 1.0

                    if len(dict["g_grd"]) != 1:
                        grade += 0.5

                    dict["grd_mak"] = grade

                    takeList.append(dict)
                    checkCourse(dict, checkUser, year)

        # 전공 학점
        sInfo = Subject.objects.filter(Q(course_pobjnm="전공") | Q(course_pobjnm="전공필수"),
                                       Q(course_sustnm__startswith="소프트") | Q(course_sustnm__startswith="컴퓨터"),
                                       course_year=year)
        if (random.choice(prob) == 0):
            rand_credits = random.randint(requirements[year]["majorCredits"], requirements[year]["majorCredits"] + 10)
        else:
            rand_credits = random.randint(requirements[year]["majorCredits"] - 5,
                                          requirements[year]["majorCredits"] - 3)

        while (checkUser.majorCredits < rand_credits):
            temp = random.choice(sInfo)
            dict = {}

            flag = True
            for i in range(0, len(takeList)):
                if takeList[i]["sbjt_no"] == temp.course_sbjtclss.split("-")[0]:
                    flag = False
                    break

            if flag:
                dict["sbjt_no"] = temp.course_sbjtclss.split("-")[0]
                dict["kor_nm"] = temp.course_clssnm
                dict["re_year"] = year
                dict["acq_pnt"] = temp.course_pnt.split("-")[0]
                grd_pool = "ABCD"
                dict["g_grd"] = random.choice(grd_pool) + random.choice(plus_prob)
                grade = 0
                if dict["g_grd"][0] == "A":
                    grade = 4.0
                elif dict["g_grd"][0] == "B":
                    grade = 3.0
                elif dict["g_grd"][0] == "C":
                    grade = 2.0
                elif dict["g_grd"][0] == "D":
                    grade = 1.0

                if len(dict["g_grd"]) != 1:
                    grade += 0.5

                dict["grd_mak"] = grade

                takeList.append(dict)
                checkCourse(dict, checkUser, year)

        # 전공기초 학점
        sInfo = Subject.objects.filter(Q(course_sustnm__startswith="소프트") | Q(course_sustnm__startswith="컴퓨터"),
                                       course_pobjnm="전공기초", course_year=year)
        if (random.choice(prob) == 0):
            rand_credits = random.randint(requirements[year]["majorBasicCredits"],
                                          requirements[year]["majorBasicCredits"])
        else:
            rand_credits = random.randint(requirements[year]["majorBasicCredits"] - 6,
                                          requirements[year]["majorBasicCredits"] - 2)

        while checkUser.majorBasicCredits <= rand_credits:
            temp = random.choice(sInfo)
            dict = {}

            flag = True
            for i in range(0, len(takeList)):
                if takeList[i]["sbjt_no"] == temp.course_sbjtclss.split("-")[0]:
                    flag = False
                    break

            if flag:
                dict["sbjt_no"] = temp.course_sbjtclss.split("-")[0]
                dict["kor_nm"] = temp.course_clssnm
                dict["re_year"] = year
                dict["acq_pnt"] = temp.course_pnt.split("-")[0]
                grd_pool = "ABCD"
                dict["g_grd"] = random.choice(grd_pool) + random.choice(plus_prob)
                grade = 0
                if dict["g_grd"][0] == "A":
                    grade = 4.0
                elif dict["g_grd"][0] == "B":
                    grade = 3.0
                elif dict["g_grd"][0] == "C":
                    grade = 2.0
                elif dict["g_grd"][0] == "D":
                    grade = 1.0

                if len(dict["g_grd"]) != 1:
                    grade += 0.5

                dict["grd_mak"] = grade

                takeList.append(dict)
                checkCourse(dict, checkUser, year)

        # 교양 학점
        sInfo = Subject.objects.filter(course_pobjnm="교양", course_year=year)
        rand_credits = random.randint(35, 45)

        while (checkUser.totalGECredits < rand_credits):
            temp = random.choice(sInfo)
            dict = {}

            flag = True
            for i in range(0, len(takeList)):
                if takeList[i]["sbjt_no"] == temp.course_sbjtclss.split("-")[0]:
                    flag = False
                    break

            if flag:
                dict["sbjt_no"] = temp.course_sbjtclss.split("-")[0]
                dict["kor_nm"] = temp.course_clssnm
                dict["re_year"] = year
                dict["acq_pnt"] = temp.course_pnt.split("-")[0]
                grd_pool = "ABCD"
                dict["g_grd"] = random.choice(grd_pool) + random.choice(plus_prob)
                grade = 0
                if dict["g_grd"][0] == "A":
                    grade = 4.0
                elif dict["g_grd"][0] == "B":
                    grade = 3.0
                elif dict["g_grd"][0] == "C":
                    grade = 2.0
                elif dict["g_grd"][0] == "D":
                    grade = 1.0

                if len(dict["g_grd"]) != 1:
                    grade += 0.5

                dict["grd_mak"] = grade

                takeList.append(dict)
                checkCourse(dict, checkUser, year)

        checkGdRequire(year, userData, takeList)
        userGraduInfo[ID] = userData
        test_idx += 1

        st += "학번: " + userGraduInfo[ID].st_id + "\n" + "수강한 과목:\n"
        for i in range(0, len(takeList)):
            st += takeList[i]["kor_nm"] + "(" + takeList[i]["acq_pnt"] + "학점)" + ": " + takeList[i]["g_grd"] + "\n"

        

    if message == "makingStudent":
        response = "생성 완료\n"
        response += st

    #message = "totalCredits"
    if message == "totalCredits":
        time.sleep(1)
        response = "해당 학번의 학생은 총 " + str(requirements[userGraduInfo[ID].year]["totalCredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].totalCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].totalCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].totalCredits) + " 학점을 수강하였고 " + str(
                userGraduInfo[ID].totalCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    #message = "exclusiveGECredits"
    if message == "exclusiveGECredits":
        time.sleep(1)
        response = "해당 학번의 학생은 전문 교양을 " + str(
            requirements[userGraduInfo[ID].year]["exclusiveGECredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].exclusiveGECreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].exclusiveGECredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].exclusiveGECredits) + " 학점을 수강하였고 " + str(
                userGraduInfo[ID].exclusiveGECreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    #message = "BSMCredits"
    if message == "BSMCredits":
        time.sleep(1)
        response = "해당 학번의 학생은 BSM 과목을 " + str(
            requirements[userGraduInfo[ID].year]["bsmCredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].bsmCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].bsmCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].bsmCredits) + " 학점을 수강하였고 " + str(
                userGraduInfo[ID].bsmCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    #message = "coreGECredits"
    if message == "coreGECredits":
        time.sleep(1)
        if int(userGraduInfo[ID].year) <= 2014:
            response = "해당 학번의 학생은 핵심 교양을 " + str(
                requirements[userGraduInfo[ID].year]["numCoreGE"]) + " 과목 이상 수강해야 합니다.\n"
            if userGraduInfo[ID].numCoreGESatisfied:
                response += "이 학생은 총 " + str(userGraduInfo[ID].numCoreGE) + " 과목을 수강하였으므로 위 조건을 만족합니다.\n"
            else:
                response += "이 학생은 총 " + str(userGraduInfo[ID].numCoreGE) + " 과목을 수강하였고 " + str(
                    userGraduInfo[ID].numCoreGEMore) + "과목을 더 수강해야 위 조건을 만족합니다.\n"
        elif int(userGraduInfo[ID].year) == 2015:
            response = "해당 학번의 학생은 토대기반, 존재구축, 소통융합, 실천 영역의 핵심 교양을 각각 1과목 이상 수강해야 합니다.\n"
            if userGraduInfo[ID].coreGE15_satisfied:
                response += "이 학생은 모든 영역의 핵심 교양을 수강하였습니다.\n"
            else:
                response += "이 학생은 4가지 영역 중 "
                if userGraduInfo[ID].coreGE15["토대기반"] == False:
                    response += "[토대기반]"
                if userGraduInfo[ID].coreGE15["존재구축"] == False:
                    response += "[존재구축]"
                if userGraduInfo[ID].coreGE15["소통융합"] == False:
                    response += "[소통융합]"
                if userGraduInfo[ID].coreGE15["실천"] == False:
                    response += "[실천]"
                response += " 영역의 핵심 교양을 수강해야 위 조건을 만족합니다.\n"

        else:
            response = "해당 학번의 학생은 도전, 창의, 융합, 신뢰, 소통 영역의 핵심 교양을 각각 1과목 이상 수강해야 합니다.\n"
            if userGraduInfo[ID].coreGE16to20_satisfied:
                response += "이 학생은 모든 영역의 핵심 교양을 수강하였습니다.\n"
            else:
                response += "이 학생은 5가지 영역 중 "
                try:
                    if userGraduInfo[ID].coreGE16to20["도전"] == False:
                        response += "[도전]"
                    if userGraduInfo[ID].coreGE16to20["창의"] == False:
                        response += "[창의]"
                    if userGraduInfo[ID].coreGE16to20["융합"] == False:
                        response += "[융합]"
                    if userGraduInfo[ID].coreGE16to20["신뢰"] == False:
                        response += "[신뢰]"
                    if userGraduInfo[ID].coreGE16to20["소통"] == False:
                        response += "[소통]"
                except Exception as e:
                    str(e)
                    # response = userGraduInfo[ID].coreGE16to20["도전"]

                response += " 영역의 핵심 교양을 수강해야 위 조건을 만족합니다.\n"

    #message = "majorCredits"
    if message == "majorCredits":
        time.sleep(1)
        response = "해당 학번의 학생은 전공 과목을 " + str(
            requirements[userGraduInfo[ID].year]["majorCredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].majorCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorCredits) + " 학점을 수강하였고 " + str(
                userGraduInfo[ID].majorCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    #message = "majorBasicCredits"
    if message == "majorBasicCredits":
        time.sleep(1)
        response = "해당 학번의 학생은 전공 기초 과목을 " + str(
            requirements[userGraduInfo[ID].year]["majorBasicCredits"]) + " 학점 이상을 수강해야 합니다. \n"
        if userGraduInfo[ID].majorBasicCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorBasicCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorBasicCredits) + " 학점을 수강하였고 " + str(
                userGraduInfo[ID].majorBasicCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    #message = "majorCompulsoryCredits"
    if message == "majorCompulsoryCredits":
        time.sleep(1)
        response = "해당 학번의 학생은 전공 필수 과목을 " + str(
            requirements[userGraduInfo[ID].year]["majorCompulsoryCredits"]) + " 학점 수강해야 합니다. \n"
        if userGraduInfo[ID].majorCompulsoryCreditsSatisfied:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorCompulsoryCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생은 총 " + str(userGraduInfo[ID].majorCompulsoryCredits) + " 학점을 수강하였고 " + str(
                userGraduInfo[ID].majorCompulsoryCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다.\n"

    #message = "designSubjectCredits"
    if message == "designSubjectCredits":
        time.sleep(1)
        response = "해당 학번의 학생은 수강한 설계 과목들의 설계 점수의 총합이 " + str(
            requirements[userGraduInfo[ID].year]["designSubjectCredits"]) + " 이상이 되어야 합니다. \n"
        if userGraduInfo[ID].majorCompulsoryCreditsSatisfied:
            response += "이 학생의 설계 점수는 총 " + str(userGraduInfo[ID].majorCompulsoryCredits) + " 점 이므로 위 조건을 만족합니다.\n"
        else:
            response += "이 학생의 설계 점수는 총 " + str(userGraduInfo[ID].majorCompulsoryCredits) + " 점이며 " + str(
                userGraduInfo[ID].majorCompulsoryCreditsMore) + " 점을 더 취득해야 위 조건을 만족합니다.\n"

    #message = "avgGrade"
    if message == "avgGrade":
        time.sleep(1)
        if int(userGraduInfo[ID].year) >= 2018:
            response = "해당 학번의 학생은 평균 학점이 " + str(requirements[userGraduInfo[ID].year]["avgGrade"]) + " 이상이 되어야 합니다. \n"
            if userGraduInfo[ID].avgGradeSatisfied:
                response += "이 학생의 평균 학점은 " + str(userGraduInfo[ID].avgGrade) + " 이므로 위 조건을 만족합니다.\n"
            else:
                response += "이 학생의 평균 학점은 " + str(userGraduInfo[ID].avgGrade) + " 이며 평균 학점을 " + str(
                    userGraduInfo[ID].avgGradeMore) + " 만큼 더 올리셔야 위 조건을 만족합니다.\n"

    #message = "compulsoryNotTaken"
    if message == "compulsoryNotTaken":
        time.sleep(1)
        response = "해당 학번의 학생이 들어야하는 필수 과목 리스트는 다음과 같습니다.\n"
        for item in requirements[userGraduInfo[ID].year]["compulsorySubjects"]:
            response += item.course_title + "\n"

        if userGraduInfo[ID].compulsorySatisfied:
            response += "이 학생은 모든 필수 과목을 전부 수강했습니다.\n"
        else:
            response += "이 학생은 " + userGraduInfo[ID].compulsoryResult + "\n"

    #message = "machGE"
    if message == "machGE":
        time.sleep(1)
        if int(userGraduInfo[ID].year) >= 2015:
            response = "해당 학번의 MACH 교양 과목을 " + str(
                requirements[userGraduInfo[ID].year]["MACHGE"]) + " 학점 이상 수강해야 합니다. \n"
            if userGraduInfo[ID].machGECreditsSatisfied:
                response += "이 학생은 총 " + str(userGraduInfo[ID].machGECredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
            else:
                response += "이 학생은 총 " + str(userGraduInfo[ID].machGECredits) + " 학점을 수강하였고 " + str(
                    userGraduInfo[ID].machGECreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다\n"

    #message = "machPrac"
    if message == "machPrac":
        time.sleep(1)
        if int(userGraduInfo[ID].year) >= 2015 and int(userGraduInfo[ID].year) < 2019:
            response = "해당 학번의 MACH 교양 과목을 " + str(
                requirements[userGraduInfo[ID].year]["MACHPrac"]) + " 학점 이상 수강해야 합니다. \n"
            if userGraduInfo[ID].machPracCreditsSatisfied:
                response += "이 학생은 총 " + str(userGraduInfo[ID].machPracCredits) + " 학점을 수강하였으므로 위 조건을 만족합니다.\n"
            else:
                response += "이 학생은 총 " + str(userGraduInfo[ID].machPracCredits) + " 학점을 수강하였고 " + str(
                    userGraduInfo[ID].machPracCreditsMore) + " 학점을 더 수강해야 위 조건을 만족합니다\n"

    #message = "others"
    if message == "others":
        time.sleep(1)
        response = "이에 더해,\n"
        response += requirements[userGraduInfo[ID].year]["others"] + "\n"
        response += "상기의 조건들을 만족해야 졸업이 가능합니다.\n"


    return JsonResponse({
            'message': 1,
            'content': response
        })

def checkCourse(dict, checkUser, year):
    sInfo = Subject.objects.filter(course_sbjtclss__startswith=dict["sbjt_no"], course_year=year)

    try:
        checkUser.totalCredits += int(sInfo[0].course_pnt.split("-")[0])
    except Exception as e:
        str(e)

    for i in range(0, len(sInfo)):
        if "전공" in sInfo[i].course_pobjnm and "기초" not in sInfo[i].course_pobjnm:
            checkUser.majorCredits += int(sInfo[i].course_pnt.split("-")[0])
            break

    for i in range(0, len(sInfo)):
        if "전공기초" in sInfo[i].course_pobjnm:
            checkUser.majorBasicCredits += int(sInfo[i].course_pnt.split("-")[0])
            break
    
    for i in range(0, len(sInfo)):
        if "교양" in sInfo[i].course_pobjnm:
            checkUser.totalGECredits += int(sInfo[i].course_pnt.split("-")[0])
            break

@csrf_exempt
def refresh(request):

    if request.method == 'POST':
        tmp = json.loads(request.body)
        data = tmp['data']

        for item in data:
            if item in userGraduInfo.keys():
                del userGraduInfo[item]

    return HttpResponse('success')
