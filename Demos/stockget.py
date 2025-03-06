# yahoo stock data scraper
#
import requests
from bs4 import BeautifulSoup

def searchyh():
  url = f"https://finance.yahoo.com/quote/ES%3DF/"
  response  = requests.get(url)
  soup = BeautifulSoup(response.text, "html.parser")

  print(soup)

  results = []

  for item in soup.find_all('li', class_='box-item'):
    title = item.find('span', class_='symbol')
    # price = item.find('span', class_='s-item__price')
    # link = item.find('a', class_='s-item__link')
    print(title)
    # if title and price and link:
    #   results.append({
    #       'title': title.text,
    #       'price': price.text,
    #       'link': link['href']
    #   })

  return results


searchyh()
