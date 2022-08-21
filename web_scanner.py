import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()
cookies = {
    '_ga_GR4KJ51T5B': 'GS1.1.1651692257.1.0.1651693215.0',
    '_ga': 'GA1.1.327657774.1651692257',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_ga_GR4KJ51T5B=GS1.1.1651692257.1.0.1651693215.0; _ga=GA1.1.327657774.1651692257',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

# Read a file
with open("top-100.csv", "r") as f:
    data = f.read()
lines = data.split("\n")

for line in lines:
    url = "https://"+line.split(",")[1]    # ["1", "netflix.com"]
    print(f"🚀 URL : {url}\n")
    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        headers = response.headers
        print(f"title : {soup.title.string}\n")
    except Exception as e:
        print(f"Exception in getting header : {e}")


print("--- %s seconds ---" % (time.time() - start_time))