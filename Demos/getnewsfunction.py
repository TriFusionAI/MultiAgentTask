import streamlit as st
import requests

# Alpha Vantage API Key (Replace with your actual API Key)
API_KEY = "ALPAVANTAGE_API"

# Function to fetch stock-related news for a given company symbol
def get_stock_news(company_symbol):
    try:
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={company_symbol}&apikey={API_KEY}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        news_data = response.json().get("feed", [])  # Extract news articles
        if not news_data:
            return [{"title": "No news found", "description": "Try another company.", "url": "#"}]
        
        return news_data[:5]  # Return top 5 articles

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return [{"title": "Error fetching news", "description": "Check API key or network.", "url": "#"}]

# Streamlit UI
st.title("📈 Stock Market News")

# Input for the user to enter a stock ticker (e.g., IBM, AAPL)
company_symbol = st.text_input("Enter a company stock symbol (e.g., IBM, AAPL, TSLA)", "IBM")

if company_symbol:
    st.header(f"Latest News for {company_symbol}")

    # Fetch news
    news_articles = get_stock_news(company_symbol)

    # Display news articles
    for article in news_articles:
        with st.expander(article["title"]):
            st.write(article.get("summary", "No description available."))
            st.markdown(f"[Read more]({article['url']})")

    st.markdown("---")
    st.write("*Data provided by Alpha Vantage* 📊📰")
