import base64
import json

from instagrapi import Client

from api import api


def encodepicture(path):
    with open(path, 'rb')as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    print('converted profile pic: ' + str(encoded_image))
    return encoded_image


def fixjsonoffollow(wrongdict):
    listfollower = []
    for key in wrongdict:
        user = wrongdict[key].dict()
        listfollower.append(user)
    print('Converted dict to list')
    return listfollower


class Instascraper():
    insta_instance = 0

    def __init__(self, instauser, instapas):
        Instascraper.insta_instance += 1
        settings = {
            "cookies": {},  # set here your saved cookies
            "device_settings": {
                "cpu": "h1",
                "dpi": "640dpi",
                "model": "h1",
                "device": "RS988",
                "resolution": "1440x2392",
                "app_version": "173.0.0.21.120",
                "manufacturer": "LGE/lge",
                "version_code": "168361634",
                "android_release": "11",
                "android_version": 30
            },
            "user_agent": "Instagram 173.0.0.21.120 Android (30/11; ...DE; 168361634)"
        }
        self.insta = Client(settings)
        self.insta_user = instauser
        self.insta_pas = instapas
        self.insta.login(self.insta_user, self.insta_pas)
        self.userid = self.insta.user_id_from_username(self.insta_user)
        print("Created Instance number: " + str(
            Instascraper.insta_instance) + " with Parameters User: " + self.insta_user + " Pas: " + self.insta_pas)
        self.db = api()

    def __del__(self):
        Instascraper.insta_instance -= 1

    def get_ownprofile(self):  # returns user profile as dict
        print('Getting data for user: ' + self.insta_user)
        user = self.insta.user_info(self.userid).dict()
        print('start convert profilepic')
        picturepath = self.insta.photo_download_by_url(user['profile_pic_url'], 'profilepic', './pictures')
        try:
            profilepic = {'files': ('profilepic.jpg', open(picturepath, 'rb'), 'image', {'uri': ''})}
            r = api.request_post_img("upload", profilepic)
        except Exception as e:
            print(e)
        print('Picture saved at: ' + str(picturepath))
        data = {
            'pk': user['pk'],
            'username': user['username'],
            'name': user['full_name'],
            'follower': user['follower_count'],
            'bio': user['biography']
        }
        print('Got userdata: ' + str(data))
        endpoint = 'Insta-users'
        datalist = [data]
        self.checkexisting(endpoint, 'pk', datalist)
        print("Inserted ownprofile with name: " + user['username'] + " in the database")
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

    def checkexisting(self, endpoint, prop, data):
        try:
            for key in data:
                print('looking for existing data!')
                result = self.db.request_get(endpoint + '?' + prop + '_eq=' + str(key['pk']))
                print('This is already there: ' + str(result))
                if result == []:
                    r = self.db.request_post(endpoint, json.dumps(key))
                    print('Response: ' + str(r))
                    print('dumped: ' + str(key))
                else:
                    r = self.db.request_put(endpoint, result['id'], json.dumps(key))
                    print('Response: ' + str(r))
        except Exception as e:
            print('Error while sending data to api! ' + str(e))
