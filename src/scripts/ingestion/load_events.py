
import requests
from bs4 import BeautifulSoup
import json
import datetime

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
    soup=BeautifulSoup(resp.text,features="html.parser")
    json_data = soup.find(id="Evenemangslistning").next_sibling
    json_dict = json.loads(json_data)

    events_lan_list = json_dict["searchHits"]
    events_lan_total = json_dict["searchInfo"]["totalHits"]

    events_lan_list_filepath = "src/data/raw/events_lan_list.json"
    with open(events_lan_list_filepath, "w", encoding="utf-8") as f:
      json.dump(events_lan_list, f, ensure_ascii=False, indent=4)
    
    with open(events_lan_list_filepath, "r", encoding="utf-8") as f:
        ev = json.load(f)
        if events_lan_total==len(ev):
          print(datetime.datetime.now().strftime('%d %b %Y, %H:%M')," : Event data (" + str(events_lan_total) + " events) from Jönköping Evenemangskalender has been successfully scraped and saved")
  else:
    print("The website is down. Please try again later : ",resp.status_code)
except Exception as e:
  print("Problems with scraping the website. Please check the following error message :", e)

