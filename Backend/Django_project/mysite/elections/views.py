from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect, Http404
from django.http import JsonResponse
import datetime
import socket
import crawlers
from .models import Compulsory, Substitute, Subject


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
requirements["2010"]["designSubjectCredits"]=12 #Total credits required for design courses
requirements["2010"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2010) # List of compulsory subjects for the year

requirements["2011"]["totalCredits"]=132
requirements["2011"]["numCoreGE"]=3
requirements["2011"]["GECreditsLimit"]=45
requirements["2011"]["majorCredits"]=66
requirements["2011"]["exclusiveGECredits"]=6
requirements["2011"]["bsmCredits"]=18
requirements["2011"]["designSubjectCredits"]=12
requirements["2011"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2011)

requirements["2012"]["totalCredits"]=132
requirements["2012"]["numCoreGE"]=3
requirements["2012"]["GECreditsLimit"]=45
requirements["2012"]["majorCredits"]=66
requirements["2012"]["exclusiveGECredits"]=6
requirements["2012"]["bsmCredits"]=18
requirements["2012"]["designSubjectCredits"]=12
requirements["2012"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2012)

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

requirements["2015"]["totalCredits"]=140
requirements["2015"]["CoreGE"]=["토대기반","존재구축","소통융합","실천"] #General Education course for each area (one or more required)
requirements["2015"]["GECreditsLimit"]=45
requirements["2015"]["majorCredits"]=84
requirements["2015"]["MACHGE"]=4        #MACH liberal arts credits to be taken => 2 courses
requirements["2015"]["MACHPrac"]=2      #Total MACH practice credits to be taken => 2 courses
requirements["2015"]["exclusiveGECredits"]=6
requirements["2015"]["bsmCredits"]=18
requirements["2015"]["designSubjectCredits"]=12
requirements["2015"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2015)

