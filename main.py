from datetime import datetime, timedelta
import requests
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
account_sid = "your_account_sid_here_twilio"
auth_token = "your_auth_token_here_twilio"
av_api_key = "your_av_api_key"
news_api_key = "your_news_api_key"
av_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": av_api_key
}
news_parameters = {
    "q": COMPANY_NAME,
    "apikey": news_api_key
}

av_response = requests.get(url="https://www.alphavantage.co/query", params=av_parameters)
av_response.raise_for_status()
av_data = av_response.json()["Time Series (Daily)"]


yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
two_days_ago = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
yesterday_close = float(av_data[yesterday]["4. close"])
two_days_ago_close = float(av_data[two_days_ago]["4. close"])
if yesterday_close >= 1.05 * two_days_ago_close or yesterday_close <= 0.95 * two_days_ago_close:
    news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]
    for article in news_data:
        percentage_change = int(round((two_days_ago_close - yesterday_close) / yesterday_close, 2) * 100)
        if percentage_change >= 0:
            percentage_change = f"🔺{percentage_change}%"
        else:
            percentage_change = f"🔻{abs(percentage_change)}%"

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"\n{STOCK}: {percentage_change}\n"
                 f"Headline:\n"
                 f"{article['title']}\n"
                 f"Brief:\n"
                 f"{article['description']}",
            from_="your twilio from number here",
            to="your to number here"
        )
