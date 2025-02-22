class UserMeta(type):
    def __new__(cls, name, bases, class_dict):
        if "add_user" not in class_dict:
            raise TypeError("Klasa musi mieć metodę add_user!")
        return super().__new__(cls, name, bases, class_dict)

class UserManager(metaclass=UserMeta):
    def __init__(self):
        self.users = []

    def add_user(self, name, surname):
        new_user = {
            "id": len(self.users) + 1,
            "name": name,
            "surname": surname
        }
        self.users.append(new_user)