requirements["2016"]["totalCredits"]=140
requirements["2016"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2016"]["GECreditsLimit"]=45
requirements["2016"]["majorCredits"]=84
requirements["2016"]["MACHGE"]=4
requirements["2016"]["MACHPrac"]=2
requirements["2016"]["exclusiveGECredits"]=6
requirements["2016"]["bsmCredits"]=18
requirements["2016"]["designSubjectCredits"]=12
requirements["2016"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2016)

requirements["2017"]["totalCredits"]=140
requirements["2017"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2017"]["GECreditsLimit"]=45
requirements["2017"]["majorCredits"]=84
requirements["2017"]["MACHGE"]=4
requirements["2017"]["MACHPrac"]=2
requirements["2017"]["exclusiveGECredits"]=6
requirements["2017"]["bsmCredits"]=18
requirements["2017"]["designSubjectCredits"]=12
requirements["2017"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2017)

requirements["2018"]["totalCredits"]=140
requirements["2018"]["CoreGE"]=["도전","창의","융합","신뢰","소통"]
requirements["2018"]["GECreditsLimit"]=45
requirements["2018"]["majorCredits"]=84
requirements["2018"]["MACHGE"]=4
requirements["2018"]["MACHPrac"]=2
requirements["2018"]["exclusiveGECredits"]=6
requirements["2018"]["bsmCredits"]=18
requirements["2018"]["designSubjectCredits"]=12
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
requirements["2019"]["designSubjectCredits"]=12
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
requirements["2020"]["designSubjectCredits"]=12
requirements["2020"]["avgGrade"]=2.2
requirements["2020"]["compulsorySubjects"]=Compulsory.objects.filter(course_year=2020)

funclist = []   #질문 대답 함수 리스트


# Save {ID : UserData}
userGraduInfo = dict()


class UserData:
    totalCredits = 0
    totalCreditsSatisfied = False
    exclusiveGECredits = 0
    exclusiveGECreditsList = []
    exclusiveGECreditsSatisfied = False
    bsmCredits = 0
    bsmCreditsList = []
    bsmCreditsSatisfied = False
    numCoreGE = 0
    numCoreGEList = []
    numCoreGESatisfied = False
    totalGECredits = 0
    totalGECreditsList = []
    #totalGECreditsSatisfied = False
    majorCredits = 0
    majorCreditsList = []
    majorCreditsSatisfied = False
    majorBasicCredits = 0
    majorBasicCreditsList = []
    majorBasicCreditsSatisfied = False
    majorCompulsoryCredits = 0
    majorCompulsoryCreditsList = []
    majorCompulsoryCreditsSatisfied = False
    designSubjectCredits = 0
    designSubjectCreditsList = []
    designSubjectCreditsSatisfied = False
    avgGrade = 0
    avgGradeSatisfied = False
    compulsoryNotTaken = []
    compulsorySatisfied = False
    coreGE15 = {}
    coreGE15["토대기반"]=False
    coreGE15["존재구축"] = False
    coreGE15["소통융합"] = False
    coreGE15["실천"] = False
    coreGE15_satisfied = False
    coreGE16 = {}
    coreGE16["도전"] = False
    coreGE16["창의"] = False
    coreGE16["융합"] = False
    coreGE16["신뢰"] = False
    coreGE16["소통"] = False
    coreGE16_satisfied = False
    machGECredits = 0
    machGECreditsList = []
    machGECreditsSatisfied = False
    machPracCredits = 0
    machPracCreditsList = []
    machPracCreditsSatisfied = False
    result = ""


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

                    takeListAdaptedRetaken[idx] = takeList[index]
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
            st += sbjt[0].course_clssnm + ", "

        userData.result += "필수 과목 중 아직 수강하지 않은 과목이 있습니다.\n 수강하지 않은 필수 과목 : " + st
    return ""

def checkMinMaxRequire(year, userData, takeList):

    for func in check_funclist:
        if func[0] == year:
            func[1](year, userData, takeList)


    return ""

def check2010(year):
    

    return ""
def check2013(year, userData, takeList):
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

    # ------ 요견 판별 로직 ----------

    # 핵심 교양 학점 만족 판별
    if userData.numCoreGE >= requirements[year]["numCoreGE"]:
        userData.numCoreGESatisfied = True
    else:
        st += "핵심 교양 불만족\n 핵심 교양 과목을 " + str(equirements[year]["numCoreGE"] - userData.numCoreGE) + "개 이상 더 들으셔야 합니다."

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
        st += "전공 과목 불만족\n 전공 과목 학점을 " + str(
            requirements[year]["majorCredits"] - userData.majorCredits) + "만큼 더 취득하셔야 합니다."

    # 전공 기초 학점 만족 판별
    if userData.majorBasicCredits >= requirements[year]["majorBasicCredits"]:
        userData.majorBasicCreditsSatisfied = True
    else:
        st += "전공 기초 과목 불만족\n 전공 기초 과목 학점을 " + str(
            requirements[year]["majorBasicCredits"] - userData.majorBasicCredits) + "만큼 더 취득하셔야 합니다."

    if userData.majorCompulsoryCredits >= requirements[year]["majorCompulsoryCredits"]:
        userData.majorCompulsoryCreditsSatisfied = True
    else:
        st += "전공 필수 과목 불만족\n 전공 필수 과목 학점을 " + str(
            requirements[year]["majorCompulsoryCredits"] - userData.majorCompulsoryCredits) + "만큼 더 취득하셔야 합니다."

    # 총 학점 만족 판별
    if (userData.totalCredits - diff) >= requirements[year]["totalCredits"]:
        userData.totalCreditsSatisfied = True
    else:
        st += "총 학점 불만족\n 총 학점을 " + str(requirements[year]["totalCredits"] - userData.totalCredits) + "만큼 더 취득하셔야 합니다."

    # 전문 교양 학점 만족 판별
    if userData.exclusiveGECredits >= requirements[year]["exclusiveGECredits"]:
        userData.exclusiveGECreditsSatisfied = True
    else:
        st += "전문 교양 학점 불만족\n 전문 교양 과목 학점을 " + str(
            requirements[year]["exclusiveGECredits"] - userData.exclusiveGECredits) + "만큼 더 취득하셔야 합니다."

    # BSM 학점 만족 판별
    if userData.bsmCredits >= requirements[year]["bsmCredits"]:
        userData.bsmCreditsSatisfied = True
    else:
        st += "BSM 학점 불만족\n BSM 과목 학점을 " + str(
            requirements[year]["bsmCredits"] - userData.bsmCredits) + "만큼 더 취득하셔야 합니다."

    # 설계 학점 만족 판별
    if userData.designSubjectCredits >= requirements[year]["designSubjectCredits"]:
        userData.designSubjectCreditsSatisfied = True
    else:
        st += "설계 학점 불만족\n 설계 과목 학점을 " + str(
            requirements[year]["designSubjectCredits"] - userData.designSubjectCredits) + "만큼 더 취득하셔야 합니다."

    userData.result += st


    return ""

def check2014(year, userData, takeList):
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

    # ------ 요견 판별 로직 ----------

    # 핵심 교양 학점 만족 판별
    if userData.numCoreGE >= requirements[year]["numCoreGE"]:
        userData.numCoreGESatisfied = True
    else:
        st += "핵심 교양 불만족\n 핵심 교양 과목을 " + str(equirements[year]["numCoreGE"] - userData.numCoreGE) + "개 이상 더 들으셔야 합니다."

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
        st += "전공 과목 불만족\n 전공 과목 학점을 " + str(
            requirements[year]["majorCredits"] - userData.majorCredits) + "만큼 더 취득하셔야 합니다."

    # 전공 기초 학점 만족 판별
    if userData.majorBasicCredits >= requirements[year]["majorBasicCredits"]:
        userData.majorBasicCreditsSatisfied = True
    else:
        st += "전공 기초 과목 불만족\n 전공 기초 과목 학점을 " + str(
            requirements[year]["majorBasicCredits"] - userData.majorBasicCredits) + "만큼 더 취득하셔야 합니다."

    if userData.majorCompulsoryCredits >= requirements[year]["majorCompulsoryCredits"]:
        userData.majorCompulsoryCreditsSatisfied = True
    else:
        st += "전공 필수 과목 불만족\n 전공 필수 과목 학점을 " + str(requirements[year]["majorCompulsoryCredits"] - userData.majorCompulsoryCredits) + "만큼 더 취득하셔야 합니다."

    # 총 학점 만족 판별
    if (userData.totalCredits - diff) >= requirements[year]["totalCredits"]:
        userData.totalCreditsSatisfied = True
    else:
        st += "총 학점 불만족\n 총 학점을 " + str(requirements[year]["totalCredits"] - userData.totalCredits) + "만큼 더 취득하셔야 합니다."

    # 전문 교양 학점 만족 판별
    if userData.exclusiveGECredits >= requirements[year]["exclusiveGECredits"]:
        userData.exclusiveGECreditsSatisfied = True
    else:
        st += "전문 교양 학점 불만족\n 전문 교양 과목 학점을 " + str(requirements[year]["exclusiveGECredits"] - userData.exclusiveGECredits) + "만큼 더 취득하셔야 합니다."

    # BSM 학점 만족 판별
    if userData.bsmCredits >= requirements[year]["bsmCredits"]:
        userData.bsmCreditsSatisfied = True
    else:
        st += "BSM 학점 불만족\n BSM 과목 학점을 " + str(requirements[year]["bsmCredits"] - userData.bsmCredits) + "만큼 더 취득하셔야 합니다."

    # 설계 학점 만족 판별
    if userData.designSubjectCredits >= requirements[year]["designSubjectCredits"]:
        userData.designSubjectCreditsSatisfied = True
    else:
        st += "설계 학점 불만족\n 설계 과목 학점을 " + str(requirements[year]["designSubjectCredits"] - userData.designSubjectCredits) + "만큼 더 취득하셔야 합니다."

    userData.result += st


    return ""




check_funclist = [] #년도별 요건 분석 함수 리스트
check_funclist.append(("2014",check2014))
check_funclist.append(("2013",check2013))

def checkGdRequire(year, userData, takeList):
    checkCompulsorySatisfied(year, userData, takeList)
    checkMinMaxRequire(year, userData, takeList)




#TODO Answer whole things
def graduationAvailability(argList):
    return graduationAssessment(argList)


#TODO Answer how more credits achieved
def moreTotCredit(argList):
    return graduationAssessment(argList)


#TODO
def moreMajorCredit(argList):
    return graduationAssessment(argList)

#TODO
def askTotCredit(argList):
    return graduationAssessment(argList)
#TODO
def askMajorCompul(argList):
    return graduationAssessment(argList)
#TODO
def askConsult(argList):
    return graduationAssessment(argList)
#TODO
def askGradPaper(argList):
    return graduationAssessment(argList)


def graduationAssessment(argList):

    ret = ""

    ID = argList[0]
    PW = argList[1].replace(' ', '')

    try:

        if ID not in userGraduInfo:
            userData = UserData()
            try:
                takeList, stNum = crawlers.getUserSubject(ID, PW)
            except Exception as e:
                return "ID와 PW가 맞지 않습니다. 다시 질문 해 주세요"
            year = stNum[:4]
            checkGdRequire(year, userData, takeList)
            userGraduInfo[ID] = userData

        return userGraduInfo[ID].result
    except Exception as e:
        return str(e)




def initFunclist():
    funclist.append(("graduationAvailability", graduationAvailability))
    funclist.append(("moreTotCredit", moreTotCredit))
    funclist.append(("moreMajorCredit", moreMajorCredit))
    funclist.append(("askTotCredit", askTotCredit))
    funclist.append(("askMajorCompul", askMajorCompul))
    funclist.append(("askConsult", askConsult))
    funclist.append(("askGradPaper", askGradPaper))

    return

#For debugging
def index(request):


    return HttpResponse("hello")

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

