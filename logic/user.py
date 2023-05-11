

class User:
    def __init__(self, email, password=None, salt=None):
        self.email = email
        if password:
            self.password = password
        else:
            # TODO: gen new passwod
            self.password = "try"
        self.salt = salt