import threading
from Message import Message, MessageType


SIZE = 1024

repositories = []


def exist(repos):
    pass


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
                repositories.append(
                    [
                        self.username,
                        fileparts[0],
                        fileparts[1],
                    ]
                )
            elif message.type == MessageType.FETCH:
                print(f"Client {self.username} fetched file {message.msg}")
                if exist(repositories):
                    pass
                else:
                    self.csocket.sendall(
                        Message(MessageType.NOTIFY, "file not found")
                        .serialize_message()
                        .encode()
                    )
            elif message.type == MessageType.DISCONNECT:
                print(f"Client {self.username} disconnected")
                self.csocket.close()
                break
            else:
                print("Invalid")
            self.csocket.send(bytes(msg, "UTF-8"))

    def repos(self):
        return repositories
