class User:
    def __init__(self, username, password, id=None):
        self.id = id
        self.username = username
        self.password = password

    def __eq__(self, value):
        return self.__dict__ == value.__dict__

    def __repr__(self):
        return f"Book({self.id}, {self.username}, {self.password})"
    