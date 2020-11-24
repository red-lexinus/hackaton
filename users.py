
class User:  # класс пользователь
    def __init__(self):
        self.location = dict()
        self.is_have_location = False
        self.places_starts_at = 0


users_list = dict()  # список всех пользователей

# ключ - id пользователя, значение - класс с информацией о пользователе
