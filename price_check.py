from main import *

my_email = "Your Email"
password = "Password"

SID = "Your SID"
SECRET_KEY_Twilio = "Secret key"


def check_price(pair):
    price_url = PRICE_URL
    params = {
        "pair": pair,
        "limit": "50"
    }
    response = requests.get(price_url, params=params)
    prices = []
    print("enter")
    for data in response.json():
        prices.append(float(data["p"]))
    print(min(prices))
    return min(prices)


def alert_user(messages):
    if messages:
        msg = ""
        delete_list = []
        for message in messages:
            msg += f"{message[0]} is now {message[1]}\n"
            delete_list.append(message[0])
        print(msg)

        if len(delete_list) > 0:
            with open("watch_list.txt") as file2:
                data = file2.readlines()
            with open("watch_list.txt", "w") as file3:
                for line in data:
                    name = line.split("||")[0]
                    if name not in delete_list:
                        file3.write(line)
        # with SMTP("smtp.gmail.com", 587) as mail_bot:
        #     mail_bot.starttls()
        #     mail_bot.login(user=my_email, password=password)
        #     mail_bot.sendmail(from_addr=my_email,
        #                       to_addrs="Target mail",
        #                       msg=f"SUBJECT: Price Alert \n\n{msg}")
        #
        # client = Client(SID, SECRET_KEY_Twilio)
        # client.calls.create(to="Target number", from_="Your number", url="http://demo.twilio.com/docs/voice.xml")


def price_message_low():
    print("price_message enter")
    coins = []
    with open("watch_list.txt") as file:
        coin_list = file.readlines()
        for coin in coin_list:
            coin_name, pair, alert_price, margin = coin.split("||")
            current_price = check_price(pair)
            if margin.strip("\n") == "below":
                if current_price <= float(alert_price):
                    coins.append([coin_name, current_price])
            elif margin.strip("\n") == "above":
                if current_price >= float(alert_price):
                    coins.append([coin_name, current_price])
        return coins


alert_user(price_message_low())
