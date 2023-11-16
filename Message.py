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
    REQUESTFILE = "REQUESTFILE"
    RESPONSEFILE = "RESPONSEFILE"


class Status(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class Message:
    def __init__(self, type, msg, status=Status.SUCCESS, adr=()):
        self.type = type
        self.msg = msg
        self.status = status
        self.adr = adr

    def serialize_message(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize_message(str):
        msg_dict = json.loads(str)
        return Message(msg_dict["type"], msg_dict["msg"], msg_dict["status"],msg_dict["adr"])
