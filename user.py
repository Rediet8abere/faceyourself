class user(object):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def json(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email
            }
