import os
from twscrape import API, gather
from ..data import User, Profile, Post

class Twitter:

    def __init__(self, username: str):
        self.api = None
        self.username = username
        self.data = User(network = "Twitter")

    async def extract(self, limit: int = 20):
        await self.connect()
        await self.userinfo()
        await self.posts(limit)
        await self.following(limit)
        return self.data

    async def connect(self):
        username = os.getenv("TWITTER_USERNAME")
        passwd = os.getenv("TWITTER_PASSWORD")
        email = os.getenv("TWITTER_EMAIL")
        email_pwd = os.getenv("TWITTER_EMAIL_PWD")

        if not username or not passwd or not email or not email_pwd:
            print("[!] No twitter credential provided")
            raise

        self.api = API("accounts.db")
        await self.api.pool.add_account(username, passwd, email, email_pwd)
        await self.api.pool.login_all()

    async def userinfo(self):
        self.profile = await self.api.user_by_login(self.username)
        self.data.profile = Profile(
            id = self.profile.id,
            username = self.profile.username,
            full_name = self.profile.displayname,
            biography = self.profile.rawDescription,
            location = self.profile.location
        )
        self.data.locations.append(self.profile.location)
    
    async def posts(self, limit=20):
        posts = await gather(self.api.user_tweets_and_replies(self.profile.id, limit))
        for msg in posts:
            self.data.posts.append(Post(
                id = msg.id,
                date = msg.date,
                content = msg.rawContent
            ))
            self.data.hashtags += msg.hashtags

    async def following(self, limit=20):
        following = await gather(self.api.following(self.profile.id, limit))
        for user in following:
            self.data.following.append(Profile(
                id = user.id,
                username = user.username,
                full_name = user.displayname,
                biography = user.rawDescription,
                location = user.location
            ))
            