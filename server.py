from socket import *
from Message import Message, MessageType
from ClientThread import ClientThread as CThread
import threading

PORT = 12000
SIZE = 1024

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", PORT))
print("The server is listening...")

while True:
    serverSocket.listen(1)
    client_sock, client_address = serverSocket.accept()

    message = Message.deserialize_message(client_sock.recv(SIZE).decode())
    if message.type == MessageType.INIT:
        print(f"Client {message.msg} connected from {client_address}")

    new_thread = CThread(client_address, client_sock, message.msg)
    new_thread.start()
