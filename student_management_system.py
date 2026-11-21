import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Database
conn = sqlite3.connect("students.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS students (
                roll TEXT PRIMARY KEY, name TEXT, course TEXT, phone TEXT)""")
conn.commit()

# Function
def refresh_table(query="SELECT * FROM students", params=()):
  for row in tree.get_children():
    tree.delete(row)
  for row in cur.execute(query, params):
    tree.insert("", tk.END, values=row)

def clear_fields():
  for var in (roll_var, name_var, course_var, phone_var):
    var.set("")

def add_student():
  if not roll_var.get() or not name_var.get():
    return messagebox.showwarning("Input Error", "Roll No and Name are required.")
  try:
    cur.execute(
        "INSERT INTO students VALUES (?, ?, ?, ?)",
        (roll_var.get(), name_var.get(), course_var.get(), phone_var.get()),
    )
    conn.commit()
    refresh_table()
    clear_fields()
  except sqlite3.IntegrityError:
    messagebox.showerror("Error", "Roll No already exists.")

def update_student():
  cur.execute(
      "UPDATE students SET name=?, course=?, phone=? WHERE roll=?",
      (name_var.get(), course_var.get(), phone_var.get(), roll_var.get()),
  )
  conn.commit()
  refresh_table()
  clear_fields()

def delete_student():
  selected = tree.focus()
  if not selected:
    return messagebox.showwarning("Select Record", "Click a row to delete.")
  roll = tree.item(selected)["values"][0]
  cur.execute("DELETE FROM students WHERE roll=?", (str(roll),))
  conn.commit()
  refresh_table()
  clear_fields()

def select_row(event):
  selected = tree.focus()
  if selected:
    vals = tree.item(selected)["values"]
    roll_var.set(vals[0])
    name_var.set(vals[1])
    course_var.set(vals[2])
    phone_var.set(vals[3])

def search_student(*args):
  term = f"%{search_var.get()}%"
  refresh_table(
      "SELECT * FROM students WHERE roll LIKE ? OR name LIKE ?", (term, term)
  )

# Tkinter
window = tk.Tk()
window.title("Student Management System")
window.geometry("680x420")

roll_var, name_var, course_var, phone_var, search_var = [
    tk.StringVar() for _ in range(5)
]
search_var.trace_add("write", search_student)

form = tk.Frame(window, padx=15, pady=15)
form.pack(side=tk.LEFT, fill=tk.Y)

fields = [
    ("Roll No:", roll_var),
    ("Full Name:", name_var),
    ("Course:", course_var),
    ("Phone:", phone_var),
]
for idx, (label, var) in enumerate(fields):
  tk.Label(form, text=label).grid(row=idx, column=0, sticky="w", pady=5)
  tk.Entry(form, textvariable=var, width=22).grid(row=idx, column=1, pady=5)

tk.Button(form, text="Add", width=10, bg="#4CAF50", fg="white", command=add_student).grid(row=4, column=0, pady=10)
tk.Button(form, text="Update", width=10, bg="#2196F3", fg="white", command=update_student).grid(row=4, column=1, pady=10)
tk.Button(form, text="Delete", width=10, bg="#f44336", fg="white", command=delete_student).grid(row=5, column=0, pady=5)
tk.Button(form, text="Clear", width=10, command=clear_fields).grid(row=5, column=1, pady=5)

right = tk.Frame(window, padx=10, pady=15)
right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(right, text="Search (Roll or Name):").pack(anchor="w")
tk.Entry(right, textvariable=search_var).pack(fill=tk.X, pady=(0, 10))

cols = ("Roll", "Name", "Course", "Phone")
tree = ttk.Treeview(right, columns=cols, show="headings")
for col in cols:
  tree.heading(col, text=col)
  tree.column(col, width=100)
tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<ButtonRelease-1>", select_row)

refresh_table()
window.mainloop()
