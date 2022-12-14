
import datetime
import requests
import json


auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
basic_url = "https://tdx.transportdata.tw/api/basic"


class TDX(object):
    def __init__(self, app_id, app_key) -> None:
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = None

    def get_bus_route(self, city, route_no):
        url = f"{basic_url}/v2/Bus/Route/City/{city}" + \
            f"?$filter=RouteName/En eq '{route_no}'&$top=1&$format=JSON"

        resp = requests.get(url, headers=self.__data_header())

        return resp.json() or []

    def get_bus_estimate_time(self, city, route, stop_id):
        url = f"{basic_url}/v2/Bus/EstimatedTimeOfArrival/City/{city}" + \
            f"/{route}?$filter=StopID eq '{stop_id}'&$top=1&$format=JSON"

        resp = requests.get(url, headers=self.__data_header())

        estimate = resp.json()[0]

        stop_name = estimate["StopName"]["Zh_tw"]

        # seconds
        estimate_time = estimate["EstimateTime"]

        last_update_time = datetime.datetime.strptime(
            estimate["SrcUpdateTime"], "%Y-%m-%dT%H:%M:%S%z")

        diff = datetime.datetime.now().astimezone() - last_update_time
        seconds = estimate_time - diff.total_seconds()
    
        return {
            "stop_name": stop_name,
            "estimate_seconds": seconds,
            "estimate_time": self.__time_format(seconds)
        }

    def __auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return{
            'content-type': content_type,
            'grant_type': grant_type,
            'client_id': self.app_id,
            'client_secret': self.app_key
        }

    def __data_header(self):
        access_token = self.__auth_token()

        return{'authorization': f'Bearer {access_token}'}

    def __auth_token(self):
        if not self.auth_response:
            self.auth_response = requests.post(auth_url, self.__auth_header())

        return json.loads(self.auth_response.text).get('access_token')

    def __time_format(self, total_seconds):
        minute = total_seconds // 60

        seconds = total_seconds - minute * 60

        result = ""

        if minute > 0:
            result += f"{minute:0.0f}分"

        return f"{result}{seconds:0.0f}秒"
