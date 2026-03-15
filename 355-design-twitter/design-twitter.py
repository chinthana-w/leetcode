from collections import deque

class Twitter:

    def __init__(self):
        self.users = {}
        self.tweets = {}
        self.global_id = 0

    def getOrCreateUser(self, userId):
        if userId not in self.users:
            user = User(userId)
            self.users[userId] = user
        else:
            user = self.users[userId]

        return user

    def postTweet(self, userId: int, tweetId: int) -> None:
        user = self.getOrCreateUser(userId)
        tweet = user.postTweet(tweetId)
        tweet.global_id = self.global_id
        self.global_id += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        user = self.getOrCreateUser(userId)
        userList = [user] + list(user.following.values())
        # print(f"user list: {userList}")
        tweets = []
        for u in userList:
            for t in u.tweets.values():
                tweets.append(t)

        # print(userList, tweets)

        tweets = sorted(tweets,key=lambda t: t.global_id)[::-1]
        return [t.id for t in tweets[:10]]

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId == followeeId:
            return
        follower = self.getOrCreateUser(followerId)
        followee = self.getOrCreateUser(followeeId)

        follower.follow(followee)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followerId == followeeId:
            return
        follower = self.getOrCreateUser(followerId)
        followee = self.getOrCreateUser(followeeId)

        follower.unfollow(followee)
        
class User:
    def __init__(self, idx):
        self.id = idx
        self.tweets = {}
        self.tweet_history = deque([])
        self.followers = {}
        self.following = {}

    def __repr__(self):
        return f"user #{self.id}"

    def postTweet(self, tweet_id):
        tweet = Tweet(tweet_id, self)
        self.tweets[tweet_id] = tweet
        self.tweet_history.append(tweet_id)

        return tweet

    def follow(self, user):
        # print(f"{self.id} following {user.id}")
        self.following[user.id] = user
        user.followers[self.id] = self
        # print("follow list", self.following.values())

    def unfollow(self, user):
        # print(f"{self.id} unfollowing {user.id}")
        if user.id in self.following:
            del self.following[user.id]
        if self.id in user.followers:
            del user.followers[self.id]
        # print("following, ", self.following.values())

class Tweet:
    def __init__(self, idx, user):
        self.id = idx
        self.user = user

    def __repr__(self):
        return f"Tweet #{self.id}"


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)