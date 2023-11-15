from enum import Enum
import json


class MessageType(str, Enum):
    PUBLISH = "PUBLISH"
    FETCH = "FETCH"
    DISCOVER = "DISCOVER"
    PING = "PING"
    DISCONNECT = "DISCONNECT"
    INIT = "INIT"
    NOTIFY = "NOTIFY"


class Message:
    def __init__(self, type, msg):
        self.type = type
        self.msg = msg

    def serialize_message(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize_message(str):
        msg_dict = json.loads(str)
        return Message(msg_dict["type"], msg_dict["msg"])
