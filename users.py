# users.py
class UserManager:
    def __init__(self):
        self.users = []
        
    def add_user(self, name, surname):
        new_user = {
            "id": len(self.users) + 1,
            "name": name,
            "surname": surname
        }
        self.users.append(new_user)