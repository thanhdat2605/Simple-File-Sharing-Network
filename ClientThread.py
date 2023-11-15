import threading
from Message import Message, MessageType

SIZE = 1024

repositories = {}


class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket, username):
        threading.Thread.__init__(self)
        self.csocket = client_socket
        self.caddress = client_address
        self.username = username

    def run(self):
        msg = ""
        while True:
            message = Message.deserialize_message(self.csocket.recv(SIZE).decode())
            if message.type == MessageType.PUBLISH:
                print(f"Client {self.username} published file {message.msg}")
                fileparts = message.msg.split("\\")
                if len(repositories[self.username]) != 0:
                    repositories[self.username] = {}
                repositories[self.username][fileparts[1]] = fileparts[0]
            elif message.type == MessageType.FETCH:
                pass
            elif message.type == MessageType.DISCONNECT:
                print(f"Client {self.username} disconnected")
                self.csocket.close()
                break
            else:
                print("Invalid")
            print("from client", msg.upper())
            self.csocket.send(bytes(msg, "UTF-8"))

    def repos(self):
        return repositories
