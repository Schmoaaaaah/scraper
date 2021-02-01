import json

import requests
from environs import Env


class api():
    def __init__(self):
        env = Env()
        env.read_env()
        mytoken = env("TOKEN")
        self.url = "https://schmoaaaaah.r4nd0.de/api/"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(mytoken)
        }

    def request_post(self, endpoint, insert):
        try:
            r = requests.post(self.url + endpoint, json=insert, headers=self.headers).json()
            return r
        except Exception as e:
            print('Post failed: ' + str(e))

    def request_post_img(self, endpoint, file):
        try:
            r = requests.post(self.url + endpoint, files=file, headers=self.headers).json()
            return r
        except Exception as e:
            print('Post failed: ' + str(e))

    def request_get(self, endpoint, elementid=None):
        try:
            if elementid is None:
                print('getting data without id.')
                rjson = requests.get(self.url + endpoint, headers=self.headers).json()
                if rjson == []:
                    return rjson
                else:
                    return json.load(rjson)
            else:
                print('getting data with id: ' + str(elementid))
                return json.load(requests.get(self.url + endpoint + '/' + elementid, headers=self.headers).json())
        except Exception as e:
            print('Get failed beacause: ' + str(e))

    def request_put(self, endpoint, elementid, insert):
        try:
            r = requests.put(self.url + endpoint + elementid, json=insert, headers=self.headers).json()
            return r
        except Exception as e:
            print('Put failed: ' + str(e))
