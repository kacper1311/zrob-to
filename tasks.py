# tasks.py
class TaskManager:
    def __init__(self):
        self.tasks = []
        
    def add_task(self, title, description, status, assigned_to):
        new_task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "status": status,
            "assigned_to": assigned_to
        }
        self.tasks.append(new_task)