from socket import *
from Message import Message, MessageType, Status
import os
import threading
import random

IP = "localhost"
SERVER_PORT = 12000
CLIENT_PORT = random.randint(10000, 20000)
ADDR = (IP, SERVER_PORT)
SIZE = 1024
FORMAT = "utf-8"


def fetch(fname, clientSocket):
    clientSocket.sendall(Message(MessageType.FETCH, fname).serialize_message().encode())

    result = Message.deserialize_message(clientSocket.recv(SIZE).decode())
    if result.type == MessageType.NOTIFY:
        if result.status == "FAILURE":
            print(f"{result.msg[1]} is not exist")
        elif result.status == "SUCCESS":
            reqSocket = socket(AF_INET, SOCK_STREAM)

            print(f"fetching {result.msg}from {result.adr}")
            try:
                reqSocket.connect((result.adr[0], result.adr[1]))
            except socket.error:
                print(f"Could not connect to client at {result.adr}")
                exit(1)
            reqSocket.sendall(
                Message(MessageType.REQUESTFILE, result.msg[0] + "/" + result.msg[1])
                .serialize_message()
                .encode()
            )

            res = Message.deserialize_message(reqSocket.recv(SIZE).decode(FORMAT))
            if res.type == MessageType.RESPONSEFILE and res.status == Status.SUCCESS:
                file = open(result.msg[1], "w")
                file.write(res.msg)
                file.close()
            elif res.type == MessageType.RESPONSEFILE and res.status == Status.FAILURE:
                print("read file unsuccessful")


def publish(lname, fname, clientSocket):
    if os.path.isdir(lname):
        if os.path.isfile(lname + "/" + fname):
            clientSocket.sendall(
                Message(MessageType.PUBLISH, lname + "\\" + fname)
                .serialize_message()
                .encode()
            )
        else:
            print("file is not exist")
    else:
        print("directory is not exist")


def disconnect(clientSocket):
    clientSocket.sendall(
        Message(MessageType.DISCONNECT, "goodbye").serialize_message().encode()
    )

    res =Message.deserialize_message(clientSocket.recv(SIZE).decode())
    if res.status == Status.SUCCESS:
        print("disconnected from server")
        flag.login = False    
        clientSocket.close()
        closeSocket = socket(AF_INET, SOCK_STREAM)
        try:
            closeSocket.connect((IP,CLIENT_PORT))
        except socket.error as e:
            print(f"Could not connect to server: {e}")
        closeSocket.sendall(Message(MessageType.DISCONNECT, "goodbye").serialize_message().encode())
        closeSocket.close()
    exit()


def init(username, clientSocket):
    try:
        clientSocket.connect(ADDR)
    except socket.error as e:
        print(f"Could not connect to server: {e}")
        exit()

    clientSocket.sendall(
        Message(MessageType.INIT, username, Status.SUCCESS, (IP, CLIENT_PORT))
        .serialize_message()
        .encode()
    )

    res = Message.deserialize_message(clientSocket.recv(SIZE).decode())
    if res.status == Status.SUCCESS:
        print("connected to server")
        threading.Thread(target=listening_from_client).start()
        flag.login = True
    else:
        print(res.msg)
        clientSocket.close()


class static:
    def __init__(self, login=False):
        self.login = login


flag = static()


def handle_commands():
    while 1:
        command = input("> ")
        command = command.split()
        if command[0] == "disconnect" or command[0] == "d":
            disconnect(clientSocket)
        elif command[0] == "init" or command[0] == "i":
            if not flag.login:
                clientSocket = socket(AF_INET, SOCK_STREAM)
                init(command[1], clientSocket)
            else:
                print("you are already logged in")
        elif command[0] == "publish" or command[0] == "p":
            publish(command[1], command[2], clientSocket)
        elif command[0] == "fetch" or command[0] == "f":
            fetch(command[1], clientSocket)


def listening_from_client():
    global s2cSocket 
    s2cSocket= socket(AF_INET, SOCK_STREAM)
    s2cSocket.bind(("", CLIENT_PORT))
    s2cSocket.listen(1)
    cSocket, caddr = s2cSocket.accept()

    message = Message.deserialize_message(cSocket.recv(SIZE).decode())
    if message.type == MessageType.REQUESTFILE:
        if os.path.isfile(message.msg):
            file = open(message.msg, "r")
            msg = file.read()
            file.close()
            cSocket.sendall(
                Message(MessageType.RESPONSEFILE, msg, Status.SUCCESS)
                .serialize_message()
                .encode()
            )
        else:
            cSocket.sendall(
                Message.serialize_message(
                    MessageType.RESPONSEFILE, "", Status.FAILURE
                ).encode()
            )
    s2cSocket.close()
    cSocket.close()


threading.Thread(target=handle_commands).start()