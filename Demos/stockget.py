# yahoo stock data scraper
#
import requests
from bs4 import BeautifulSoup
from pydoc import text

def searchyh():
  url = f"https://finance.yahoo.com/quote/ES%3DF/"
  headers = {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
  }
  response  = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, "html.parser")

  print(soup)

  results = []

  for item in soup.find_all('li', class_='box-item'):
    title = item.find('span', class_='symbol')
    if title:
        # print(title.text)
        return results
    else :
        return None



searchyh()
