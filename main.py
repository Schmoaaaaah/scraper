import os
from time import sleep

from firebase import Firebase
from mongodb import mongodb
from insta import Instascrapertofirebase
from environs import Env


def main():
    env = Env()
    env.read_env()
    Firebase()
    while True:
        instagram(env, Firebase.get_client(Firebase))
        sleep(86400)
    

def instagram(env, db):
    accounts = {}
    for i in range(len(env.list("INSTA_USER"))):
        accounts['user' + str(i)] = [env.list("INSTA_USER")[i], env.list("INSTA_PAS")[i],
                                     Instascrapertofirebase(env.list("INSTA_USER")[i], env.list("INSTA_PAS")[i], db)]
    for key in accounts:
        accounts[key][2].get_all()


main()
