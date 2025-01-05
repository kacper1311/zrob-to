import tkinter as tk
from tkinter import ttk, messagebox
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
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                return [Task(**task) for task in json.load(file)]
        return []

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump([task.__dict__ for task in self.tasks], file)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, index, task, status):
        self.tasks[index].task = task
        self.tasks[index].status = status
        self.save_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zrób to!")
        self.root.geometry("800x600")
        self.manager = TaskManager()

        self.create_widgets()
        self.update_task_list()

    def create_widgets(self):
        # Frame for the task details
        self.frame_details = ttk.Frame(self.root, padding="10")
        self.frame_details.grid(row=0, column=0, sticky="nsew")

        # Frame for the task list
        self.frame_tasks = ttk.Frame(self.root, padding="10")
        self.frame_tasks.grid(row=1, column=0, sticky="nsew")

        # Configure grid weights for responsiveness
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=1)

        # Buttons
        self.frame_buttons = ttk.Frame(self.frame_details)
        self.frame_buttons.pack(fill="x", pady=10)

        self.button_add = tk.Button(self.frame_buttons, text="Dodaj zadanie", font=("Arial", 12), command=self.show_add_task_form)
        self.button_add.pack(side="left", padx=5, expand=True)

        # Edit and delete frame
        self.edit_delete_frame = ttk.Frame(self.root, padding="10", relief="raised")
        self.edit_delete_frame.place_forget()

        self.label_edit_task = ttk.Label(self.edit_delete_frame, text="Edytuj zadanie", font=("Arial", 14))
        self.label_edit_task.pack(anchor="center")

        self.text_task_edit = tk.Text(self.edit_delete_frame, wrap="word", height=4, font=("Arial", 12))
        self.text_task_edit.pack(fill="x", pady=5)

        self.label_status_edit = ttk.Label(self.edit_delete_frame, text="Status", font=("Arial", 14))
        self.label_status_edit.pack(anchor="center")

        self.combo_status_edit = ttk.Combobox(self.edit_delete_frame, values=["do zrobienia", "w trakcie", "zakończone"], font=("Arial", 12), state="readonly")
        self.combo_status_edit.pack(fill="x", pady=5)
        self.combo_status_edit.bind("<Button-1>", lambda event: self.combo_status_edit.event_generate('<Down>'))

        self.button_edit = tk.Button(self.edit_delete_frame, text="Edytuj", font=("Arial", 12), command=self.edit_task)
        self.button_edit.pack(side="left", padx=5, expand=True)

        self.button_delete = tk.Button(self.edit_delete_frame, text="Usuń", font=("Arial", 12), command=self.delete_task)
        self.button_delete.pack(side="left", padx=5, expand=True)

        self.button_cancel = tk.Button(self.edit_delete_frame, text="Anuluj", font=("Arial", 12), command=self.hide_edit_delete_buttons)
        self.button_cancel.pack(side="left", padx=5, expand=True)

        # Task list
        self.label_tasks = ttk.Label(self.frame_tasks, text="Lista zadań", font=("Arial", 14))
        self.label_tasks.pack(anchor="center")

        self.text_tasks = tk.Text(self.frame_tasks, wrap="word", font=("Arial", 12))
        self.text_tasks.pack(fill="both", expand=True)
        self.text_tasks.bind("<Button-1>", self.show_edit_delete_buttons)

    def show_add_task_form(self):
        self.edit_delete_frame.place_forget()
        self.add_task_frame = ttk.Frame(self.root, padding="10", relief="raised")
        self.add_task_frame.place(relx=0.5, rely=0.3, anchor="center")

        self.label_add_task = ttk.Label(self.add_task_frame, text="Dodaj nowe zadanie", font=("Arial", 14))
        self.label_add_task.pack(anchor="center")

        self.text_task_add = tk.Text(self.add_task_frame, wrap="word", height=4, font=("Arial", 12))
        self.text_task_add.pack(fill="x", pady=5)

        self.label_status_add = ttk.Label(self.add_task_frame, text="Status", font=("Arial", 14))
        self.label_status_add.pack(anchor="center")

        self.combo_status_add = ttk.Combobox(self.add_task_frame, values=["do zrobienia", "w trakcie", "zakończone"], font=("Arial", 12), state="readonly")
        self.combo_status_add.pack(fill="x", pady=5)
        self.combo_status_add.set("do zrobienia")
        self.combo_status_add.bind("<Button-1>", lambda event: self.combo_status_add.event_generate('<Down>'))

        self.button_confirm_add = tk.Button(self.add_task_frame, text="Dodaj", font=("Arial", 12), command=self.add_task)
        self.button_confirm_add.pack(side="left", padx=5, expand=True)

        self.button_cancel_add = tk.Button(self.add_task_frame, text="Anuluj", font=("Arial", 12), command=self.hide_add_task_form)
        self.button_cancel_add.pack(side="left", padx=5, expand=True)

    def hide_add_task_form(self):
        self.add_task_frame.place_forget()

    def add_task(self):
        task = self.text_task_add.get("1.0", tk.END).strip()
        status = self.combo_status_add.get()
        if task and status:
            new_task = Task(task, status)
            self.manager.add_task(new_task)
            self.update_task_list()
            self.hide_add_task_form()

    def edit_task(self):
        selected_task_index = self.get_selected_task_index()
        if selected_task_index is not None:
            task = self.text_task_edit.get("1.0", tk.END).strip()
            status = self.combo_status_edit.get()
            if task and status:
                self.manager.edit_task(selected_task_index, task, status)
                self.update_task_list()
                self.hide_edit_delete_buttons()

    def delete_task(self):
        selected_task_index = self.get_selected_task_index()
        if selected_task_index is not None:
            self.manager.delete_task(selected_task_index)
            self.update_task_list()
            self.hide_edit_delete_buttons()

    def show_edit_delete_buttons(self, event):
        selected_task_index = self.get_selected_task_index()
        if selected_task_index is not None:
            selected_task = self.manager.tasks[selected_task_index]
            self.text_task_edit.delete("1.0", tk.END)
            self.text_task_edit.insert(tk.END, selected_task.task)
            self.combo_status_edit.set(selected_task.status)
            self.edit_delete_frame.place(relx=0.5, rely=0.3, anchor="center")

    def hide_edit_delete_buttons(self):
        self.edit_delete_frame.place_forget()

    def update_task_list(self):
        self.text_tasks.config(state=tk.NORMAL)
        self.text_tasks.delete("1.0", tk.END)
        for task in self.manager.tasks:
            self.text_tasks.insert(tk.END, f"{task.task} - {task.status}\n")
        self.text_tasks.config(state=tk.DISABLED)

    def get_selected_task_index(self):
        try:
            index = self.text_tasks.index(tk.CURRENT).split('.')[0]
            return int(index) - 1
        except:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()