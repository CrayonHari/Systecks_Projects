import shutil
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
from tkinter.font import Font
import os
import sqlite3
import glob

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("user_data.db")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL)''')
        self.conn.commit()

    def insert_user(self, name, email, password):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO users (name, email, password) VALUES (?, ?, ?)''',
                       (name, email, password))
        self.conn.commit()

    def fetch_user(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE email=? AND password=?''', (email, password))
        return cursor.fetchone()

class Login():
    def __init__(self, root, database):
        self.root = root
        self.root.title("File Manager")
        self.database = database

        self.log_in = ttk.Label(root, text='        Welcome        ', padding=30,
                                font=Font(family='Helvetica', size=30, weight='normal', underline=True))
        self.log_in.pack(pady=50)
        self.frame = ttk.Frame()
        self.frame.pack(pady=10)
        self.email_label = ttk.Label(self.frame, text="Email:", font=('Helvetica', 15))
        self.email_label.pack(pady=10, anchor='w')
        self.email_entry = ttk.Entry(self.frame, font=('Helvetica', 15))
        self.email_entry.pack(pady=10)

        self.password_label = ttk.Label(self.frame, text="Password:", font=('Helvetica', 15))
        self.password_label.pack(pady=10, anchor='w')
        self.password_entry = ttk.Entry(self.frame, show="*", font=('Helvetica', 15))
        self.password_entry.pack(pady=10)

        self.login_button = ttk.Button(self.frame, text="Login", width=10, command=self.login)
        self.login_button.pack(padx=10, pady=10)

        self.text = ttk.Label(self.frame, text='New User?', font=('Helvetica', 12))
        self.text.pack(side="left", padx=10, pady=10)

        self.signup_button = ttk.Button(self.frame, text="Sign Up", width=10, command=self.signup)
        self.signup_button.pack(side="left", padx=10, pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email == "" or password == "":
            messagebox.showerror("Error", "Please enter both username and password.")
        else:
            user_data = self.database.fetch_user(email, password)
            if user_data:
                messagebox.showinfo("Success", "Login successful!")
                self.root.withdraw()
                self.email_entry.delete(0, 'end')  # Clear the email entry box
                self.password_entry.delete(0, 'end')  # Clear the password entry box
                application = tk.Toplevel(self.root)
                application.title("Project Manager")
                app = Application(application)
                app.upload_section()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

    def signup(self):
        self.root.withdraw()
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("520x520")
        SignUP(signup_window, self.database)  # Pass the database instance to the SignUP class

class SignUP:
    def __init__(self, master, database):
        self.master = master
        self.master.title("Sign Up")
        self.database = database

        self.frame = ttk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        self.name_label = ttk.Label(self.frame, text="Name:", font=('Helvetica', 15))
        self.name_label.pack(pady=(10, 5), anchor='w')
        self.name_entry = ttk.Entry(self.frame, font=('Helvetica', 15))
        self.name_entry.pack(pady=(0, 10))

        self.email_label = ttk.Label(self.frame, text="Email:", font=('Helvetica', 15))
        self.email_label.pack(pady=(10, 5), anchor='w')
        self.email_entry = ttk.Entry(self.frame, font=('Helvetica', 15))
        self.email_entry.pack(pady=(0, 10))

        self.password_label = ttk.Label(self.frame, text="Password:", font=('Helvetica', 15))
        self.password_label.pack(pady=(10, 5), anchor='w')
        self.password_entry = ttk.Entry(self.frame, show="*", font=('Helvetica', 15))
        self.password_entry.pack(pady=(0, 10))

        self.confirm_password_label = ttk.Label(self.frame, text="Confirm Password:", font=('Helvetica', 15))
        self.confirm_password_label.pack(pady=(10, 5), anchor='w')
        self.confirm_password_entry = ttk.Entry(self.frame, show="*", font=('Helvetica', 15))
        self.confirm_password_entry.pack(pady=(0, 10))

        self.signup_button = ttk.Button(self.frame, text="Sign Up", width=10, command=self.signup)
        self.signup_button.pack(pady=(20, 10))

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def signup(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validate entries
        if not name or not email or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
        else:
            # Call the insert_user method with username and password
            self.database.insert_user(name,email, password)
            messagebox.showinfo("Success", "Signup successful!")
            self.master.destroy()  # Close the signup window
            # Open the login window
            root.deiconify()  # Restore the login window

    def on_close(self):
        self.master.destroy()
        root.deiconify()


class Application(ttk.Frame):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.geometry("720x720")  # Set window size to 600x600
        self.root.title("File Manager")

        # Add logout button in the top right corner
        self.logout_button = ttk.Button(root, text="Logout", command=self.logout)
        self.logout_button.pack(side="top", anchor="ne", padx=10, pady=10)

        self.heading = ttk.Label(root, text="File Management Options",
                                 font=Font(family="helvetica", size=30, underline=True))
        self.heading.pack(pady=50)

        self.frame = ttk.Frame(root)
        self.frame.pack(pady=30)

        # Buttons
        self.upload_button = ttk.Button(self.frame, text="Upload a File", command=self.upload_section, width=15)
        self.upload_button.grid(row=0, column=0, padx=5)

        self.download_button = ttk.Button(self.frame, text="Download Files", command=self.download_section, width=15)
        self.download_button.grid(row=0, column=1, padx=5)

        self.manage_button = ttk.Button(self.frame, text="Manage Files", command=self.manage_section, width=15)
        self.manage_button.grid(row=0, column=2, padx=5)

        self.current_section = None

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)



    def upload_section(self):
        if self.current_section != "upload":
            self.remove_current_section()
            self.current_section = "upload"
            self.upload_frame = ttk.Frame(self.root)
            self.upload_frame.pack(pady=10)
            self.upload_frame_label = ttk.Label(self.upload_frame, text="Upload a File", font=("helvetica", 20))
            self.upload_frame_label.pack(pady=5)
            self.browse_button = ttk.Button(self.upload_frame, text="Browse File", command=self.browse_file, width=15)
            self.browse_button.pack(pady=5)
            self.selected_file_label = ttk.Label(self.upload_frame, text="")
            self.selected_file_label.pack(pady=5)
            self.upload_button_inside = ttk.Button(self.upload_frame, text="Upload", command=self.upload_file, width=15)
            self.upload_button_inside.pack(pady=5)

    def download_section(self):
        if self.current_section != "download":
            self.remove_current_section()
            self.current_section = "download"
            self.download_frame = ttk.Frame(self.root)
            self.download_frame.pack(pady=10)
            self.download_frame_label = ttk.Label(self.download_frame, text="Download Files", font=("helvetica", 20))
            self.download_frame_label.pack(pady=5)

            # Create treeview widget
            self.tree = ttk.Treeview(self.download_frame)
            self.tree["columns"] = ("Name", "Type", "Size", "Download")
            self.tree.heading("#0", text="Path")
            self.tree.heading("Name", text="Name")
            self.tree.heading("Type", text="Type")
            self.tree.heading("Size", text="Size")
            self.tree.heading("Download", text="Download")
            self.tree.column("#0", width=200)
            self.tree.column("Name", width=200)
            self.tree.column("Type", width=100)
            self.tree.column("Size", width=100)
            self.tree.column("Download", width=100)
            self.tree.pack(side="left", fill="both", expand=True)

            # Add scrollbar
            self.scrollbar = ttk.Scrollbar(self.download_frame, orient="vertical", command=self.tree.yview)
            self.scrollbar.pack(side="right", fill="y")
            self.tree.configure(yscrollcommand=self.scrollbar.set)

            # Populate treeview with files
            self.populate_treeview()

    def populate_treeview(self):
        # Clear existing items
        self.tree.delete(*self.tree.get_children())

        folder_path = r"D:\ECE\Sem5-Works\Systecks Solution Virtual Internship\Project_2\server"  # Folder path

        # Iterate over files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            file_size = os.path.getsize(file_path)
            file_type = "File" if os.path.isfile(file_path) else "Folder"
            file_size_str = f"{file_size} bytes" if os.path.isfile(file_path) else ""
            item_id = self.tree.insert("", "end", text=file_path,
                                       values=(file_name, file_type, file_size_str, ""))
            self.tree.tag_configure(item_id, foreground="blue")  # Changing color to simulate a button
            self.tree.item(item_id, text=file_path)  # Displaying full path
            self.tree.bind("<Button-1>", lambda event: self.handle_button_click(event))  # Binding click event

    def handle_button_click(self, event):
        item_id = self.tree.identify_row(event.y)
        item = self.tree.item(item_id)
        file_path = item['text']  # Get the file path from the clicked item
        save_path = os.path.join("downloaded_files", os.path.basename(file_path))
        try:
            shutil.copy2(file_path, save_path)  # Copy the file to the "downloaded_files" directory
            messagebox.showinfo("Success", "File downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading the file: {e}")

    def download_file(self, file_path):
        # Placeholder for file download functionality
        print("File downloaded:", file_path)

    def manage_section(self):

        if self.current_section != "manage":
            self.remove_current_section()
            self.current_section = "manage"
            self.manage_frame = ttk.Frame(self.root)
            self.manage_frame.pack(pady=10)

            # Added heading for manage section
            self.manage_frame_label = ttk.Label(self.manage_frame, text="Manage Files", font=("helvetica", 20))
            self.manage_frame_label.pack(pady=5)

            # Create a new treeview for managing downloaded files
            self.manage_tree = ttk.Treeview(self.manage_frame)
            self.manage_tree["columns"] = ("Name", "Type", "Size")
            self.manage_tree.heading("#0", text="Path")
            self.manage_tree.heading("Name", text="Name")
            self.manage_tree.heading("Type", text="Type")
            self.manage_tree.heading("Size", text="Size")
            self.manage_tree.column("#0", width=200)
            self.manage_tree.column("Name", width=200)
            self.manage_tree.column("Type", width=100)
            self.manage_tree.column("Size", width=100)

            # Add scrollbar
            self.scrollbar = ttk.Scrollbar(self.manage_frame, orient="vertical", command=self.manage_tree.yview)
            self.scrollbar.pack(side="right", fill="y")

            self.manage_tree.pack(side="left", fill="both", expand=True)
            self.manage_tree.configure(yscrollcommand=self.scrollbar.set)

            self.delete_frame = tk.Frame(self.root)
            self.delete_frame.pack(pady=10)
            self.delete_button = ttk.Button(self.delete_frame, text="Delete File", command=self.delete_file, width=15)
            self.delete_button.pack()
            # Populate treeview with downloaded files
            self.populate_manage_treeview()

    def populate_manage_treeview(self):
        # Clear existing items

        self.manage_tree.delete(*self.manage_tree.get_children())

        # List files in the downloaded_files folder
        downloaded_files = glob.glob("D:/ECE/Sem5-Works/Systecks Solution Virtual Internship/Project2/downloaded_files/*")

        # Iterate over files in the downloaded_files list
        for file_path in downloaded_files:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_type = "File" if os.path.isfile(file_path) else "Folder"
            file_size_str = f"{file_size} bytes" if os.path.isfile(file_path) else ""
            self.manage_tree.insert("", "end", text=file_path,
                                    values=(file_name, file_type, file_size_str))

    def remove_current_section(self):
        if self.current_section == "upload":
            self.upload_frame.destroy()
        elif self.current_section == "download":
            self.download_frame.destroy()
        elif self.current_section == "manage":
            self.manage_frame.destroy()
            self.delete_frame.destroy()

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file_label.config(text=file_path)

    def upload_file(self):
        file_path = self.selected_file_label.cget("text")
        if file_path:
            try:
                # Get just the filename
                _, file_name = os.path.split(file_path)

                # Define the destination directory
                destination_folder = r"D:\ECE\Sem5-Works\Systecks Solution Virtual Internship\Project2\server"

                # Copy the file to the destination directory
                shutil.copy2(file_path, os.path.join(destination_folder, file_name))

                messagebox.showinfo("Success", "File uploaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while uploading the file: {e}")

    def delete_file(self):
        # Get the selected item from the treeview
        selected_item = self.manage_tree.focus()
        if selected_item:
            # Get the file path from the selected item
            file_path = self.manage_tree.item(selected_item, "text")

            # Remove the file
            try:
                os.remove(file_path)
                # Remove the item from the treeview
                self.manage_tree.delete(selected_item)
                messagebox.showinfo("Success", "File deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting the file: {e}")

    def logout(self):
        self.root.destroy()
        root.deiconify()

    def on_close(self):
        root.destroy()


if __name__ == "__main__":
    root = ttk.Window(themename='morph')
    root.geometry("540x720")
    database = Database()  # Create an instance of the Database class
    app = Login(root, database)  # Pass the database instance to the Login class
    root.mainloop()
