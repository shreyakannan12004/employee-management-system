import sqlite3


def connect_db():
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

connect_db()
from tkinter import *
from tkinter import ttk, messagebox

root = Tk()
root.title("Employee Management System")
root.geometry("700x500")
root.configure(bg="lightblue")
name_var = StringVar()
dept_var = StringVar()
salary_var = StringVar()
id_var = StringVar()
search_var = StringVar()


def add_employee():
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO employee (name, department, salary) VALUES (?, ?, ?)",
                (name_var.get(), dept_var.get(), salary_var.get()))
    conn.commit()
    conn.close()
    fetch_data()
    clear_fields()
    messagebox.showinfo("Success", "Employee added successfully!")

def fetch_data():
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee")
    rows = cur.fetchall()
    conn.close()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)

def clear_fields():
    name_var.set("")
    dept_var.set("")
    salary_var.set("")
    id_var.set("")

def get_data(event):
    selected = tree.focus()
    values = tree.item(selected, 'values')
    if values:
        id_var.set(values[0])
        name_var.set(values[1])
        dept_var.set(values[2])
        salary_var.set(values[3])

def update_employee():
    if id_var.get() == "":
        messagebox.showerror("Error", "Select a record first.")
        return
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("UPDATE employee SET name=?, department=?, salary=? WHERE id=?",
                (name_var.get(), dept_var.get(), salary_var.get(), id_var.get()))
    conn.commit()
    conn.close()
    fetch_data()
    clear_fields()
    messagebox.showinfo("Updated", "Employee updated successfully!")

def delete_employee():
    if id_var.get() == "":
        messagebox.showerror("Error", "Select a record first.")
        return
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM employee WHERE id=?", (id_var.get(),))
    conn.commit()
    conn.close()
    fetch_data()
    clear_fields()
    messagebox.showinfo("Deleted", "Employee deleted successfully!")

def search_employee():
    query = search_var.get()
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee WHERE name LIKE ? OR department LIKE ?", 
                ('%' + query + '%', '%' + query + '%'))
    rows = cur.fetchall()
    conn.close()
    
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)

frame1 = Frame(root, bg="#3a8c99")
frame1.pack(pady=40)

Label(frame1, text="Name", bg="#c6dff5", fg="blue").grid(row=0, column=0, padx=10, pady=5)
Entry(frame1, textvariable=name_var).grid(row=0, column=1,pady=5)

Label(frame1, text="Department", bg="#c6dff5",fg = "blue").grid(row=1, column=0, padx=10,pady=5)
Entry(frame1, textvariable=dept_var).grid(row=1, column=1,pady=5)

Label(frame1, text="Salary", bg="#c6dff5",fg = "blue").grid(row=2, column=0, padx=10,pady=5)
Entry(frame1, textvariable=salary_var).grid(row=2, column=1,pady=5)
frame2 = Frame(root, bg="#c6dff5")
frame2.pack()

Button(frame2, text="Add", width=25, command=lambda: add_employee()).grid(row=0, column=0, padx=10, pady=10)
Button(frame2, text="Update", width=25, command=lambda: update_employee()).grid(row=0, column=1, padx=10)
Button(frame2, text="Delete", width=25, command=lambda: delete_employee()).grid(row=0, column=2, padx=10)
Button(frame2, text="Clear", width=25, command=lambda: clear_fields()).grid(row=0, column=3, padx=10)

search_frame = Frame(root, bg="#f0f0f0")
search_frame.pack(pady=10)
Label(search_frame, text="Search:", bg="#f0f0f0").pack(side=LEFT)
Entry(search_frame, textvariable=search_var).pack(side=LEFT, padx=5)
Button(search_frame, text="Search", command=search_employee).pack(side=LEFT)

columns = ("ID", "Name", "Department", "Salary")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill=BOTH, expand=True, pady=10)

# Event listener to load selected data
tree.bind("<ButtonRelease-1>", lambda e: get_data(e))


    # update treeview


fetch_data()
root.mainloop()


