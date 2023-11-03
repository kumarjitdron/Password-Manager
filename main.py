from tkinter import *
from tkinter import messagebox
import pyperclip
import random
import json
import rsa

# ---------------------------- PASSWORD ENCRYPTION ------------------------------- #
def encrypt(msg):
    with open("public.pem", "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    encrypt_message = rsa.encrypt(msg.encode(),pub_key=public_key)
    return encrypt_message

# ---------------------------- PASSWORD DECRYPYION ------------------------------- #
def decrypt(msg):
    with open("private.pem", "rb") as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
    decrypt_message = rsa.decrypt(msg, priv_key = private_key)
    return decrypt_message
    


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
    password_list = []
    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char
    pyperclip.copy(password)
    inputPass.insert(0, password)
# ---------------------------- SEARCH DATA ------------------------------- #


def search(website):
    with open("data.json", "r") as file:
        data = json.load(file)
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            password1 = bytes.fromhex(password)
            decrypt_password = decrypt(password1).decode()
            pyperclip.copy(decrypt_password)
            messagebox.showinfo(website, f"Email: {email}\nPassword: {decrypt_password}")
        else:
            messagebox.showerror(website, f"Website not exists")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    website = inputWeb.get()
    username = inputUser.get()
    password = inputPass.get()
    encrypted_password = encrypt(password)
    new_data = {
        website: {
            "email": username,
            "password": encrypted_password.hex()
        }

    }
    if len(password) == 0 or len(username) == 0 or len(website) == 0:
        messagebox.showerror("Data Missing", "Please Enter all Data")
    else:
        ans = messagebox.askyesno(website,
                                  f"These are the details entered: \nEmail: {username}\nPassword: {password}\nIs it ok to save?")
        if ans:
            try:
                with open("data.json", mode="r") as file:
                    # Reading old data
                    data = json.load(file)

            except FileNotFoundError:
                with open("data.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                # Saving updated data
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)   # json.dump() is used to write json data
            finally:
                inputWeb.delete(0, "end")
                inputPass.delete(0, "end")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=190)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 95, image=logo)
canvas.grid(column=2, row=1)

# label website
web = Label(text="Website: ", font=("Courier", 15, "bold"))
web.grid(column=1, row=2)

# Entry Website
inputWeb = Entry(width=32)
inputWeb.grid(column=2, row=2)

# label Email/Username
user = Label(text="Email/Username: ", font=("Courier", 15, "bold"))
user.grid(column=1, row=3)

# Entry Email/Username
inputUser = Entry(width=50)
inputUser.grid(column=2, row=3, columnspan=3)
inputUser.insert(0, "kumarjitdron69@gmail.com")

# label Password
user = Label(text="Password: ", font=("Courier", 15, "bold"))
user.grid(column=1, row=4)

# Entry Password
inputPass = Entry(width=32)
inputPass.grid(column=2, row=4)

# Generate Password Button
genPass = Button(text="Generate Password", highlightthickness=0, command=password_gen)
genPass.grid(column=3, row=4)

# Add Button
add_btn = Button(text="Add", highlightthickness=0, width=47, command=save_data)
add_btn.config(pady=10)
add_btn.grid(column=2, row=5, columnspan=3)

# search button
search_bt = Button(text="Search", highlightthickness=0, width=10, command=lambda: search(inputWeb.get()))
search_bt.grid(column=3, row=2)


window.mainloop()