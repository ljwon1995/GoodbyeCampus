from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect, Http404
from django.http import JsonResponse
import datetime
import socket
import crawlers
from .models import Compulsory, Substitute, Subject

funclist = []

class UserCheckedData: #user data
    totalCredits = 0
    exclusiveGECredits = 0
    bsmCredits = 0
    numCoreGE = 0
    totalGECredits = 0
    majorCredits = 0
    designSubjectCredits = 0
    compulsoryTaken = []

def certainFunction(argList):
    graduationAssessment(argList)
    #Do its logic

def checkCompulsorySatisfid(year):
    #Do its logic

    return ""

def checkMinMaxRequire(year):
    #Do its logic

    return ""

def checkGdRequire(year):
    ret = ""
    ret += checkCompulsorySatisfied(year)
    ret += checkMinMaxRequire(year)

    return ret


def graduationAssessment(argList):
    ID = argList[0]
    PW = argList[1]
    #TODO In chatscript need to take ! inputs also

    try:
        takeLists = crawlers.getUserSubject("yey6689", "para3150!")
        #stNum = takeLists[0]
        stNum = "20141226"
        year = stNum[:4]
        checkGdRequire(year)

    except Exception as e:
        error = e
        return str(error)

    return "Hello"

def initFunclist():
    funclist.append(("graduationAssessment", graduationAssessment))
    return

# Create your views here.
def index(request):
    str = "20141226"
    str2 = str[:4]


    return HttpResponse(str2)


def api(request, message):
    # TODO port is changing every time user sent. So make the way to distinguish user without port number.

    HOST = 'ec2-3-21-126-101.us-east-2.compute.amazonaws.com'
    PORT = 1024

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

