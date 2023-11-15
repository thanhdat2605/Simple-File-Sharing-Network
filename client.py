from socket import *
from Message import Message, MessageType
import os


IP = "localhost"
PORT = 12000
ADDR = (IP, PORT)
SIZE = 1024

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)


def fetch(fname):
    pass

def publish(lname, fname):
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

def disconnect():
    clientSocket.sendall(
        Message(MessageType.DISCONNECT, "goodbye").serialize_message().encode()
    )
    clientSocket.close()
    exit()

msg = input("Enter your name: ")
clientSocket.sendall(Message(MessageType.INIT, msg).serialize_message().encode())
while True:
    command = input("> ")
    command = command.split()
    if command[0] == "disconnect" or command[0] == "d":
        disconnect()
    elif command[0] == "publish" or command[0] == "p":
        publish(command[1], command[2])
    elif command[0] == "fetch" or command[0] == "f":
        fetch(command[1])
