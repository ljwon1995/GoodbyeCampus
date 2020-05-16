from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect, Http404
from django.http import JsonResponse
import datetime
import socket


funclist = []



# Create your views here.
def index(request):
    str = "server started"
    return HttpResponse(str)


def api(request, message):
    # TODO port is changing every time user sent. So make the way to distinguish user without port number.

    HOST = 'ec2-3-21-126-101.us-east-2.compute.amazonaws.com'
    PORT = 1024

    ip = request.META.get('REMOTE_ADDR')
    port = request.META.get('REMOTE_PORT')

    name = ip + "/" + port

    if (message == 'start'):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind(('', 0))
        client_socket.connect((HOST, PORT))

        msg = ":reset"
        bot = "HARRY"

        data = name + chr(0) + bot + chr(0) + msg + chr(0);
        client_socket.send(data.encode())
        data = client_socket.recv(50000).decode()
        client_socket.close()
        data = "kkk"

        #                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #                client_socket.bind(('', 0))
        #                client_socket.connect((HOST, PORT))

        #                msg = ""
        #                bot = 'HARRY'
        #                data = name + chr(0) + bot + chr(0) + msg + chr(0);

        #                client_socket.send(data.encode())
        #                data = client_socket.recv(10000).decode();

        #                client_socket.close()

        return JsonResponse({
            'message': 1,
            'content': data
        })

    print('user message = ', message)

    # to the chatbot(message)
    # result = message.upper()

    print("Conversation Started");

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
    if type == 'f':
        fname = tokens[1]
        argList = tokens[2:]

        for func in funclist:
            if func[0] == fname:
                response = func[1](argList)

    elif type == 'u':
        response = tokens[1]

    else:
        response = "Error"

    client_socket.close()
    return JsonResponse({
        'message': 1,
        'content': response
    })

