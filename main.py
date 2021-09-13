import requests
import json
from twilio.rest import Client
from smtplib import SMTP

NAME_URL = "https://api.coindcx.com/exchange/v1/markets_details"
PRICE_URL = "https://public.coindcx.com/market_data/trade_history"


def get_crypto_data():
    name_url = NAME_URL
    response = requests.get(name_url)
    datum = response.json()

    for data in datum:
        new_data = {datum.index(data): {key: data[key] for key in data}}
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


def get_coin_pair(coin_list):
    coin_name, alert_price, margin, base_coin = coin_list
    try:
        with open("coin_data.json", "r") as file:
            datum = json.load(file)
            for key in datum:
                if datum[key]["base_currency_short_name"] == base_coin:
                    if datum[key]["target_currency_name"] == coin_name or datum[key]["target_currency_short_name"] == coin_name:
                        add_to_watchlist([datum[key]["pair"], coin_name, alert_price, margin])

    except FileNotFoundError:
        print("No file found in client side")


def add_to_watchlist(coin_list):
    coin_pair, coin, alert_price, margin = coin_list
    if coin_pair:
        try:
            with open("watch_list.txt", "a") as file1:
                file1.write(f"{coin}||{coin_pair}||{alert_price}||{margin}\n")

        except FileNotFoundError:
            with open("watch_list.txt") as file1:
                file1.write(f"{coin}||{coin_pair}||{alert_price}||{margin}\n")
