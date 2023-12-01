from socket import *
from Message import Message, MessageType, Status
import os
import threading
import random
import mimetypes
import base64
import json

IP = "localhost"
SERVER_PORT = 12000
CLIENT_PORT = random.randint(10000, 20000)
ADDR = (IP, SERVER_PORT)
SIZE = 1024576
FORMAT = "utf-8"


def fetch(fname, clientSocket):
    clientSocket.sendall(Message(MessageType.FETCH, fname).serialize_message().encode())

    result = Message.deserialize_message(clientSocket.recv(SIZE).decode())
    fileType = mimetypes.guess_type(result.msg[1])[0]

    if result.type == MessageType.NOTIFY:
        if result.status == "FAILURE":
            print(f"Fetching file is not exist")
        elif result.status == "SUCCESS":
            reqSocket = socket(AF_INET, SOCK_STREAM)

            print(f"Fetching {result.msg} from {result.adr}")
            try:
                reqSocket.connect((result.adr[0], result.adr[1]))  # IP, PORT
            except socket.error:
                print(f"Could not connect to client at {result.adr}")
                exit(1)
            reqSocket.sendall(
                Message(
                    MessageType.REQUESTFILE,
                    [
                        result.msg[0],
                        result.msg[1],
                        mimetypes.guess_type(result.msg[1])[0],
                    ],
                )  # File resporitory + file name
                .serialize_message()
                .encode()
            )
            if fileType == "text/plain":
                res = Message.deserialize_message(reqSocket.recv(SIZE).decode(FORMAT))
                if (
                    res.type == MessageType.RESPONSEFILE
                    and res.status == Status.SUCCESS
                ):
                    # with (fname, "w") as file:
                    #     file.write(res.msg)
                    # file.close()
                    file = open(fname, "w")
                    file.write(res.msg)
                    file.close()
                    print(f"Fetching file {fname} SUCCESSFUL")
                elif (
                    res.type == MessageType.RESPONSEFILE
                    and res.status == Status.FAILURE
                ):
                    print(f"Fetching file {fname} UNSUCCESSFUL")
            elif fileType == "image/jpeg" or fileType == "image/png":
                res = Message.json_to_message(reqSocket.recv(SIZE).decode())
                if (
                    res.type == MessageType.RESPONSEFILE
                    and res.status == Status.SUCCESS
                ):
                    with open(fname, "wb") as image_file:
                        # while True:
                        #     res = reqSocket.recv(SIZE)
                        #     if not res:
                        #         break
                        #     image_file.write(base64.b64decode(res))

                        image_file.write(base64.b64decode(res.msg))
                    print(f"Fetching image {fname} SUCCESSFUL")
                elif (
                    res.type == MessageType.RESPONSEFILE
                    and res.status == Status.FAILURE
                ):
                    print(f"Fetching image {fname} UNSUCCESSFUL")

            reqSocket.close()


def publish(lname, fname, clientSocket):
    if os.path.isdir(lname):
        if os.path.isfile(lname + "/" + fname):
            clientSocket.sendall(
                Message(MessageType.PUBLISH, [lname, fname])
                .serialize_message()
                .encode()
            )
        else:
            print(f"File {fname} does not exist in {lname}")
    else:
        print(f"Repository {lname} is invalid")


def disconnect(clientSocket):
    clientSocket.sendall(
        Message(MessageType.DISCONNECT, "goodbye").serialize_message().encode()
    )

    res = Message.deserialize_message(clientSocket.recv(SIZE).decode())
    if res.status == Status.SUCCESS:
        print("Disconnected from server")
        flag.login = False
        clientSocket.close()
        closeSocket = socket(AF_INET, SOCK_STREAM)
        try:
            closeSocket.connect((IP, CLIENT_PORT))
        except socket.error as e:
            print(f"Could not connect to server: {e}")
        closeSocket.sendall(
            Message(MessageType.DISCONNECT, "goodbye").serialize_message().encode()
        )
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
        print("Connected to server")
        threading.Thread(target=listening_from_client).start()
        flag.login = True
    else:
        print(res.msg)
        clientSocket.close()


class static:
    def __init__(self, login=False):
        self.login = login
        self.name = ""


flag = static()


def handle_commands():
    while 1:
        if not flag.login:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            name = input("Enter your name: ")
            init(name, clientSocket)
        else:
            if flag.name != "":
                print(f"You are logged in as {flag.name}")

        command = input("> ")
        command = command.split()
        if command:
            if command[0] == "disconnect" or command[0] == "d":
                disconnect(clientSocket)
            elif command[0] == "publish" or command[0] == "p":
                publish(command[1], command[2], clientSocket)
            elif command[0] == "fetch" or command[0] == "f":
                fetch(command[1], clientSocket)


def listening_from_client():
    while 1:
        global s2cSocket
        s2cSocket = socket(AF_INET, SOCK_STREAM)
        s2cSocket.bind(("", CLIENT_PORT))
        s2cSocket.listen(1)
        cSocket, caddr = s2cSocket.accept()

        message = Message.deserialize_message(cSocket.recv(SIZE).decode())
        if message.type == MessageType.REQUESTFILE:
            fileDir = message.msg[0] + "/" + message.msg[1]
            if os.path.isfile(fileDir):
                if message.msg[2] == "text/plain":
                    file = open(fileDir, "r")
                    msg = file.read()
                    file.close()
                    cSocket.sendall(
                        Message(MessageType.RESPONSEFILE, msg, Status.SUCCESS)
                        .serialize_message()
                        .encode()
                    )
                elif message.msg[2] == "image/jpeg" or message.msg[2] == "image/png":
                    with open(fileDir, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode()
                    # cSocket.sendall(encoded_string)
                    cSocket.sendall(
                        Message(
                            MessageType.RESPONSEFILE, encoded_string, Status.SUCCESS
                        )
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
