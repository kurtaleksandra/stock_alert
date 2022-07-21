import requests
import datetime
from twilio.rest import Client
import random

date = str(datetime.datetime.now())[0:11]

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
APIKEY_STOCK = 'CLVM22O424DZMMYL'
APIKEY_NEWS = '4f99051c1f2b4a78961e69bbe2fb51cd'
ACCOUNT_SID = "ACbb5fe55657e67c77a74de2b721985f53"
ACCOUNT_TOKEN = "ef77490674686da58f602685b99395e8"
PHONE_NUMBER = "+18304520698"

parameters_stock = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': APIKEY_STOCK,
}

response_stock = requests.get(url='https://www.alphavantage.co/query', params=parameters_stock)
response_stock.raise_for_status()
stock_data = response_stock.json()

stock_list = [stock_data["Time Series (Daily)"][key]["4. close"] for key in stock_data["Time Series (Daily)"]][:2]
perc_difference = round((float(stock_list[0]) - float(stock_list[1])) / float(stock_list[1]) * 100, 0)

parameters_news = {
    "q": "Tesla&",
    "from": date,
    "sortBy": "publishedAt&",
    "language": "en",
    "apiKey": APIKEY_NEWS
}

response_news = requests.get(url="https://newsapi.org/v2/everything", params=parameters_news)
response_news.raise_for_status()
news_data = response_news.json()

three_news = news_data["articles"][0:4]
title = "title"
description = "description"
random_news = random.randint(0, 2)

if perc_difference < 0:
    up_down = "↓"
else:
    up_down = "↑"

message_text = f"TSLA: {up_down} {abs(perc_difference)}%\nHeadline:{three_news[random_news][title]}\nDescription: {three_news[random_news][description]}"

if abs(perc_difference) >= 5:
    client = Client(ACCOUNT_SID, ACCOUNT_TOKEN)
    message = client.messages \
        .create(
        body=message_text,
        from_=PHONE_NUMBER,
        to="+48883965983"
    )
    print(message.status)
