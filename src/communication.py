import requests
from requests.exceptions import RequestException

from comsConstants import BASE_URL, TOKEN_FIELD, AUTH_ENDPOINT, AUTH_EMAIL, AUTH_PASSWORD


class ApiCaller:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
        except RequestException as e:
            print(f"Errore nella richiesta GET: {e}")
            return None
        return response.json()

    def post(self, endpoint, data=None):
        try:
            response = requests.post(f"{self.base_url}/{endpoint}", json=data)
            response.raise_for_status()
        except RequestException as e:
            print(f"Errore nella richiesta: {e}")
            return None
        return response.json()

    def put(self, endpoint, data=None):
        try:
            response = requests.put(f"{self.base_url}/{endpoint}", json=data)
            response.raise_for_status()
        except RequestException as e:
            print(f"Errore nella richiesta: {e}")
            return None
        return response.json()

    def update(self, endpoint, data=None):
        try:
            response = requests.patch(f"{self.base_url}/{endpoint}", json=data)
            response.raise_for_status()
        except RequestException as e:
            print(f"Errore nella richiesta: {e}")
            return None
        return response.json()

    def delete(self, endpoint):
        try:
            response = requests.delete(f"{self.base_url}/{endpoint}")
            response.raise_for_status()
        except RequestException as e:
            print(f"Errore nella richiesta: {e}")
            return None
        return response.json()


class PayloadCommunication:

    def __init__(self):
        self.api = ApiCaller(BASE_URL)
        self.__token = None
        self.__resource = None

    def login(self, email, password):
        response = self.api.post(AUTH_ENDPOINT, {AUTH_EMAIL: email, AUTH_PASSWORD: password})
        if response is None:
            print("Errore nel login.")
            return False
        self.__token = response[TOKEN_FIELD]
        return True

    def get_token(self):
        return self.__token

    def do(self, method, endpoint, data=None):
        if method == "GET":
            return self.api.get(endpoint, data)
        elif method == "POST":
            return self.api.post(endpoint, data)
        elif method == "PUT":
            return self.api.put(endpoint, data)
        elif method == "PATCH":
            return self.api.update(endpoint, data)
        elif method == "DELETE":
            return self.api.delete(endpoint)
        else:
            print("Not valid method. Use GET, POST, PUT, PATCH or DELETE.")
            return None

    def notify_payload_start(self):
        return self.do("POST", "payload/start", {"token": self.__token})

    def notify_payload_end(self):
        return self.do("POST", "payload/end", {"token": self.__token})

    def notify_payload_error(self, error):
        return self.do("POST", "payload/error", {"token": self.__token, "error": error})

    def get_resource(self, email):
        self.__resource = self.do("GET", "resource", {"email": email})