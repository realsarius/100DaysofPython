import requests
from datetime import datetime, timedelta
from twilio.rest import Client
import json
import time

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
two_days_ago = str(datetime.now() - timedelta(days=3))
three_days_ago = str(datetime.now() - timedelta(days=4))
two_days_ago = two_days_ago.split()
three_days_ago = three_days_ago.split()

# print(two_days_ago[0]) # 2024-06-09

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# API calls for this service is limited to 25 calls per day
# parameters = {
#     "function": "TIME_SERIES_INTRADAY",
#     "interval": "60min",
#     "apikey": "YOUR_API_KEY",
#     "symbol": STOCK_NAME
# }

# r = requests.get(STOCK_ENDPOINT, params=parameters)
# r.raise_for_status()

# data = r.json()

# So I'm just using locally saved data from the data I've gathered from the API call.
file = open("data.json")
data = json.load(file)

# print(data)

#TODO 2. - Get the day before two_days_ago's closing stock price
two_days_ago_closing_value = 0
three_days_ago_closing_value = 0
for key, value in data["Time Series (60min)"].items():
    if key.split()[0] == two_days_ago[0] and key.split()[1] == "19:00:00":
        print(f"Two days ago, closing: {value['4. close']}")
        two_days_ago_closing_value = float(value['4. close'])
    if key.split()[0] == three_days_ago[0] and key.split()[1] == "19:00:00":
        print(f"Three days ago, closing: {value['4. close']}")
        three_days_ago_closing_value = float(value['4. close'])

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
positive_difference = abs(two_days_ago_closing_value - three_days_ago_closing_value)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = (positive_difference / ((two_days_ago_closing_value + three_days_ago_closing_value) / 2)) * 100
print(percentage_difference)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News"). 
if percentage_difference < 5:
    news_paramaters = {
        "apiKey": "YOUR_API_KEY",
        "q": COMPANY_NAME
    }
    news = requests.get(NEWS_ENDPOINT, params=news_paramaters)
    news.raise_for_status()
    news_data = news.json()
    articles = news_data["articles"]
    
    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

    article_titles = []
#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    for article in articles[:3]:
        article_titles.append({
            "article_title": article["title"],
            "article_link": article["url"],
            "article_brief": article["description"]
        })

    # print(article_titles)
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio. 

    account_sid = 'YOUR_ACCOUNT_SID'
    auth_token = 'YOUR_AUTH_TOKEN'
    client = Client(account_sid, auth_token)
    for article in article_titles:
        print(article["article_title"])
        msg = f"{STOCK_NAME}: {round(percentage_difference, 2)}\nHeadline: {article['article_title']}\nBrief: {article['article_brief']}"
        # print(msg)

        message = client.messages.create(
        body=msg,
        from_='TWILIO_PHONE_NUMBER',
        to='PHONE_NUMBER'
        )

        print(message.sid)
        time.sleep(1)


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

