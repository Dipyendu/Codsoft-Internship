import customtkinter as ctk
from tkinter import messagebox
import json
import os

# Set the appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# File to store tasks
TASKS_FILE = "tasks.json"

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern To-Do List")
        self.geometry("600x700")  # Initial window size
        self.resizable(True, True)  # Allow window resizing

        # Initialize tasks list
        self.tasks = []
        self.load_tasks()

        # Define larger fonts
        self.title_font = ctk.CTkFont(size=28, weight="bold")
        self.button_font = ctk.CTkFont(size=16)
        self.entry_font = ctk.CTkFont(size=16)
        self.checkbox_font = ctk.CTkFont(size=16)

        # Configure grid layout for responsiveness
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)  # Allow the task list to expand

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title = ctk.CTkLabel(self, text="To-Do List", font=self.title_font)
        title.pack(pady=20)

        # Frame for adding tasks
        add_frame = ctk.CTkFrame(self)
        add_frame.pack(pady=10, padx=20, fill="x")

        self.task_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter a new task", font=self.entry_font)
        self.task_entry.pack(side="left", expand=True, fill="x", padx=(10, 5), pady=10)

        add_button = ctk.CTkButton(add_frame, text="Add Task", font=self.button_font, command=self.add_task)
        add_button.pack(side="right", padx=(5, 10), pady=10)

        # Frame for task list with scrollbar
        list_frame = ctk.CTkScrollableFrame(self, width=560, height=500)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.list_frame = list_frame

        # Populate existing tasks
        self.display_tasks()

        # Save tasks on closing the app
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {"description": task_text, "completed": False}
            self.tasks.append(task)
            self.display_tasks()
            self.task_entry.delete(0, "end")
            self.save_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a task description.")

    def display_tasks(self):
        # Clear the current list
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for idx, task in enumerate(self.tasks, start=1):
            task_frame = ctk.CTkFrame(self.list_frame)
            task_frame.pack(pady=5, padx=10, fill="x")

            var = ctk.BooleanVar(value=task["completed"])
            checkbox = ctk.CTkCheckBox(
                task_frame,
                text=task["description"],
                variable=var,
                font=self.checkbox_font,
                command=lambda idx=idx-1, var=var: self.toggle_task(idx, var)
            )
            checkbox.pack(side="left", padx=10, pady=10, fill="x", expand=True)

            delete_button = ctk.CTkButton(
                task_frame,
                text="Delete",
                font=self.button_font,
                width=80,
                command=lambda idx=idx-1: self.delete_task(idx)
            )
            delete_button.pack(side="right", padx=10, pady=10)

    def toggle_task(self, index, var):
        self.tasks[index]["completed"] = var.get()
        self.save_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.display_tasks()
        self.save_tasks()

    def save_tasks(self):
        try:
            with open(TASKS_FILE, "w") as file:
                json.dump(self.tasks, file, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving tasks:\n{e}")

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, "r") as file:
                    self.tasks = json.load(file)
            except Exception as e:
                messagebox.showerror("Load Error", f"An error occurred while loading tasks:\n{e}")
                self.tasks = []

    def on_closing(self):
        self.save_tasks()
        self.destroy()

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
