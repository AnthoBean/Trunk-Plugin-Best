import requests

def fetch_latest_price():
    url = "https://hourlypricing.comed.com/api?type=5minutefeed"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # Return last 5 entries
    return data[-5:]
