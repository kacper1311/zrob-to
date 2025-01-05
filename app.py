import tkinter as tk
from tkinter import ttk
import json
import os

class Task:
    def __init__(self, task, status="do zrobienia"):
        self.task = task
        self.status = status

class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            if os.path.exists("tasks.json"):
                with open("tasks.json", "r") as file:
                    return [Task(**task) for task in json.load(file)]
        except Exception as e:
            app.show_error_message(f"Błąd wczytywania zadań: {e}")
        return []

    def save_tasks(self):
        try:
            with open("tasks.json", "w") as file:
                json.dump([task.__dict__ for task in self.tasks], file)
        except Exception as e:
            app.show_error_message(f"Błąd zapisu zadań: {e}")

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, index, task, status):
        try:
            self.tasks[index].task = task
            self.tasks[index].status = status
            self.save_tasks()
        except IndexError:
            app.show_error_message("Nie można edytować: zadanie nie istnieje.")

    def delete_task(self, index):
        try:
            del self.tasks[index]
            self.save_tasks()
        except IndexError:
            app.show_error_message("Nie można usunąć: zadanie nie istnieje.")

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zrób to!")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b2b2b")
        self.manager = TaskManager()

        self.create_widgets()
        self.update_task_list()

    def create_widgets(self):
        # Frames
        self.frame_tasks = tk.Frame(self.root, bg="#3c3f41", pady=10)
        self.frame_tasks.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_controls = tk.Frame(self.root, bg="#2b2b2b")
        self.frame_controls.pack(fill="x", padx=10, pady=5)

        # Task list with scrollbar
        self.canvas = tk.Canvas(self.frame_tasks, bg="#3c3f41", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame_tasks, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#3c3f41")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add task section
        self.button_add_task = tk.Button(self.root, text="Dodaj nowe zadanie", font=("Segoe UI", 12), command=self.show_add_task, bg="#4CAF50", fg="white")
        self.button_add_task.pack(side="bottom", pady=10)

    def add_task(self, task_text, status):
        if task_text:
            self.manager.add_task(Task(task_text, status))
            self.update_task_list()
        else:
            self.show_error_message("Treść zadania nie może być pusta!")

    def update_task_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.manager.tasks):
            task_frame = tk.Frame(self.scrollable_frame, bg="#444444", pady=5, padx=5, relief="raised", bd=2)
            task_frame.pack(fill="x", pady=5)

            task_label = tk.Label(task_frame, text=task.task, font=("Segoe UI", 12), bg="#444444", fg="white", anchor="w")
            task_label.pack(side="left", fill="x", expand=True, padx=5)

            status_color = {"do zrobienia": "#ff4d4d", "w trakcie": "#ffa500", "zakończone": "#4CAF50"}
            status_label = tk.Label(task_frame, text=task.status, font=("Segoe UI", 12), bg=status_color.get(task.status, "#444444"), fg="white", width=12)
            status_label.pack(side="left", padx=5)

            button_edit = tk.Button(task_frame, text="Edytuj", font=("Segoe UI", 10), bg="#2196F3", fg="white", command=lambda idx=index: self.show_edit_task(idx))
            button_edit.pack(side="right", padx=5)

            button_delete = tk.Button(task_frame, text="Usuń", font=("Segoe UI", 10), bg="#f44336", fg="white", command=lambda idx=index: self.delete_task(idx))
            button_delete.pack(side="right", padx=5)

    def show_add_task(self):
        self.clear_task_controls()

        self.entry_new_task = tk.Entry(self.frame_controls, font=("Segoe UI", 12), bg="#1e1e1e", fg="white", insertbackground="white")
        self.entry_new_task.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.combo_status_add = ttk.Combobox(self.frame_controls, values=["do zrobienia", "w trakcie", "zakończone"], font=("Segoe UI", 12), state="readonly")
        self.combo_status_add.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.combo_status_add.set("do zrobienia")

        button_save = tk.Button(self.frame_controls, text="Dodaj", font=("Segoe UI", 12), bg="#4CAF50", fg="white", command=self.save_new_task)
        button_save.grid(row=0, column=2, padx=5, pady=5)

        button_cancel = tk.Button(self.frame_controls, text="Anuluj", font=("Segoe UI", 12), command=self.hide_task_controls)
        button_cancel.grid(row=0, column=3, padx=5, pady=5)

        self.frame_controls.columnconfigure(0, weight=1)

    def save_new_task(self):
        task_text = self.entry_new_task.get().strip()
        status = self.combo_status_add.get()
        self.add_task(task_text, status)
        self.hide_task_controls()

    def show_edit_task(self, index):
        self.clear_task_controls()

        task = self.manager.tasks[index]

        self.entry_edit_task = tk.Entry(self.frame_controls, font=("Segoe UI", 12), bg="#1e1e1e", fg="white", insertbackground="white")
        self.entry_edit_task.insert(0, task.task)
        self.entry_edit_task.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.combo_status_edit = ttk.Combobox(self.frame_controls, values=["do zrobienia", "w trakcie", "zakończone"], font=("Segoe UI", 12), state="readonly")
        self.combo_status_edit.set(task.status)
        self.combo_status_edit.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button_save = tk.Button(self.frame_controls, text="Zapisz", font=("Segoe UI", 12), bg="#4CAF50", fg="white", command=lambda: self.edit_task(index))
        button_save.grid(row=0, column=2, padx=5, pady=5)

        button_cancel = tk.Button(self.frame_controls, text="Anuluj", font=("Segoe UI", 12), command=self.hide_task_controls)
        button_cancel.grid(row=0, column=3, padx=5, pady=5)

        self.frame_controls.columnconfigure(0, weight=1)

    def edit_task(self, index):
        task_text = self.entry_edit_task.get().strip()
        status = self.combo_status_edit.get()
        if task_text:
            self.manager.edit_task(index, task_text, status)
            self.update_task_list()
            self.hide_task_controls()
        else:
            self.show_error_message("Treść zadania nie może być pusta!")

    def delete_task(self, index):
        self.manager.delete_task(index)
        self.update_task_list()

    def hide_task_controls(self):
        for widget in self.frame_controls.winfo_children():
            widget.destroy()

    def clear_task_controls(self):
        for widget in self.frame_controls.winfo_children():
            widget.destroy()

    def show_error_message(self, message):
        error_label = tk.Label(self.root, text=message, font=("Segoe UI", 10), bg="#2b2b2b", fg="red")
        error_label.pack(fill="x")
        self.root.after(3000, error_label.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
