import requests
import json
from twilio.rest import Client
from smtplib import SMTP

NAME_URL = "https://api.coindcx.com/exchange/v1/markets_details"
PRICE_URL = "https://public.coindcx.com/market_data/trade_history"


# Get all crypto currencies details from coindcx api
def get_crypto_data():
    name_url = NAME_URL
    # print("got the response")
    response = requests.get(name_url)
    # Getting data as json
    datum = response.json()
    # print("got the response")

    for data in datum:
        new_data = {datum.index(data): {key: data[key] for key in data}}
        # Writing data from json to a json file
        try:
            with open("coin_data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("coin_data.json", "w") as file1:
                json.dump(new_data, file1, indent=4)
        else:
            data.update(new_data)

            with open("coin_data.json", "w") as file1:
                json.dump(data, file1, indent=4)


# To get details of a particular crypto we want coin_pair of that crypto
def get_coin_pair(coin_list):
    coin_name, alert_price, margin, base_coin = coin_list
    try:
        with open("coin_data.json", "r") as file:
            datum = json.load(file)
            for key in datum:
                # to get coin pair we need base coin of that crypto eg:INR, BITCOIN etc... else we get multiple
                # crypto of same name but with different base coin
                if datum[key]["base_currency_short_name"] == base_coin:
                    # target_currency_name is full name of the crypto (Ripple) target_currency_short_name(XRP)
                    if datum[key]["target_currency_name"] == coin_name or datum[key]["target_currency_short_name"] == coin_name.upper():
                        add_to_watchlist([datum[key]["pair"], coin_name, alert_price, margin])

    except FileNotFoundError:
        print("No file found in client side")


# adding the crypto and its details like alert price, coin_pair , margin to watch list
def add_to_watchlist(coin_list):
    coin_pair, coin, alert_price, margin = coin_list
    if coin_pair:
        try:
            with open("watch_list.txt", "a") as file1:
                file1.write(f"{coin}||{coin_pair}||{alert_price}||{margin}\n")

        except FileNotFoundError:
            with open("watch_list.txt") as file1:
                file1.write(f"{coin}||{coin_pair}||{alert_price}||{margin}\n")
