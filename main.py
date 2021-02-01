
from insta import Instascraper
from environs import Env


def main():
    env = Env()
    env.read_env()
    Instascraper('schmoaaaaah', 'Noah2014').get_ownprofile()
    # while True:
    #    instagram(env)
    #    sleep(86400)


def instagram(env):
    accounts = {}
    for i in range(len(env.list("INSTA_USER"))):
        accounts['user' + str(i)] = [env.list("INSTA_USER")[i], env.list("INSTA_PAS")[i],
                                     Instascraper(env.list("INSTA_USER")[i], env.list("INSTA_PAS")[i])]
    for key in accounts:
        accounts[key][2].get_all()


main()
