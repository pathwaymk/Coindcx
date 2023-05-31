from main import *
from tkinter import *
from tkinter import messagebox
Font_tuple = ("Helvetica", 20, "bold")


def get_details():
    coin_name = []
    coin_short_name = []

    with open("coin_name.txt") as file:
        data = file.readlines()
        for name in data:
            coin_name.append(name.strip("\n"))

    with open("coin_short.txt") as file:
        data = file.readlines()
        for name in data:
            coin_short_name.append(name.strip("\n"))

    coin = coin_name_entry.get().capitalize()
    alert_price = price_entry.get()
    margin = v.get()
    base_coin = base_coin_entry.get()

    # Checking weather the user enter the valid crypto coin
    if coin not in coin_name and coin.upper() not in coin_short_name:
        messagebox.showwarning("Crypto name", "No crypto find, Try again")
        return None
    # Checking weather all the entry in the app(form) is filled
    elif float(alert_price) < 0:
        messagebox.showwarning("Negative price", "Please enter price above zero")
        return None
    elif margin == "1":
        messagebox.showwarning("Radio box", "Please check the radio box")
        return None
    elif not base_coin:
        messagebox.showwarning("Base coin", "Please enter a valid base coin")
        return None
    # Removing all the entry in the form
    coin_name_entry.delete(0, END)
    # base_coin_entry.delete(0, END)
    price_entry.delete(0, END)
    coin_name_entry.focus_set()
    # Passing the data to get_coin_pair and then add to the watch list
    # get_crypto_data()
    get_coin_pair([coin, alert_price, margin, base_coin])
    messagebox.showinfo(title="Success", message=f"{coin} is added to the watch list")


# Creating UI for the app
window = Tk()
window.title("Crypto Reminder")
window.config(width=400, height=400, bg="#000000")
window.minsize(300, 400)
coin_entry_var = StringVar()
coin_price_var = StringVar()
base_coin_var = StringVar(window, "INR")
v = StringVar(window, "1")

head = Label(text="CRYPTO ALERT", bg="#000000", fg="#66FCF1", font=Font_tuple)
head.grid(row=0, column=0, columnspan=2)

coin_name_label = Label(text="Coin name: ", font=("Courier", 15, "bold"), fg="#FFFF00", bg="#000000")
coin_name_label.grid(row=1, column=0, padx=(20, 5), pady=20, sticky="w")

coin_name_entry = Entry(textvariable=coin_entry_var)
coin_name_entry.grid(row=1, column=1, padx=(0, 10))

price_label = Label(text="Alert Price: ", font=("Courier", 15, "bold"), fg="#FFFF00", bg="#000000")
price_label.grid(row=2, column=0, padx=(20, 5), pady=20, sticky="w")

price_entry = Entry(textvariable=coin_price_var)
price_entry.grid(row=2, column=1, padx=(0, 10))

base_coin_label = Label(text="Base coin: ", font=("Courier", 15, "bold"), fg="#FFFF00", bg="#000000")
base_coin_label.grid(row=3, column=0, padx=(20, 5), pady=20, sticky="w")

base_coin_entry = Entry(textvariable=base_coin_var)
base_coin_entry.grid(row=3, column=1, padx=(0, 10))

coin_alert_label = Label(text="Alert when the price is", font=("Courier", 15, "bold"), fg="#FFFF00", bg="#000000")
coin_alert_label.grid(row=4, column=0, columnspan=2, padx=(20, 5), pady=20)

below_radio = Radiobutton(text="Below alert price", variable=v, value="below", fg="#FFFF00", bg="#000000", activebackground="#000000", activeforeground="#FFFF00", selectcolor="black")
below_radio.grid(row=5, column=0, sticky="w", ipadx=15)

above_radio = Radiobutton(text="Above alert price", variable=v, value="above", fg="#FFFF00", bg="#000000", activebackground="#000000", activeforeground="#FFFF00", selectcolor="black")
above_radio.grid(row=5, column=1, sticky="w")

submit = Button(text="Add", fg="#000000", bg="#FFFF00", activebackground="#000000", activeforeground="#FFFF00", width=10, command=get_details)
submit.grid(row=6, column=0, columnspan=2, pady=(15, 0))

coin_name_entry.focus_set()

window.mainloop()
