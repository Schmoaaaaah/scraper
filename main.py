import os
from time import sleep

from mongodb import mongodb
from insta import Instascrapertomongo
from environs import Env


def main():
    env = Env()
    env.read_env()
    while True:
        instagram(env)
        sleep(86400)
    

def instagram(env):
    accounts = {}
    mongo = mongodb(env)
    db = mongodb.get_connection(mongo)
    for i in range(len(env.list("INSTA_USER"))):
        accounts['user' + str(i)] = [env.list("INSTA_USER")[i], env.list("INSTA_PAS")[i],
                                     Instascrapertomongo(env.list("INSTA_USER")[i], env.list("INSTA_PAS")[i], db)]
    for key in accounts:
        accounts[key][2].get_all()


main()
