class TitleValidator:
    def __get__(self, instance, owner):
        return instance._title

    def __set__(self, instance, value):
        if not value or not isinstance(value, str):
            raise ValueError("Tytuł zadania nie może być pusty i musi być tekstem!")
        instance._title = value

class Task:
    title = TitleValidator()

    def __init__(self, title, description, status, assigned_to):
        self.title = title  # Deskryptor sprawdzi poprawność
        self.description = description
        self.status = status
        self.assigned_to = assigned_to

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, status, assigned_to):
        new_task = Task(title, description, status, assigned_to)
        self.tasks.append(new_task)
