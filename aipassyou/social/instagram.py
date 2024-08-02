import os
import instaloader
from ..data import User, Profile, Post

class Instagram:

    def __init__(self, username):
        self.api = instaloader.Instaloader()
        self.username = username
        self.data = User(network = "Instagram")

    def extract(self, limit: int = 20):
        self.connect()
        self.userinfo()
        self.posts(limit)
        self.following(limit)
        return self.data
    
    def connect(self):
        username = os.getenv("INSTAGRAM_USERNAME")
        password = os.getenv("INSTAGRAM_PASSWORD")
        
        if username and password:
            self.api.login(username, password)

    def userinfo(self):
        self.profile = instaloader.Profile.from_username(self.api.context, self.username)
        self.data.profile = Profile(
            id = self.profile.userid,
            username = self.profile.username,
            full_name = self.profile.full_name,
            biography = self.profile.biography
        )
        if self.profile.biography_hashtags: 
            self.data.hashtags += self.profile.biography_hashtags
    
    def posts(self, limit: int = 20):
        posts = self.profile.get_posts()
        for post in posts:
            self.data.posts.append(Post(
                id = post.mediaid,
                #title = post.title,
                date = post.date,
                content = post.caption
            ))
            #if post.location: self.data.locations.append(post.location.name)
            if post.caption_hashtags: self.data.hashtags += post.caption_hashtags
            
            limit-=1
            if limit == 0: break

    def following(self, limit: int = 20):
        pass
        ''' login required
        following = self.profile.get_followees()
        for profile in following:
            self.data.following.append(User(
                id = profile.userid,
                username = profile.username,
                full_name = profile.full_name,
                biography = profile.biography
            ))

            limit-=1
            if limit == 0: break
        '''
            
