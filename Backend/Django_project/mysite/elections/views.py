from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect, Http404
from django.http import JsonResponse
import datetime
import socket

# Create your views here.
def index(request):
    str = "server started"
    return HttpResponse(str)


def api(request, message):

        HOST = 'ec2-3-21-126-101.us-east-2.compute.amazonaws.com'
        PORT = 1024

        if(message == 'start'):
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.bind(('', 0))
                client_socket.connect((HOST, PORT))

                name = 'Jaewon'
                msg = ":build Goodcam reset"
                bot = "HARRY"

                data = name + chr(0) + bot + chr(0) + msg + chr(0);
                client_socket.send(data.encode())
                data = client_socket.recv(50000).decode()

                client_socket.close()

                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.bind(('', 0))
                client_socket.connect((HOST, PORT))

                msg = ""

                data = name + chr(0) + bot + chr(0) + msg + chr(0);
                client_socket.send(data.encode());

                data = client_socket.recv(10000).decode();




                return JsonResponse({
                        'message': 1,
                        'content':  data
                        })



            

        print('user message = ', message)

	#to the chatbot(message)
	#result = message.upper()





        print("Conversation Started");

        name = 'Jaewon'
        bot = "HARRY"


        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind(('', 0))
        client_socket.connect((HOST, PORT))


        data = name + chr(0) + bot + chr(0) + message + chr(0);
        client_socket.send(data.encode());

        data = client_socket.recv(10000);
        print('bot : ', data.decode());
        data = data.decode()
        
        client_socket.close()
        return JsonResponse({
                'message': 1,
                'content':  data
                })
