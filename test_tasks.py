import unittest
from tasks import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        self.manager.add_task("Test", "Opis", "do zrobienia", "User")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0]["title"], "Test")

    def test_task_status(self):
        self.manager.add_task("Test", "Opis", "zakończone", "User")
        self.assertEqual(self.manager.tasks[0]["status"], "zakończone")

if __name__ == "__main__":
    unittest.main()
