from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class PostFactory:
    @staticmethod
    def create_post(post_type, user, *args):
        if post_type == "Text":
            return SocialNetwork.TextPost(args[0], user)
        elif post_type == "Image":
            return SocialNetwork.ImagePost(args[0], user)
        elif post_type == "Sale":
            return SocialNetwork.SalePost(args[0], args[1], args[2], user)
        else:
            return None


class Sender(ABC):
    def __init__(self):
        self.followers = []

    def notify(self, notification):
        for follower in self.followers:
            follower.update(notification)


class Member(ABC):
    @abstractmethod
    def update(self, notification):
        pass


class SocialNetwork:
    _instance = None

    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name):
        self.name = name
        self.users = []
        self.logged_in_users = []
        self.posts = []
        print(f"The social network {self.name} was created!")

    def sign_up(self, username, password):
        if username in [user.name for user in self.users]:
            return None
        elif not 8 > len(password) > 4:
            return None
        else:
            user = self.User(username, password)
            self.users.append(user)
            self.logged_in_users.append(user)
            user.logged_in = True
            return user

    def log_out(self, username):
        for user in self.logged_in_users:
            if user.name == username:
                self.logged_in_users.remove(user)
                user.logged_in = False
                print(f"{username} disconnected")

    def log_in(self, username, password):
        for user in self.users:
            if user.name == username and user.password == password:
                self.logged_in_users.append(user)
                user.logged_in = True
                print(f"{username} connected")

    def __str__(self):
        result = f"{self.name} social network:\n"
        for user in self.users:
            result += str(user) + "\n"
        return result

    class User(Sender, Member):
        def __init__(self, name, password):
            super().__init__()
            self.name = name
            self.password = password
            self.following = []
            self.notifications = []
            self.posts = []
            self.logged_in = False

        def follow(self, user):
            if not self.logged_in or user in self.following or user == self:
                return False
            self.following.append(user)
            user.followers.append(self)
            print(f"{self.name} started following {user.name}")

        def unfollow(self, user):
            if not self.logged_in or user not in self.following or user == self:
                return False
            self.following.remove(user)
            user.followers.remove(self)
            print(f"{self.name} unfollowed {user.name}")

        def publish_post(self, post_type, *args):
            if not self.logged_in:
                return None
            post = PostFactory().create_post(post_type, self, *args)
            self.posts.append(post)
            self.notify(f"{self.name} has a new post")
            print(post)
            return post

        def print_notifications(self):
            print(f"{self.name}'s notifications:")
            for notification in self.notifications:
                print(notification)

        def update(self, notification):
            self.notifications.append(notification)

        def __str__(self):
            return f"User name: {self.name}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers)}"

    class Post:
        def __init__(self, user):
            self.user = user
            self.likes = []
            self.comments = []

        def like(self, user):
            if user not in self.likes and user != self.user:
                self.likes.append(user)
                notification = f"{user.name} liked your post"
                self.user.update(notification)
                print(f"notification to {self.user.name}: {notification}")

        def comment(self, user, text):
            self.comments.append((user, text))
            notification = f"{user.name} commented on your post"
            self.user.update(notification)
            print(f"notification to {self.user.name}: {notification}: {text}")

    class TextPost(Post):
        def __init__(self, text, user):
            super().__init__(user)
            self.__text = text

        def __str__(self):
            return f"{self.user.name} published a post:\n\"{self.__text}\"\n"

    class ImagePost(Post):
        def __init__(self, image, user):
            super().__init__(user)
            self.__image = image

        def display(self):
            try:
                img = mpimg.imread(self.__image)
                plt.imshow(img)
                plt.show()
            except FileNotFoundError:
                pass
            print("Shows picture")

        def __str__(self):
            return f"{self.user.name} posted a picture\n"

    class SalePost(Post):
        def __init__(self, item, price, location, user):
            super().__init__(user)
            self.__item = item
            self.__price = price
            self.__location = location
            self.__isSold = False
            self.__discounted = False

        def discount(self, percent, password):
            if self.user.password == password:
                self.__discounted = True
                self.__price *= (1 - percent / 100)
                print(f"Discount on {self.user.name} product! the new price is: {self.__price}")

        def sold(self, password):
            if self.user.password == password and not self.__isSold:
                self.__isSold = True
                print(f"{self.user.name}'s product is sold")

        def __str__(self):
            return f"{self.user.name} posted a product for sale:\n{'Sold!' if self.__isSold else 'For sale!'} {self.__item}, price: {self.__price}, pickup from: {self.__location}\n"
