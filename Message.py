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

    @staticmethod
    def image_to_json(file_path):
        try:
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            return Message(
                MessageType.RESPONSEFILE, encoded_string, Status.SUCCESS
            ).serialize_message()
        except Exception as e:
            return Message(
                MessageType.RESPONSEFILE, str(e), Status.FAILURE
            ).serialize_message()

    @staticmethod
    def json_to_message(json_str):
        try:
            msg_dict = json.loads(json_str)
            return Message(
                msg_dict["type"], msg_dict["msg"], msg_dict["status"], msg_dict["adr"]
            )
        except Exception as e:
            return Message(MessageType.RESPONSEFILE, str(e), Status.FAILURE)
