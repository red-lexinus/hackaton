
class User:  # класс пользователь
    def __init__(self, location=dict()):
        self.location = location


users_list = dict()  # список всех пользователей

# ключ - id пользователя, значение - класс с информацией о пользователе
