from tkinter import *
from tkinter import ttk

def add_task():
    task = task_entry.get()
    if task:
        tasks_listbox.insert(END, task)
        task_entry.delete(0, END)

def remove_task():
    selected_task_index = tasks_listbox.curselection()
    if selected_task_index:
        tasks_listbox.delete(selected_task_index)



root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Simple To-Do List").grid(column=0, row=0, columnspan=2)
ttk.Label(frm, text="Task:").grid(column=0, row=1)
tasks_listbox = Listbox(height=10, width=50)
tasks_listbox.grid(column=0, row=4, columnspan=2)
task_entry = ttk.Entry(frm, width=30)
task_entry.grid(column=1, row=1)
ttk.Button(frm, text="Add Task", command=add_task).grid(column=0, row=2, columnspan=2)
ttk.Button(frm, text="Remove Task", command=remove_task).grid(column=0, row=3, columnspan=2)
ttk.Button(frm, text="Exit", command=root.destroy).grid(column=0, row=4, columnspan=2)
root.mainloop()
