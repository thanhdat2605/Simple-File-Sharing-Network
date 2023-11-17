from socket import *
from Message import Message, MessageType, Status
import random

# from ClientThread import CThread
import threading


class CThread(threading.Thread):
    def __init__(self, client_address, client_socket, username, adr):
        threading.Thread.__init__(self)
        self.csocket = client_socket
        self.caddress = client_address
        self.username = username
        self.adr = adr

    def run(self):
        msg = ""
        while True:
            try:
                message = Message.deserialize_message(self.csocket.recv(SIZE).decode())
                if message.type == MessageType.PUBLISH:
                    print(f"Client {self.username} published file {message.msg}")
                    fileparts = message.msg.split("\\")
                    repositories.append(
                        [
                            self.username,
                            fileparts[0],
                            fileparts[1],
                        ]
                    )
                elif message.type == MessageType.INIT:
                    print(f"Client {message.msg} connected from {self.caddress}")
                elif message.type == MessageType.FETCH:
                    print(f"Client {self.username} fetched file {message.msg}")
                    flag = False
                    for data in repositories:
                        if data[2] == message.msg:
                            flag = True
                            break
                    if flag:
                        self.csocket.sendall(
                            Message(
                                MessageType.NOTIFY,
                                [data[1], data[2]],
                                Status.SUCCESS,
                                self.adr,
                            )
                            .serialize_message()
                            .encode()
                        )
                    else:
                        self.csocket.sendall(
                            Message(MessageType.NOTIFY, data[2], Status.FAILURE)
                            .serialize_message()
                            .encode()
                        )
                elif message.type == MessageType.DISCONNECT:
                    print(f"Client {self.username} disconnected")
                    self.csocket.sendall(
                        Message(MessageType.DISCONNECT, "goodbye", Status.SUCCESS)
                        .serialize_message()
                        .encode()
                    )
                    for uthread in threads:
                        if uthread.username == self.username:
                            threads.remove(uthread)
                    self.csocket.close()
                    break
                else:
                    print("Invalid")
                self.csocket.send(bytes(msg, "UTF-8"))
            except:
                print(f"Client {self.username} disconnected")
                for uthread in threads:
                    if uthread.username == self.username:
                        threads.remove(uthread)
                    self.csocket.close()
                break


PORT = 12000
SIZE = 1024

stop = False

threads = []
repositories = []

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", PORT))
print("The server is listening...")


def discover(username):
    if isOnline(username):
        print("Repositories:")
        for data in repositories:
            if data[0] == username:
                print(data[1] + "/" + data[2])
    else:
        print(f"Client {username} is offline")


def ping(username):
    if isOnline(username):
        print(f"Client {username} is online")
    else:
        print(f"Client {username} is offline")


def isOnline(username):
    for user in threads:
        if user.username == username:
            return True
    return False


def handle_commands():
    while 1:
        command = input("> ")
        command = command.split()
        if command[0] == "discover" or command[0] == "d":
            discover(command[1])
        elif command[0] == "ping" or command[0] == "p":
            ping(command[1])
        elif command[0] == "stop" or command[0] == "s":
            pass
        else:
            print("Command not found")


def listening():
    while 1:
        serverSocket.listen(2)
        client_sock, client_address = serverSocket.accept()
        message = Message.deserialize_message(client_sock.recv(SIZE).decode())
        if message.type == MessageType.INIT:
            if isOnline(message.msg):
                client_sock.sendall(
                    Message(
                        MessageType.INIT,
                        "Username already exists",
                        Status.FAILURE,
                        message.adr,
                    )
                    .serialize_message()
                    .encode()
                )
                continue
            print(f"Client {message.msg} connected from {client_address}")
            client_sock.sendall(
                Message(MessageType.INIT, "", Status.SUCCESS)
                .serialize_message()
                .encode()
            )
        user_thread = CThread(client_address, client_sock, message.msg, message.adr)
        user_thread.start()
        threads.append(user_thread)


threading.Thread(target=handle_commands).start()
threading.Thread(target=listening).start()
