
import requests
from bs4 import BeautifulSoup
import json

# Scrape event data from Jönköping municipality website

url = "https://www.jonkoping.se/evenemangskalender/evenemangskalender?filters=%7B%7D&page=1000&pageMode=all&query=&sv.12.27b6a9cc17cdfe279de33aae.route=%2Fsearch&sv.target=12.27b6a9cc17cdfe279de33aae&timestamp=1743355834489"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.jonkoping.se/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

try:
  resp = requests.get(url,headers=header)
  if resp.status_code == 200:
    soup=BeautifulSoup(resp.text)
    json_data = soup.find(id="Evenemangslistning").next_sibling
    json_dict = json.loads(json_data)

    events_list = json_dict["searchHits"]
    events_total = json_dict["searchInfo"]["totalHits"]

    print(events_total,len(events_list))
  else:
    print("The website is down. Please try again later : ",resp.status_code)
except Exception as e:
  print("Invalid website. Please check the following error message :", e)

