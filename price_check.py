import time

from main import *

SID = "Your SID"
SECRET_KEY_Twilio = "Your Auth key"


# Getting the price of the particular crypto with its coin_pair
def check_price(pair):
    price_url = PRICE_URL
    params = {
        "pair": pair,
        "limit": "1"
    }
    response = requests.get(price_url, params=params)
    # returning the price of that crypto
    return response.json()[0]["p"]


# Get a list of coins to send alert
def alert_user(messages):
    if messages:
        msg = ""
        delete_list = []
        print("creating alert")
        # Creating a message that contains the name of the coin and price of the coin
        for message in messages:
            # message[0] is the name of the coin, message[1] is the current price of the coin
            msg += f"{message[0]} is now {message[1]}\n"
            delete_list.append(message[0])
        print(msg)

        # Once the message is created the particular coins in the watch list is deleted to avoid repeating
        if len(delete_list) > 0:
            with open("watch_list.txt") as file2:
                data = file2.readlines()
            with open("watch_list.txt", "w") as file3:
                for line in data:
                    name = line.split("||")[0]
                    if name not in delete_list:
                        file3.write(line)

        client = Client(SID, SECRET_KEY_Twilio)
        message = client.messages.create(
            from_='Twillo number ',
            body=msg,
            to='receiver number'
        )
        client.calls.create(to="+919360562973", from_="+13204463938", url="http://demo.twilio.com/docs/voice.xml")


# Checking the prices of the cryptos in watch list
def price_message():
    coins = []
    with open("watch_list.txt") as file:
        coin_list = file.readlines()
        print(coin_list)
        for coin in coin_list:
            coin_name, pair, alert_price, margin = coin.split("||")
            # getting current price of a crypto
            current_price = check_price(pair)
            # If the crypto's price satisfies the any of the below condition add the crypto to the coins list to send
            # alert
            if margin.strip("\n") == "below":
                if current_price <= float(alert_price):
                    coins.append([coin_name, current_price])
            elif margin.strip("\n") == "above":
                if current_price >= float(alert_price):
                    coins.append([coin_name, current_price])
        return coins


while True:
    # Looping it every 120 secs
    alert_user(price_message())
    time.sleep(120)
