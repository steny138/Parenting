from .event_type import EventType
from ..utility import now_timestamp, to_timestamp
import os
import json
import requests
import logging
import uuid

logger = logging.getLogger(__name__)


class Itofoo(object):

    ITOFOO_DOMAIN = "https://service.itofoo.com"
    ITOFOO_AUTH = "/auth/service"
    ITOFOO_KIDSRUN = "/kidsrun/service"
    __header = {
        "screen": "375.0*812.0*3.0",
        "system": "iOS/15.5",
        "device": "iPhone",
        "app": "com.zeon.GuardianCare/11.6",
        "version": "7.8"
    }
    BABYID = os.getenv("IToFooBabyId")

    def __init__(self, username, password):
        self.user_name = username
        self.password = password

        self._session = requests.Session()
        self._session.auth = (
            "com.zeon.toddlercare-guardiancare", "zeon.@itp.itofoo")
        self.__login()

    def __del__(self):
        self._session.close()

    def user_info(self):
        payload = {
            "request": "QUERYUSERINFO",
            "parameters": {

            },
            "header": self.__header
        }

        resp = self._session.post(
            f'{self.ITOFOO_DOMAIN}{self.ITOFOO_AUTH}', json=payload)

        return resp.json()

    def baby_info(self):
        payload = {
            "request": "QUERYBABY",
            "parameters": {

            },
            "header": self.__header
        }
        resp = self._session.post(
            f'{self.ITOFOO_DOMAIN}{self.ITOFOO_KIDSRUN}', json=payload)

        return resp.json()

    def pickup_baby(self):
        files = {
            'parameters': (None, json.dumps({
                "time": {
                    "utc": now_timestamp()
                },
                "tag": 0,
                "eventuuid": str(uuid.uuid4()),  # 預告接小孩事件
                "event": {
                    "guardianrelation": "Dad",
                    "minutesarrive": 15,
                    "type": 45,
                    "pickuptime": {
                        "utc": to_timestamp(15)  # 預計到達接送時間
                    }
                },
                "babyid": self.BABYID,
                "type": 45
            })),
            'header': (None, json.dumps(self.__header)),
        }
        resp = self._session.post(
            f'{self.ITOFOO_DOMAIN}/event/add', files=files)

        logging.debug(resp.json())

        return resp.json()

    def baby_departure(self):
        return self.__qrcode_event(EventType.Departure)

    def baby_arrivals(self):
        return self.__qrcode_event(EventType.Arrivals)

    def __login(self):
        payload = {
            "request": "LOGIN",
            "parameters": {
                "app": "com.zeon.GuardianCare",
                "username": self.user_name,
                "password": self.password
            },
            "header": self.__header
        }

        resp = self._session.post(
            f'{self.ITOFOO_DOMAIN}/auth/login', json=payload)

        logger.debug(resp.json())

    def __qrcode_event(self, type):
        payload = {
            "request": "ADDBABYEVENT",
            "parameters": {
                "time": {
                    "utc": now_timestamp()
                },
                "event": {
                    "type": type,
                    "guardian": "Dad"
                },
                "babyid": self.BABYID,
                "type": type
            },
            "header": self.__header
        }

        resp = self._session.post(
            f'{self.ITOFOO_DOMAIN}/v1/qrcode/kindergarten/952/20210721/',
            json=payload,
            params={"action": "addbabyevent"})

        logging.debug(resp.json())

        return resp.json()
