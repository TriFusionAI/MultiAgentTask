import json
import streamlit as st
from Dev.Agent.syscore import Agent, ResearchAgent, StockResearchAgent, NewsRetrievalAgent, AnalysisAgent

def agentFlow():
    # Research
    agent = ResearchAgent()
    stock_data = agent.interact()

    # Tickers Generation
    agent = StockResearchAgent()
    agent.human = f"{stock_data}"

    tickers = agent.chat_interact()

    # News Retrieval Agent
    agent = NewsRetrievalAgent()
    news_data = agent.interact()

    # Analysis
    agent = AnalysisAgent()
    agent.human = f"Create an Analysis report for this\nTop Stocks for the day {stock_data}\nNews of the day {news_data}"
    analysis_data = agent.chat_interact()

    # Compiler Agent
    llmagent = Agent()
    llmagent.human = f"""
    Create a usable JSON file for a UI with the structure:
    {{
        "title": "top_indicies",
        "data": "< >",
        "news": "< >"
    }}
    NO COMMENTS
    indices = {stock_data}
    news = {news_data}
    """
    response = llmagent.chat_interact().content

    # Try to parse the response as JSON directly
    try:
        start_index = response.find('{')
        end_index = response.rfind('}')
        if start_index != -1 and end_index != -1:
            json_data = response[start_index:end_index + 1]
            return json.loads(json_data)
        else:
            st.error("No valid JSON structure found in the response.")
            return {}
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return {}

def main():
    st.title('Stock Data and News Viewer')
    with st.spinner('Loading data... Please wait.'):
        data = agentFlow()
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

    st.subheader('Generated JSON Data')
    st.json(data)

if __name__ == '__main__':
    main()
