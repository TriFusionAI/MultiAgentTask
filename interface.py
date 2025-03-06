import json
import re
import streamlit as st
from Dev.Agent.syscore import Agent, ResearchAgent, StockResearchAgent, NewsRetrievalAgent, AnalysisAgent

def agentFlow():
    # Research
    agent = ResearchAgent()
    agent.human = ""
    stock_data = agent.interact()

    # Tickers Generation
    agent = StockResearchAgent()
    agent.human = f"{stock_data}"
    tickers = agent.chat_interact()

    # News Retrieval Agent
    agent = NewsRetrievalAgent()
    agent.human = f""
    news_data = agent.interact()

    # Analysis
    agent = AnalysisAgent()
    agent.human = f"Create a Analysis report for this\n Top Stocks for the day {stock_data}\n News of the day {news_data}"
    data = agent.chat_interact()

    # Compiler Agent
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
    response = llmagent.chat_interact().content
    # Extract JSON content between backticks
    match = re.search(r'```(.*?)```', response, re.DOTALL)
    if match:
        json_data = match.group(1).strip()
        try:
            return json.loads(json_data)
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON: {e}")
            return {}
    else:
        st.error("No JSON data found in the response.")
        return {}

def main():
    st.title('Stock Data and News Viewer')

    # Retrieve the JSON data from the agent flow
    data = agentFlow()

    # Display the raw JSON data
    st.subheader('Generated JSON Data')
    st.json(data)

    # Parse and display specific components
    st.subheader('Top Indices')
    for index in data.get('data', []):
        st.write(f"- {index.get('index', 'Unknown')}")

    st.subheader('News Highlights')
    for news in data.get('news', []):
        st.markdown(f"**{news.get('title', 'No Title')}**")
        st.write(news.get('description', 'No Description'))
        st.write(f"Source: {news.get('source', 'Unknown')} | Published: {news.get('published_at', 'N/A')}")
        if news.get('image_url'):
            st.image(news['image_url'])

if __name__ == '__main__':
    main()
