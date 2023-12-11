import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3

mage_path = "assets/photo.png"
original_image = Image.open(mage_path)
resized_image = original_image.resize((100, 100))
# اتصال به پایگاه داده
conn = sqlite3.connect('phonebook.db')

# ایجاد یک cursor
cursor = conn.cursor()

# ایجاد یک جدول برای ذخیره اطلاعات مخاطبان اگر وجود نداشته باشد
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone_number TEXT
    )''')


def add_contact_to_database(name, phone_number):
    cursor.execute('INSERT INTO contacts (name, phone_number) VALUES (?, ?)', (name, phone_number))
    conn.commit()


def search_contact_in_database(name):
    cursor.execute('SELECT * FROM contacts WHERE name = ?', (name,))
    return cursor.fetchall()


def display_all_contacts_in_database():
    cursor.execute('SELECT * FROM contacts')
    return cursor.fetchall()


def delete_contact_from_database(name):
    cursor.execute('DELETE FROM contacts WHERE name = ?', (name,))
    conn.commit()


def add_contact():
    name = name_entry.get()
    phone_number = phone_entry.get()

    if name and phone_number:
        add_contact_to_database(name, phone_number)

        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Contact added successfully!")
    else:
        messagebox.showwarning("Error", "Please enter both name and phone number.")


def search_contact():
    name = name_entry.get()

    if name:
        contacts = search_contact_in_database(name)

        if contacts:
            messagebox.showinfo("Contact Found", f"Name: {contacts[0][1]}\nPhone Number: {contacts[0][2]}")
        else:
            messagebox.showinfo("Contact Not Found", f"No contact found with the name '{name}'")
    else:
        messagebox.showwarning("Error", "Please enter a name to search.")


def display_contacts():
    contacts = display_all_contacts_in_database()

    if contacts:
        contacts_info = ""
        for contact in contacts:
            contacts_info += f"Name: {contact[1]}, Phone Number: {contact[2]}\n"
        messagebox.showinfo("Contacts", contacts_info)
    else:
        messagebox.showinfo("No Contacts", "No contacts found.")


def delete_contact():
    name = name_entry.get()

    if name:
        delete_contact_from_database(name)

        name_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")
    else:
        messagebox.showwarning("Error", "Please enter a name to delete.")


def exit_app():
    conn.close()
    root.quit()


root = tk.Tk()
photo = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(root, image=photo)
image_label.grid(row=0, column=0, columnspan=2, pady=10)
root.title("Phonebook Application")
root.configure(bg='blue')

# Labels
tk.Label(root, text="Name:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Phone Number:").grid(row=2, column=0, padx=5, pady=5)

# Entry Fields
name_entry = tk.Entry(root)
phone_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=5, pady=5)
phone_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Contact", command=add_contact).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Search Contact", command=search_contact).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="Display Contacts", command=display_contacts).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="Delete Contact", command=delete_contact).grid(row=6, column=0, columnspan=2, pady=10)
tk.Button(root, text="Exit", command=exit_app).grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
