import os

import firebase_admin
from firebase_admin import credentials, firestore


class Firebase:
    def __init__(self):
        cred = credentials.Certificate("./serviceAccountKey.json")
        self.default_app = firebase_admin.initialize_app(cred)

    def get_client(self):
        return firestore.client()
