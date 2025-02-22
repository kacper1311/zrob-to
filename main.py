import tkinter as tk
from tkinter import ttk, messagebox
from tasks import TaskManager
from users import UserManager
from storage import save_data, load_data

# Konfiguracja stylów
BG_COLOR = "#2d3436"
ACCENT_COLOR = "#0984e3"
BTN_COLOR = "#74b9ff"
TEXT_COLOR = "#dfe6e9"
ENTRY_BG = "#636e72"
FONT = ("Segoe UI", 10)

class ModernTaskManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zrób to!")
        self.geometry("1200x800")
        self.configure(background=BG_COLOR)
        
        # Inicjalizacja menedżerów
        self.task_manager = TaskManager()
        self.user_manager = UserManager()
        self.load_initial_data()
        
        # Konfiguracja interfejsu
        self.style = ttk.Style()
        self._configure_styles()
        self._create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _configure_styles(self):
        self.style.theme_use("clam")
        
        # Globalne style
        self.style.configure(".", 
                           background=BG_COLOR,
                           foreground=TEXT_COLOR,
                           font=FONT)
        
        # Style zakładek
        self.style.configure("TNotebook", background=BG_COLOR)
        self.style.configure("TNotebook.Tab",
                           padding=[20, 5],
                           font=("Segoe UI", 11, "bold"),
                           background=BG_COLOR,
                           foreground=TEXT_COLOR)
        self.style.map("TNotebook.Tab",
                     background=[("selected", ACCENT_COLOR)],
                     foreground=[("selected", "white")])

        # Style przycisków
        self.style.configure("TButton",
                           background=BTN_COLOR,
                           borderwidth=0,
                           padding=10,
                           font=("Segoe UI", 10, "bold"))
        self.style.map("TButton",
                     background=[("active", ACCENT_COLOR)])

        # Style list
        self.style.configure("Treeview",
                           background=ENTRY_BG,
                           fieldbackground=ENTRY_BG,
                           foreground=TEXT_COLOR,
                           rowheight=35,
                           borderwidth=0)
        self.style.configure("Treeview.Heading",
                           background=ACCENT_COLOR,
                           foreground="white",
                           padding=10,
                           font=("Segoe UI", 11, "bold"))

        # Style pól wprowadzania
        self.style.configure("TEntry",
                           fieldbackground=ENTRY_BG,
                           insertcolor=TEXT_COLOR,
                           borderwidth=0,
                           padding=8)
        self.style.configure("TCombobox",
                           fieldbackground=ENTRY_BG)

    def _create_widgets(self):
        # Kontener główny
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Zakładki
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Zakładka zadań
        tasks_tab = self._create_tab_content("tasks")
        notebook.add(tasks_tab, text="📝 Zadania")

        # Zakładka użytkowników
        users_tab = self._create_tab_content("users")
        notebook.add(users_tab, text="👥 Użytkownicy")

    def _create_tab_content(self, tab_type):
        tab = ttk.Frame(self)
        
        # Kontener wewnętrzny
        container = ttk.Frame(tab)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        if tab_type == "tasks":
            # Nagłówek zadań
            header_frame = ttk.Frame(container)
            header_frame.pack(fill=tk.X, pady=(0, 15))
            
            ttk.Label(header_frame, 
                    text="Zarządzanie zadaniami", 
                    font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT)
            
            # Przyciski akcji
            btn_frame = ttk.Frame(header_frame)
            btn_frame.pack(side=tk.RIGHT)
            
            ttk.Button(btn_frame, 
                     text="➕ Nowe zadanie", 
                     command=self.open_add_task_dialog).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, 
                     text="✎ Edytuj", 
                     command=self.open_edit_task_dialog).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, 
                     text="🗑 Usuń", 
                     command=self.delete_task).pack(side=tk.LEFT, padx=5)

            # Lista zadań
            columns = ("ID", "Tytuł", "Opis", "Status", "Przypisany do")
            self.tasks_tree = self._create_tree(container, columns)
            self.refresh_tasks_list()

        elif tab_type == "users":
            # Nagłówek użytkowników
            header_frame = ttk.Frame(container)
            header_frame.pack(fill=tk.X, pady=(0, 15))
            
            ttk.Label(header_frame, 
                    text="Zarządzanie użytkownikami", 
                    font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT)
            
            # Przyciski akcji
            btn_frame = ttk.Frame(header_frame)
            btn_frame.pack(side=tk.RIGHT)
            
            ttk.Button(btn_frame, 
                     text="➕ Dodaj użytkownika", 
                     command=self.open_add_user_dialog).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, 
                     text="✎ Edytuj", 
                     command=self.open_edit_user_dialog).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, 
                     text="🗑 Usuń", 
                     command=self.delete_user).pack(side=tk.LEFT, padx=5)

            # Lista użytkowników
            columns = ("ID", "Imię", "Nazwisko")
            self.users_tree = self._create_tree(container, columns)
            self.refresh_users_list()

        return tab

    def _create_tree(self, parent, columns):
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col, anchor=tk.W)
            tree.column(col, width=150, anchor=tk.W, stretch=True)
            
        tree.pack(fill=tk.BOTH, expand=True)
        return tree

    def load_initial_data(self):
        data = load_data()
        self.task_manager.tasks = data.get("tasks", [])
        self.user_manager.users = data.get("users", [])

    def refresh_tasks_list(self):
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        for task in self.task_manager.tasks:
            self.tasks_tree.insert("", tk.END, values=(
                task["id"],
                task["title"],
                task["description"],
                task["status"],
                task["assigned_to"]
            ))

    def refresh_users_list(self):
        self.users_tree.delete(*self.users_tree.get_children())
        for user in self.user_manager.users:
            self.users_tree.insert("", tk.END, values=(
                user["id"],
                user["name"],
                user["surname"]
            ))

    def open_add_task_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Nowe zadanie")
        dialog.configure(background=BG_COLOR)
        
        # Pola formularza
        fields = [
            ("Tytuł:", ttk.Entry(dialog)),
            ("Opis:", ttk.Entry(dialog)),
            ("Status:", ttk.Combobox(dialog, values=["do zrobienia", "w trakcie", "zakończone"])),
            ("Przypisz do:", ttk.Combobox(dialog, values=[
                f"{user['name']} {user['surname']}" for user in self.user_manager.users
            ]))
        ]
        
        # Automatyczne ustawienie statusu
        fields[2][1].current(0)
        
        for i, (label, widget) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            widget.grid(row=i, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Button(dialog, 
                 text="Zapisz", 
                 command=lambda: self._save_new_task(
                     [widget.get() for _, widget in fields],
                     dialog
                 )).grid(row=4, columnspan=2, pady=10)

    def _save_new_task(self, data, dialog):
        title, desc, status, assigned = data
        if not title:
            messagebox.showwarning("Błąd", "Wprowadź tytuł zadania!")
            return
            
        self.task_manager.add_task(title, desc, status, assigned)
        self.refresh_tasks_list()
        dialog.destroy()

    def delete_task(self):
        selected = self.tasks_tree.focus()
        if not selected:
            messagebox.showwarning("Błąd", "Wybierz zadanie do usunięcia!")
            return
            
        task_id = int(self.tasks_tree.item(selected)["values"][0])
        self.task_manager.tasks = [t for t in self.task_manager.tasks if t["id"] != task_id]
        self.refresh_tasks_list()
        messagebox.showinfo("Sukces", "Zadanie usunięte!")

    def open_edit_task_dialog(self):
        selected = self.tasks_tree.focus()
        if not selected:
            messagebox.showwarning("Błąd", "Wybierz zadanie do edycji!")
            return
            
        task_id = int(self.tasks_tree.item(selected)["values"][0])
        task = next(t for t in self.task_manager.tasks if t["id"] == task_id)

        dialog = tk.Toplevel(self)
        dialog.title("Edytuj zadanie")
        dialog.configure(background=BG_COLOR)
        
        fields = [
            ("Tytuł:", ttk.Entry(dialog), task["title"]),
            ("Opis:", ttk.Entry(dialog), task["description"]),
            ("Status:", ttk.Combobox(dialog, values=["do zrobienia", "w trakcie", "zakończone"]), task["status"]),
            ("Przypisz do:", ttk.Combobox(dialog, values=[
                f"{u['name']} {u['surname']}" for u in self.user_manager.users
            ]), task["assigned_to"])
        ]
        
        for i, (label, widget, value) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            widget.insert(0, value) if isinstance(widget, ttk.Entry) else widget.set(value)
            widget.grid(row=i, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Button(dialog, 
                 text="Zapisz zmiany", 
                 command=lambda: self._save_edited_task(
                     task,
                     [widget.get() if isinstance(widget, ttk.Entry) else widget.get() for _, widget, _ in fields],
                     dialog
                 )).grid(row=4, columnspan=2, pady=10)

    def _save_edited_task(self, task, data, dialog):
        task["title"] = data[0]
        task["description"] = data[1]
        task["status"] = data[2]
        task["assigned_to"] = data[3]
        self.refresh_tasks_list()
        dialog.destroy()
        messagebox.showinfo("Sukces", "Zmiany zapisane!")

    def open_add_user_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Dodaj użytkownika")
        dialog.configure(background=BG_COLOR)
        
        # Pola formularza
        fields = [
            ("Imię:", ttk.Entry(dialog)),
            ("Nazwisko:", ttk.Entry(dialog))
        ]
        
        for i, (label, widget) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            widget.grid(row=i, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Button(dialog, 
                 text="Zapisz", 
                 command=lambda: self._save_new_user(
                     [widget.get() for _, widget in fields],
                     dialog
                 )).grid(row=2, columnspan=2, pady=10)

    def _save_new_user(self, data, dialog):
        name, surname = data
        if not name or not surname:
            messagebox.showwarning("Błąd", "Wprowadź imię i nazwisko!")
            return
            
        self.user_manager.add_user(name, surname)
        self.refresh_users_list()
        dialog.destroy()

    def delete_user(self):
        selected = self.users_tree.focus()
        if not selected:
            messagebox.showwarning("Błąd", "Wybierz użytkownika do usunięcia!")
            return
            
        user_id = int(self.users_tree.item(selected)["values"][0])
        self.user_manager.users = [u for u in self.user_manager.users if u["id"] != user_id]
        self.refresh_users_list()
        messagebox.showinfo("Sukces", "Użytkownik usunięty!")

    def open_edit_user_dialog(self):
        selected = self.users_tree.focus()
        if not selected:
            messagebox.showwarning("Błąd", "Wybierz użytkownika do edycji!")
            return
            
        user_id = int(self.users_tree.item(selected)["values"][0])
        user = next(u for u in self.user_manager.users if u["id"] == user_id)

        dialog = tk.Toplevel(self)
        dialog.title("Edytuj użytkownika")
        dialog.configure(background=BG_COLOR)
        
        fields = [
            ("Imię:", ttk.Entry(dialog), user["name"]),
            ("Nazwisko:", ttk.Entry(dialog), user["surname"])
        ]
        
        for i, (label, widget, value) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            widget.insert(0, value)
            widget.grid(row=i, column=1, padx=10, pady=5, sticky=tk.EW)
        
        ttk.Button(dialog, 
                 text="Zapisz zmiany", 
                 command=lambda: self._save_edited_user(
                     user,
                     [widget.get() for _, widget, _ in fields],
                     dialog
                 )).grid(row=2, columnspan=2, pady=10)

    def _save_edited_user(self, user, data, dialog):
        user["name"] = data[0]
        user["surname"] = data[1]
        self.refresh_users_list()
        dialog.destroy()
        messagebox.showinfo("Sukces", "Zmiany zapisane!")

    def on_close(self):
        save_data(self.task_manager.tasks, self.user_manager.users)
        self.destroy()

if __name__ == "__main__":
    app = ModernTaskManager()
    app.mainloop()