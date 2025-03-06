import sys
from typing import Self, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
import streamlit as st

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

# Base Agent class
class Agent:
    def __init__(self):
        self.chat = ChatGroq(temperature=0, model_name="llama3-8b-8192")
        self.system = ""
        self.human = ""
        self.tools = {}

    def register_tool(self, name: str, tool_func):
        """Register a tool for the agent to use."""
        self.tools[name] = tool_func

    def interact(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system),
            ("human", self.human)
        ])
        # Execute the tool if requested
        if "research" in self.tools:
            result = self.tools["research"]({})
            print("Tool Output:", result)

class ResearchAgent(Agent):
    def __init__(self):
        super().__init__()
        self.system = "You are an Agent designed to list the most available stocks using the research tool."
        self.register_tool("research", research)

# Instantiate and test the ResearchAgent
agent = ResearchAgent()
agent.human = "Show me the top stocks."
agent.interact()
