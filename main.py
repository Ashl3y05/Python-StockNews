import os
import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

alphavantage_endpoint = "https://www.alphavantage.co/query"
alphavantage_api_key =  os.environ["ALPHAVANTAGE_API_KEY"]
newsapi_endpoint = "https://newsapi.org/v2/everything"
newsapi_api_key = os.environ["NEWSAPI_API_KEY"]

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

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

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

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
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
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


