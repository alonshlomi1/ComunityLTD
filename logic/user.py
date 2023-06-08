

class User:
    def __init__(self, email, password=None, salt=None):
        self.email = email
        if password:
            self.password = password
        else:
            # default
            self.password = "1234567890"
        self.salt = salt