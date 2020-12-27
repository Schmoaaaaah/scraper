from instagrapi import Client


def fixjsonoffollow(wrongdict):
    listfollower = []
    for key in wrongdict:
        user = wrongdict[key].dict()
        listfollower.append(user)
    print('Converted dict to list')
    return listfollower


class Instascrapertomongo():
    insta_instance = 0

    def __init__(self, instauser, instapas, db):
        Instascrapertomongo.insta_instance += 1
        self.insta = Client()
        self.insta_user = instauser
        self.insta_pas = instapas
        self.insta.login(self.insta_user, self.insta_pas)
        self.userid = self.insta.user_id_from_username(self.insta_user)
        print("Created Instance number: " + str(
            Instascrapertomongo.insta_instance) + " with Parameters User: " + self.insta_user + " Pas: " + self.insta_pas)
        self.db = db

    def __del__(self):
        Instascrapertomongo.insta_instance -= 1

    def get_ownprofile(self):  # returns user profile as json
        print('Getting data for user: ' + self.insta_user)
        user = self.insta.user_info(self.userid).dict()
        print('Got userdata')
        collname = 'insta_' + self.insta_user + '_ownprofile'
        coll = self.db[collname]
        self.trydeletecoll(coll, collname)
        coll.insert_one(user)
        print("Inserted ownprofile in the database")
        return user

    def get_followers(self):  # returns followers of user as json
        print('Getting followers')
        follower = self.insta.user_followers(self.userid)
        print('Got followers')
        followerlist = fixjsonoffollow(follower)
        collname = 'insta_' + self.insta_user + '_follower'
        coll = self.db[collname]
        self.trydeletecoll(coll, collname)
        for follow in followerlist:
            coll.insert_one(follow)
        print("inserted follower of user in the database")
        return follower

    def get_following(self):  # returns people user follows as json
        print('Getting people you follow')
        following = self.insta.user_following(self.userid)
        print('Got people you follow')
        followinglist = fixjsonoffollow(following)
        collname = 'insta_' + self.insta_user + '_following'
        coll = self.db[collname]
        self.trydeletecoll(coll, collname)
        for follow in followinglist:
            coll.insert_one(follow)
        print("Inserted people that follow user in the database")
        return following

    def get_posts(self):  # list of posts as json
        print('Getting posts')
        posts = self.insta.user_medias(self.userid)
        print('got posts')
        collname = 'insta_' + self.insta_user + '_post'
        coll = self.db[collname]
        self.trydeletecoll(coll, collname)
        for media in posts:
            coll.insert_one(media.dict())
        print("inserted posts into the database")
        return posts

    def get_all(self):
        self.get_ownprofile()
        self.get_followers()
        self.get_following()
        self.get_posts()

    def trydeletecoll(self, coll, collname):
        try:
            coll.drop()
        except:
            print('Collum: ' + collname + ' doesn`t exist')
