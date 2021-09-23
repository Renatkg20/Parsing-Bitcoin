import requests 
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd
import time

"""
url = "https://finance.yahoo.com/quote/BTC-USD/"
def get_coin_price(url):
    res = requests.get(url).content
    soup = BeautifulSoup(res, "html.parser")
    soup = soup.find("div", {"class":"D(ib)"})
    fin = soup.get_text("\n").split("\n")
    return fin
"""

url = "https://tradingeconomics.com/btcusd:cur"

def get_coin_price(url):
    time1 = datetime.datetime.now()
    res = requests.get(url).content
    soup = BeautifulSoup(res, "html.parser")
    soup = soup.find("div", {"class":"market-header-values row"})
    fin = soup.get_text("")
    fin1 = re.sub(" +", " ", fin)
    fin2 = re.sub("\n +", " ", fin1)
    fin3 = re.sub("\r +", "", fin2)
    fin5 = fin3.strip().split("\n")
    return f" {fin5[0]} USD/BTC: {fin5[1]} \n {fin5[4] } {fin5[6]}  {fin5[7]} \n {fin5[10]} {fin5[12]} \n Time: {time1}"

def telegram_bot_sendtext(bot_message):
    bot_token = '1272032516:AAEFp8g4Y67bB_DuzH4GEWHS3M69zO1l88g'
    bot_chatID = '535448074'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


# print(get_coin_price(url).split("\n").split(":"))

#  df = pd.DataFrame("Price of BTC" : [])

def convert_data_df():
    res = get_coin_price(url).split("\n")
    #res1 = " ".join(res).split("\n")
    #name_btc = res[0].split(":")[0]
    price_btc = res[0].split(":")[1]
    #daily_title = res[1].split(":")[0]
    daily_chg = res[1].split(":")[1]
    daily_prc = (res[1].split(":")[1]).strip().split(" ")[2]
    #yearly_title = res[2].split(":")[0]
    yearly_prs = res[2].split(":")[1]
    df = pd.DataFrame({ name_btc : price_btc, daily_title : daily_chg, "Persent % per day": daily_prc, yearly_title:yearly_prs}, index = [1])
    df.to_csv("btc_data.csv",index = False, mode = 'a') 

    # return name_btc, price_btc, daily_title, daily_chg, daily_prc, yearly_title, yearly_prs
    return df

for i in range(100):
    print(convert_data_df())
    time.sleep(60)