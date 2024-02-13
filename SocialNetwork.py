from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class SocialNetwork:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name):
        self.name = name
        self.users = []
        self.logged_in_users = []
        self.posts = []
        print(f"The social network {name} was created!")

    class Observer:
        def notify(self, notification):
            pass

    class User(Observer):
        def __init__(self, name, password):
            self.name = name
            self.password = password
            self.following = []
            self.followers = []
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
            if post_type == "Text":
                content = args[0]
            elif post_type == "Image":
                content = args[0]
            elif post_type == "Sale":
                item, price, location = args
                content = {"item": item, "price": price,
                           "location": location}  # f"{item}, price: {price}, pickup from: {location}"
            else:
                return None  # Invalid post type

            post = SocialNetwork.Post(post_type, content, self)
            self.posts.append(post)
            print(post)
            return post

        def like(self, post):
            pass

        def comment(self, post, text):
            pass

        def print_notifications(self):
            print(f"{self.name}'s notifications:\n")
            for notification in self.notifications:
                print(notification)

        def notify(self, notification):
            self.notifications.append(notification)
            print(f"notification to {self.name}: {notification}")

        def __str__(self):
            return f"User name: {self.name}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers)}"

    class Post:
        def __init__(self, post_type, content, user):
            self.post_type = post_type
            self.content = content
            self.user = user
            self.likes = []
            self.comments = []
            self.isSold = False
            self.discounted = False
            self.item = None
            self.price = None
            self.location = None

        def like(self, user):
            if user not in self.likes and user != self.user:
                self.likes.append(user)
                notification = f"{user.name} liked your post"
                self.user.notify(notification)

        def comment(self, user, text):
            self.comments.append((user, text))
            notification = f"{user.name} commented on your post: {text}"
            self.user.notify(notification)

        def discount(self, percent, password):
            if self.user.password == password and self.post_type == "Sale":
                self.discounted = True
                self.content["price"] *= (1 - percent / 100)
                print(f"Discount on {self.user.name}'s product! the new price is: {self.content['price']}")

        def sold(self, password):
            if self.user.password == password and self.post_type == "Sale":
                self.isSold = True
                print(f"{self.user.name}'s product is sold")

        def display(self):
            if self.post_type == "Image":
                img = mpimg.imread(self.content)
                plt.imshow(img)
                plt.show()
                print("Shows picture")

        def __str__(self):
            if self.post_type == "Text":
                return f"{self.user.name} published a post:\n\"{self.content}\"\n"
            elif self.post_type == "Image":
                return f"{self.user.name} posted a picture\n"
            else:
                content = f"{self.content['item']}, price: {self.content['price']}, pickup from: {self.content['location']}"
                return f"{self.user.name} posted a product for sale:\n{'Sold!' if self.isSold else 'For sale!'} {content}\n"

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
