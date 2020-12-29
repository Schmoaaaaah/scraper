from instagrapi import Client


def fixjsonoffollow(wrongdict):
    listfollower = []
    for key in wrongdict:
        user = wrongdict[key].dict()
        listfollower.append(user)
    print('Converted dict to list')
    return listfollower


class Instascrapertofirebase():
    insta_instance = 0

    def __init__(self, instauser, instapas, db):
        Instascrapertofirebase.insta_instance += 1
        self.insta = Client()
        self.insta_user = instauser
        self.insta_pas = instapas
        self.insta.login(self.insta_user, self.insta_pas)
        self.userid = self.insta.user_id_from_username(self.insta_user)
        print("Created Instance number: " + str(
            Instascrapertofirebase.insta_instance) + " with Parameters User: " + self.insta_user + " Pas: " + self.insta_pas)
        self.db = db

    def __del__(self):
        Instascrapertofirebase.insta_instance -= 1

    def get_ownprofile(self):  # returns user profile as json
        print('Getting data for user: ' + self.insta_user)
        user = self.insta.user_info(self.userid).dict()
        data = {
            'pk': user['pk'],
            'username': user['username'],
            'name': user['full_name'],
            'profilepic': user['profile_pic_url'],
            'follower': user['follower_count'],
            'bio': user['biography']
        }
        print('Got userdata')
        collname = 'insta_' + self.insta_user + '_ownprofile'
        self.trydeletecoll(collname)
        self.db.collection(collname).document(str(user['pk'])).set(data)
        print("Inserted ownprofile with name: "+user['username']+" in the database")
        return user

    def get_followers(self):  # returns followers of user as json
        print('Getting followers')
        follower = self.insta.user_followers(self.userid)
        print('Got followers')
        followerlist = fixjsonoffollow(follower)
        collname = 'insta_' + self.insta_user + '_follower'
        self.trydeletecoll(collname)
        for follow in followerlist:
            data = {
                'pk': follow['pk'],
                'username': follow['username'],
                'name': follow['full_name'],
                'profilepic': follow['profile_pic_url']
            }
            self.db.collection(collname).document(str(follow['pk'])).set(data)
            print("inserted row from follower: " + follow['username'])
        print("inserted follower of user in the database")
        return follower

    def get_following(self):  # returns people user follows as json
        print('Getting people you follow')
        following = self.insta.user_following(self.userid)
        print('Got people you follow')
        followinglist = fixjsonoffollow(following)
        collname = 'insta_' + self.insta_user + '_following'
        self.trydeletecoll(collname)
        for follow in followinglist:
            data = {
                'pk': follow['pk'],
                'username': follow['username'],
                'name': follow['full_name'],
                'profilepic': follow['profile_pic_url']
            }
            self.db.collection(collname).document(str(follow['pk'])).set(data)
            print("inserted row from followin: " + follow['username'])
        print("Inserted people that follow user in the database")
        return following

    def get_posts(self):  # list of posts as json
        print('Getting posts')
        posts = self.insta.user_medias(self.userid)
        print('got posts')
        collname = 'insta_' + self.insta_user + '_post'
        self.trydeletecoll(collname)
        for media in posts:
            dic = media.dict()
            data = {
                'pk': dic['pk'],
                'caption': dic['caption_text'],
                'commentscount': dic['comment_count'],
                'likes': dic['like_count'],
                'date': dic['taken_at'],
                'resources': dic['resources'],
                'thumbnail': dic['thumbnail_url'],
                'video': dic['video_url'],
                'videodur': dic['video_duration']
            }
            self.db.collection(collname).document(str(dic['pk'])).set(data)
            print("Inserted row of post with caption: " + dic['caption_text'])
        print("inserted posts into the database")
        return posts

    def get_all(self):
        self.get_ownprofile()
        self.get_followers()
        self.get_following()
        self.get_posts()

    def trydeletecoll(self, collname):
        try:
            docs = self.db.collection(collname).stream()
            for doc in docs:
                doc.reference.delete()
        except:
            print('Collum: ' + collname + ' doesn`t exist')
