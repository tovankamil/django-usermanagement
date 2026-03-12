from apps.users.interfaces.user_repository import UserRepository


class MockUserRepository(UserRepository):

    def __init__(self):
        self.users = {}

    def get_by_id(self, user_id):
        return self.users.get(user_id)

    def get_by_email(self, email):
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_by_username(self, username):
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def list(self):
        return list(self.users.values())

    def create(self, user):
        self.users[user.id] = user
        return user

    def update(self, user):
        self.users[user.id] = user
        return user

    def delete(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
