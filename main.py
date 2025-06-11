import os
from twilio.rest import Client
import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

alphavantage_endpoint = "https://www.alphavantage.co/query"
alphavantage_api_key =  os.environ["ALPHAVANTAGE_API_KEY"]
newsapi_endpoint = "https://newsapi.org/v2/everything"
newsapi_api_key = os.environ["NEWSAPI_API_KEY"]
account_sid =os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_TOKEN"]

av_parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey":alphavantage_api_key,
}


def percentage_difference(value1, value2):
    try:
        absolute_value = abs(value1 - value2)
        average_value = (value1 + value2) / 2
        perc_diff = (absolute_value / average_value) * 100
        return round(perc_diff, 2)
    except ZeroDivisionError:
        return "Error! Cannot Divide Zero"

def price_movement(yesterday, before):
    if yesterday > before:
        return "🔺"
    elif before > yesterday:
        return "🔻"
    else:
        return "="


response = requests.get(url=alphavantage_endpoint,params=av_parameters)
response.raise_for_status()
stock_data = response.json()


stock_dates = [key for key in stock_data["Time Series (Daily)"]]

yesterday_data = float(stock_data["Time Series (Daily)"][stock_dates[0]]["1. open"])
day_before = float(stock_data["Time Series (Daily)"][stock_dates[1]]["1. open"])
print(f"Yesterday: {yesterday_data}")
print(f"Day Before: {day_before}")
print(f"\nDifference: {percentage_difference(yesterday_data, day_before)}%")
if percentage_difference(yesterday_data,day_before) >= 5:
    print("Get News")


n_api_parameters = {
    "q":COMPANY_NAME,
    "from":stock_dates[0],
    "sortBy":"popularity",
    "apiKey":newsapi_api_key
}
news_response = requests.get(url=newsapi_endpoint,params=n_api_parameters)
news_response.raise_for_status()
news_data = news_response.json()
print(news_data)


header = f"TSLA: {price_movement(yesterday_data, day_before)}{percentage_difference(yesterday_data, day_before)}"
headline = f"Headline: {news_data["articles"][0]["title"]}"
detail = f"Brief: {news_data["articles"][0]["description"]}"

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=f"{header}\n{headline}\n{detail}",
    to='whatsapp:+639993543575'
)

print(message.status)


