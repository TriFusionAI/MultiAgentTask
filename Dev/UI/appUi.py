import streamlit as st
import yfinance as yf
import requests
from datetime import datetime

# Configuration
NEWS_API_KEY = "916530b0499849dbb2f440ef449dd00f"  # Replace with your actual API key
NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=916530b0499849dbb2f440ef449dd00f"

# Top 5 US Stock Market Indices
STOCKS = {
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "NASDAQ": "^IXIC",
    "Russell 2000": "^RUT",
    "NYSE Composite": "^NYA"
}

def get_stock_data():
    stock_data = {}
    for name, symbol in STOCKS.items():
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if not data.empty:
            stock_data[name] = {
                "Price": data["Close"].iloc[-1],
                "Change": data["Close"].iloc[-1] - data["Open"].iloc[-1],
                "Percentage Change": ((data["Close"].iloc[-1] - data["Open"].iloc[-1]) / data["Open"].iloc[-1]) * 100
            }
    return stock_data

def get_news():
    try:
        response = requests.get(NEWS_API_URL)
        response.raise_for_status()
        news_data = response.json()
        return news_data.get("articles", [])[:5]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return []

# Streamlit UI
st.set_page_config(page_title="US Stock Market & News", layout="wide")

st.title("📈 US Stock Market & News Dashboard")
st.write(f"*Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

# Stock Market Data
st.header("Market Overview")
stock_data = get_stock_data()
col1, col2 = st.columns(2)

for idx, (name, data) in enumerate(stock_data.items()):
    col = col1 if idx % 2 == 0 else col2
    with col:
        st.subheader(name)
        st.metric(label="Current Price", value=f"${data['Price']:.2f}",
                  delta=f"{data['Change']:.2f} ({data['Percentage Change']:.2f}%)")

st.markdown("---")

# News Section
st.header("Latest Business News")
news_articles = get_news()
for article in news_articles:
    with st.expander(article["title"]):
        st.write(article["description"])
        st.markdown(f"[Read more]({article['url']})")

st.markdown("---")
st.write("*Data provided by Yahoo Finance & NewsAPI.org* 📊📰")
