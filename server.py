from socket import *
from Message import Message, MessageType
from ClientThread import ClientThread as CThread
from ClientThread import *
import threading

PORT = 12000
SIZE = 1024

threads = []

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", PORT))
print("The server is listening...")

def discover(username):
    print("Repositories:")
    for data in repositories:
        if data[0] == username:
            print(data[1] + "/" + data[2])

    

def ping(username):
    pass

def stop():
    pass  


while True:
    serverSocket.listen(1)
    client_sock, client_address = serverSocket.accept()

    message = Message.deserialize_message(client_sock.recv(SIZE).decode())
    if message.type == MessageType.INIT:
        print(f"Client {message.msg} connected from {client_address}")

    user_thread = CThread(client_address, client_sock, message.msg)
    user_thread.start()
    threads.append(user_thread)

    command = input("> ")
    command = command.split()
    if command[0] == "discover" or command[0] == "d":
        discover(command[1])
    elif command[0] == "ping" or command[0] == "p":
        ping(command[1])
    elif command[0] == "stop" or command[0] == "s":
        stop()
    else:
        print("Command not found")
