import sqlite3
import hashlib
import subprocess
from tkinter import *
from tkinter import messagebox

# Only now use Tk()
root = Tk()



def create_users_table():
    conn = sqlite3.connect('employees.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    # Insert default user: admin / admin123
    hashed_pw = hashlib.sha256("admin123".encode()).hexdigest()
    cur.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', hashed_pw))
    conn.commit()
    conn.close()

def login():
    username = user_var.get()
    password = pass_var.get()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('employees.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
    result = cur.fetchone()
    conn.close()

    if result:
        root.destroy()
        subprocess.Popen(["python", "employee_management.py"])
    else:
        messagebox.showerror("Error", "Invalid credentials")
create_users_table()

root.title("Login")
root.geometry("300x200")
root.configure(bg="#f0f0f0")

user_var = StringVar()
pass_var = StringVar()

Label(root, text="Username:", bg="#f0f0f0").pack(pady=5)
Entry(root, textvariable=user_var).pack()

Label(root, text="Password:", bg="#f0f0f0").pack(pady=5)
Entry(root, textvariable=pass_var, show="*").pack()

Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()