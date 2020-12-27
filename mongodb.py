from pymongo import MongoClient

class mongodb():
    def __init__(self,env):
        self.user = env("DB_USER")
        self.pas = env("DB_PASSWORD")
        self.adr = env("DB_HOST")
        self.port = env("DB_PORT")
        self.db = env("DB_NAME")
        self.auth = env("DB_AUTHDB")

    def get_connection(self):
        url = "mongodb://" + self.user + ":" + self.pas + "@" + self.adr + ":" + self.port + "/" + self.db + "?authSource=" + self.auth
        client = MongoClient(url)
        database = client.backend
        return database
