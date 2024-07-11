import requests
from requests.exceptions import RequestException

from comsConstants import *


class ApiCaller:
    def __init__(self, base_url):
        self.base_url = base_url

    def _get_url(self, endpoint, port):
        if port:
            url = f"{self.base_url}:{port}/{endpoint}"
        else:
            url = f"{self.base_url}/{endpoint}"

        return url

    def get(self, endpoint, port="", token=None, params=None):
        url = self._get_url(endpoint, port)
        try:
            response = requests.get(url, params=params,
                                    headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
        except RequestException as e:
            print(f"Errore nella richiesta GET: {e}")
            return None
        return response.json()

    def post(self, endpoint, port="", token=None, data=None):
        url = self._get_url(endpoint, port)
        try:
            response = requests.post(url, json=data,
                                     headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
            response.raise_for_status()
        except RequestException as e:
            print(f"Errore nella richiesta: {e}")
            return None
        return response.json()

    def put(self, endpoint, port="", token=None, data=None):
        url = self._get_url(endpoint, port)
        try:
            response = requests.put(url, json=data,
                                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
            response.raise_for_status()
        except RequestException as e:
            print(f"Errore nella richiesta: {e}")
            return None
        return response.json()

    def update(self, endpoint, port="", token=None, data=None):
        url = self._get_url(endpoint, port)
        try:
            response = requests.put(url, json=data,
                                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
            response.raise_for_status()
        except RequestException as e:
            print(f"Errore nella richiesta: {e}")
            return None
        return response.json()


class PayloadCommunication:

    def __init__(self, resource_id: str = "", email: str = ""):
        self.api = ApiCaller(BASE_URL)
        self.__token = None
        self.__resource = None
        self.__resource_id = resource_id
        self.__email = email

    def login(self, password):
        response = self.api.post(AUTH_ENDPOINT, AUTH_PORT, "", {AUTH_EMAIL: self.__email, AUTH_PASSWORD: password})
        if response is None:
            print("Errore nel login.")
            return False
        self.__token = response[TOKEN_FIELD]
        return True

    def get_token(self):
        return self.__token

    def do(self, method, endpoint, port="", token=None, data=None):
        if method == "GET":
            return self.api.get(endpoint, port, token, data)
        elif method == "POST":
            return self.api.post(endpoint, port, token, data)
        elif method == "PUT":
            return self.api.put(endpoint, port, token, data)
        elif method == "PATCH":
            return self.api.update(endpoint, port, token, data)
        else:
            print("Not valid method. Use GET, POST, PUT, PATCH or DELETE.")
            return None

    def notify_payload_start(self):
        return self.do("POST", ASSIGNMENT_NOTIFY_ENDPOINT, ASSIGNMENT_NOTIFY_PORT, self.__token, {"assignedResourceId": self.__resource_id, "memberEmail": self.__email, "start": True, "stop": False})

    def notify_payload_end(self):
        return self.do("POST", ASSIGNMENT_NOTIFY_ENDPOINT, ASSIGNMENT_NOTIFY_PORT, self.__token,
                       {"assignedResourceId": self.__resource_id, "memberEmail": self.__email, "stop": True})

    def get_resource(self):
        response =  self.do("POST", RESOURCE_ENDPOINT, RESOURCE_PORT, self.__token, {"assignedResourceId": self.__resource_id, "memberEmail": self.__email})
        if response is not None:
            hardware_name = response['hardwareName']
        else:
            hardware_name = ""
        return hardware_name
