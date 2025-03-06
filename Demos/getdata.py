from os import getenv
import requests
from dotenv import load_dotenv

load_dotenv()
api = getenv('ALPHAVANTAGE_API')

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GC&apikey={api}'
r = requests.get(url)
data = r.json()

# Extract the time series data
time_series = data.get('Time Series (Daily)', {})

# Get the last four dates (today and the previous three days)
last_four_days = sorted(time_series.keys(), reverse=True)[:4]

# Print the data for the last four days
for date in last_four_days:
    print(f"Date: {date}")
    for key, value in time_series[date].items():
        print(f"  {key}: {value}")
