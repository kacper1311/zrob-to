import unittest
from users import UserManager

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.manager = UserManager()

    def test_add_user(self):
        self.manager.add_user("Jan", "Kowalski")
        self.assertEqual(len(self.manager.users), 1)
        self.assertEqual(self.manager.users[0]["name"], "Jan")

if __name__ == "__main__":
    unittest.main()
