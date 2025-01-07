import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from tkcalendar import Calendar  # You'll need to install this: pip install tkcalendar


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Load tasks
        self.tasks = self.load_tasks()

        # Create main containers
        self.create_header()
        self.create_task_input()
        self.create_task_list()

        # Style configuration
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        style.configure("TaskFrame.TFrame", background="white", relief="raised")

    def create_header(self):
        """Create the header section with title"""
        header_frame = ttk.Frame(self.root, style="Custom.TFrame", padding="20")
        header_frame.pack(fill="x")

        title = ttk.Label(
            header_frame,
            text="My To-Do List",
            font=("Helvetica", 24, "bold"),
            background="#f0f0f0"
        )
        title.pack()

    def create_task_input(self):
        """Create the input section for new tasks"""
        input_frame = ttk.Frame(self.root, style="Custom.TFrame", padding="20")
        input_frame.pack(fill="x", padx=20)

        # Task description input
        self.task_var = tk.StringVar()
        task_entry = ttk.Entry(
            input_frame,
            textvariable=self.task_var,
            font=("Helvetica", 12),
            width=40
        )
        task_entry.pack(side="left", padx=5)

        # Due date picker
        self.due_date_var = tk.StringVar()
        self.due_date_button = ttk.Button(
            input_frame,
            text="Set Due Date",
            command=self.show_calendar
        )
        self.due_date_button.pack(side="left", padx=5)

        # Add task button
        add_button = ttk.Button(
            input_frame,
            text="Add Task",
            command=self.add_task,
            style="Accent.TButton"
        )
        add_button.pack(side="left", padx=5)

    def create_task_list(self):
        """Create the scrollable task list"""
        # Create container for task list
        self.task_container = ttk.Frame(self.root, style="Custom.TFrame")
        self.task_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.task_container, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(self.task_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Custom.TFrame")

        # Configure canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack everything
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Load existing tasks
        self.refresh_task_list()

    def add_task(self):
        """Add a new task to the list"""
        description = self.task_var.get().strip()
        if not description:
            messagebox.showwarning("Warning", "Please enter a task description!")
            return

        task = {
            'description': description,
            'completed': False,
            'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'due_date': self.due_date_var.get() if self.due_date_var.get() else None
        }

        self.tasks.append(task)
        self.save_tasks()
        self.task_var.set("")  # Clear input
        self.due_date_var.set("")  # Clear due date
        self.refresh_task_list()

    def show_calendar(self):
        """Show calendar popup for date selection"""
        top = tk.Toplevel(self.root)
        top.title("Select Due Date")

        cal = Calendar(top, selectmode='day')
        cal.pack(padx=20, pady=20)

        def set_date():
            self.due_date_var.set(cal.get_date())
            top.destroy()

        ttk.Button(top, text="Set Date", command=set_date).pack(pady=10)

    def toggle_task(self, task_index):
        """Toggle task completion status"""
        self.tasks[task_index]['completed'] = not self.tasks[task_index]['completed']
        self.save_tasks()
        self.refresh_task_list()

    def delete_task(self, task_index):
        """Delete a task"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            del self.tasks[task_index]
            self.save_tasks()
            self.refresh_task_list()

    def refresh_task_list(self):
        """Refresh the displayed task list"""
        # Clear existing tasks
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Add each task to the list
        for i, task in enumerate(self.tasks):
            task_frame = ttk.Frame(self.scrollable_frame, style="TaskFrame.TFrame")
            task_frame.pack(fill="x", padx=5, pady=2)

            # Checkbox for completion status
            completed_var = tk.BooleanVar(value=task['completed'])
            checkbox = ttk.Checkbutton(
                task_frame,
                variable=completed_var,
                command=lambda x=i: self.toggle_task(x)
            )
            checkbox.pack(side="left", padx=5)

            # Task description
            description_label = ttk.Label(
                task_frame,
                text=task['description'],
                font=("Helvetica", 11),
                wraplength=500
            )
            description_label.pack(side="left", padx=5)

            # Due date if exists
            if task['due_date']:
                date_label = ttk.Label(
                    task_frame,
                    text=f"Due: {task['due_date']}",
                    font=("Helvetica", 10, "italic")
                )
                date_label.pack(side="left", padx=5)

            # Delete button
            delete_button = ttk.Button(
                task_frame,
                text="×",
                width=3,
                command=lambda x=i: self.delete_task(x)
            )
            delete_button.pack(side="right", padx=5)

    def save_tasks(self):
        """Save tasks to file"""
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        """Load tasks from file"""
        try:
            with open('tasks.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()