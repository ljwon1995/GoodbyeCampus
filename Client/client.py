import socket


HOST = 'localhost'
PORT = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('', 0))
client_socket.connect((HOST, PORT))



name = 'Jaewon'
msg = ":build Harry reset"
bot = "HARRY"

data = name + chr(0) + bot + chr(0) + msg + chr(0);

client_socket.send(data.encode());


data = client_socket.recv(10000);
print('bot : ', data.decode());



print("Conversation Started");
msg = ""


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('', 0))
client_socket.connect((HOST, PORT))


data = name + chr(0) + bot + chr(0) + msg + chr(0);
client_socket.send(data.encode());

data = client_socket.recv(10000);
print('bot : ', data.decode());






while(1):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('', 0))
    client_socket.connect((HOST, PORT))

    msg = input();
    data = name + chr(0) + bot + chr(0) + msg + chr(0);
    client_socket.send(data.encode());
    print('You : ', msg);
    data = client_socket.recv(10000)
    print('bot : ', data.decode())
    client_socket.close();

