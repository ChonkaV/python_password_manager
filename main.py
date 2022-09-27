from tkinter import *
from random import choice, randint, shuffle
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_number = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_number
    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = website_entry.get()
    mail = email_entry.get()
    code = pass_entry.get()
    new_data = {
        web: {
            "email": mail,
            "password": code
        }
    }

    if len(web) == 0 or len(code) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")

    else:
        # is_ok = messagebox.askokcancel(title=web, message=f"These are the details entries:\nEmail: {mail}"
        #                                                   f"\nPassword: {code}\nIs it OK to save?")
        try:
            with open("data.json", "r") as data_file:
                # Convert to json data to the python dict. but we have to change "w" to "r". Reading the data
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            # update data to json file (add more data)
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Write data to a json file
                json.dump(data, data_file, indent=4)

        finally:
            website_entry.delete(0, END)
            pass_entry.delete(0, END)
            print(new_data)


# ---------------------------- Find Password ------------------------------- #

def find_password():
    web_site = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")

    else:
        if web_site in data:
            email = data[web_site]["email"]
            password = data[web_site]["password"]
            messagebox.showinfo(title=web_site, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="ERROR", message=f"No details for {web_site} exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager GUI")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website = Label(text="Website:")
website.grid(column=0, row=1)

email_username = Label(text="Email/Username:")
email_username.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=27)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=45)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "viktor_python@gmail.com")

pass_entry = Entry(width=27)
pass_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)
search_button.place(x=282, y=200)

gen_pass_button = Button(text="Generate Password", width=14, command=generate_password)
gen_pass_button.grid(column=2, row=3)

add_button = Button(text="Add", width=38, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
