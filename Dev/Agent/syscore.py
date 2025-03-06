import sys
from typing import Self, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from symtable import Symbol
# import streamlit as st

load_dotenv()

# TOOLS
#
@tool
def research(input: Optional[str] = None) -> list[str]:
    """Look up the top stocks from Yahoo Finance."""
    url = "https://finance.yahoo.com/quote/ES%3DF/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.find_all('li', class_='box-item'):
        title = item.find('span', class_='symbol')
        if title:
            results.append(title.text)
    return results

@tool
def searchStockInfo(ticker):
    """Retrieve past data from alphavantage"""
    api = getenv('ALPHAVANTAGE_API')
    results = []
    for ticker in data:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api}'
        data = (requests.get(url))
        dataextract = r.json()
        time_series = data.get('Time Series (Daily)', {})
        last_four_days = sorted(time_series.keys(), reverse=True)[:4]
        results.append(last_four_days)

    return results

@tool
def fetchNews(symbol):
    """Fetches news related to IBM stock."""
    api_key = os.getenv('MKTX_API')
    if not api_key:
        raise ValueError("API key not found. Please set the 'MKTX_API' environment variable.")

    url = f"https://api.marketaux.com/v1/news/all?countries=us&filter_entities=true&limit=10&published_after=2025-03-05T05:27&api_token={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
        return news_data.get('data', [])
    else:
        raise Exception(f"Failed to fetch news: {response.status_code} - {response.text}")

@tool
def googleSearch(query: str) -> str:
    """Search for stock ticker using Google Search API."""
    api_key = os.getenv('GOOGLE_API')
    cx = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    if not api_key or not cx:
        raise ValueError("Google API key or Search Engine ID not found.")

    url = f"https://www.googleapis.com/customsearch/v1?q={query} stock ticker&key={api_key}&cx={cx}"
    response = requests.get(url)

    if response.status_code == 200:
        search_data = response.json()
        if 'items' in search_data and search_data['items']:
            return search_data['items'][0]['link']
        else:
            return "No relevant results found."
    else:
        raise Exception(f"Failed to fetch search results: {response.status_code} - {response.text}")


# AGENTS

# Base Agent class
class Agent:
    def __init__(self):
        self.chat = ChatGroq(temperature=0, model_name="llama3-8b-8192")
        self.model = ChatGroq(temperature=0, model_name="llama3-8b-8192")

        self.system = ""
        self.human = ""
        self.tools = {}

    def register_tool(self, name: str, tool_func):
        """Register a tool for the agent to use."""
        self.tools[name] = tool_func

    def chat_interact(self):
        messages = [
            (
                "system",
                f"{self.system}"
            ),
            ("human", f"{self.human}"),
        ]
        response = self.model.invoke(messages)
        return response


    def interact(self, symbol=""):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system),
            ("human", self.human)
        ])
        # Execute the tool if requested
        if "research" in self.tools:
            result = self.tools["research"]({})
            # print("Tool Output:", result)
            return result

        if "fetchNews" in self.tools:
            result = self.tools["fetchNews"](symbol)
            # print("News Articles:", result)
            return result

        if "googleSearch" in self.tools:
            result = self.tools["googleSearch"](symbol)
            # print("Google Search Result:", result)
            return result

class ResearchAgent(Agent):
    def __init__(self):
        super().__init__()
        self.system = "You are an Agent designed to list the most available stocks using the research tool."
        self.register_tool("research", research)

class NewsRetrievalAgent(Agent):
    def __init__(self):
        super().__init__()
        self.system = "You are an agent designed to retrieve and summarize the news data fetched from the fetchNews tool."
        data = self.register_tool("fetchNews", fetchNews)
        # print(data)

class AnalysisAgent(Agent):
    def __init__(self):
        super().__init__()
        self.system = "Analyze the news and the top  stocks provided and create a sentiment report"

    # def analyze_data(self, stock_data, news_data):
    #     sentiment_report = f"Sentiment report based on stock data: {stock_data} and news data: {news_data}"
    #     return sentiment_report


class StockResearchAgent(Agent):
    def __init__(self):
        super().__init__()
        self.system = "no comments, just show the tickers in an array"

class PreProcessingAgent(Agent):
    def __init__(self):
        super().__init__()
        self.system = "Preprocess these data into a json file and show it. so we can display it no comments"

if __name__ == "__main__":
    # Instantiate and test the ResearchAgent
    agent = ResearchAgent()
    agent.human = ""
    stock_data = agent.interact()

    # TickerGenerator Agent
    agent = StockResearchAgent()
    agent.human = f"{stock_data}"
    tickers = agent.chat_interact()
    # print(tickers)

    # News Retrieval Agent
    agent = NewsRetrievalAgent()
    agent.human = f""
    news_data = agent.interact()

    # Sentiment Statement Generation Agent
    print("ANALYSIS----------------------")
    agent = AnalysisAgent()
    agent.human = f"Create a Analysis report for this\n Top Stocks for the day {stock_data}\n News of the day {news_data}"
    data = agent.chat_interact()
    # print(data)
    # Instantiate and test the ResearchAgent


    print("Final-----")
    llmagent = Agent()
    llmagent.human = f"""
    Create a Usable JSON file from this for a UI
    The structure should be

        title: "top_indicies"
        data: "< >"
        news: "< >"

    -----input data
    indices = {stock_data}
    news = {news_data}
    """
    data = llmagent.chat_interact()
    print(data.content)
