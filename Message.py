from enum import Enum
import json
import base64


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
        return Message(
            msg_dict["type"], msg_dict["msg"], msg_dict["status"], msg_dict["adr"]
        )

    def image_to_json(self):
        return json.dump(self.__dict__)

    @staticmethod
    def json_to_message(json_str):
        try:
            msg_dict = json.loads(json_str)  # Use json.loads() instead of json.load()
            return Message(
                msg_dict["type"], msg_dict["msg"], msg_dict["status"], msg_dict["adr"]
            )
        except Exception as e:
            return Message(MessageType.RESPONSEFILE, str(e), Status.FAILURE)
