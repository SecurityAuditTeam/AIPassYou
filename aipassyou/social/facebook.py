import facebook_scraper
from ..data import User, Profile, Post

class Facebook:

    def __init__(self, username):
        self.username = username
        self.data = User(network = "Facebook")

    def extract(self):
        print("[!] Not Working")
        return self.data
        self.userinfo()
        self.posts()
        self.following()

    def userinfo(self):
        profile = facebook_scraper.get_profile(self.username)
        print(profile)

        self.data.profile = Profile(
            id = profile['id'],
            username = self.username,
            full_name = profile['Name'] if 'Name' in profile else None,
            biography = profile['About'] if 'About' in profile else None,
            education = profile['Education'] if 'Education' in profile else None,
            work = profile['Work'] if 'Work' in profile else None
        )
        if 'Places lived' in profile:
            for place in profile['Places lived']:
                self.data.locations.append(place['text'])


    def posts(self, limit: int = 20):
        posts = facebook_scraper.get_posts(self.username)
        for post in posts:
            self.data.posts.append(Post(
                id = post.post_id,
                date = post.time,
                content = post.text
            ))

    def following(self, limit: int = 20):
        pass
        
            
