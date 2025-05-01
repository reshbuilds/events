
import requests
from bs4 import BeautifulSoup
import json
import datetime

from src.paths import *

# Scrape event data from Jönköping municipality event website
def get_events_lan():
  lan_url = "https://www.jonkoping.se/evenemangskalender/evenemangskalender?filters=%7B%7D&page=1000&pageMode=all&query=&sv.12.27b6a9cc17cdfe279de33aae.route=%2Fsearch&sv.target=12.27b6a9cc17cdfe279de33aae&timestamp=1743355834489"
  lan_header = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
      "Accept": "application/json"
  }
  try:
    time_now = datetime.datetime.now()
    resp = requests.get(lan_url,headers=lan_header)
    if resp.status_code == 200:
      soup = BeautifulSoup(resp.text,features="html.parser")
      json_data = soup.find(id="Evenemangslistning").next_sibling
      json_dict = json.loads(json_data)

      events_list = json_dict["searchHits"]
      events_total = json_dict["searchInfo"]["totalHits"]

      return events_total,events_list
    else:
      return -1,f"The website is down. Please try again later: {resp.status_code}"
  except Exception as e:
    return -1,f"Problems with scraping the website. Please check the following error message : {e}"


# Scrape event data from Destination Jönköping event website
def get_events_tour():
  tour_url = "https://www.jonkoping.se/rest-api/Evenemangsdata/search?categories_appfilters=&numHits=999"
  tour_header = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
      "Accept": "application/json"
  }
  try:
    time_now = datetime.datetime.now()
    resp = requests.get(tour_url,headers=tour_header)
    if resp.status_code == 200:
      json_dict = json.loads(resp.text)

      events_list = json_dict["searchHits"]
      events_total = json_dict["searchInfo"]["totalHits"]

      return events_total,events_list
    else:
      return -1,f"The website is down. Please try again later: {resp.status_code}"
  except Exception as e:
    return -1,f"Problems with scraping the website. Please check the following error message : {e}"
  
# Consilidate event data by removing duplicates
def get_events_jkpg():
  time_now = datetime.datetime.now()
  lan_events_total,lan_events_list  = get_events_lan()
  tour_events_total,tour_events_list = get_events_tour()
  if lan_events_total!=-1 or tour_events_total!=-1:
    if any(ev in tour_events_list for ev in lan_events_list):
      events_list = tour_events_list
      for ev in lan_events_list:
        if ev not in tour_events_list:
          events_list.append(ev)
    else :
      events_list = lan_events_list + tour_events_list
    
    events_list_filepath = RAW_PATH + "/events_raw_" + time_now.strftime('%d_%m_%Y_%H%M') + ".json"
    with open(events_list_filepath, "w", encoding="utf-8") as f:
      json.dump(events_list, f, ensure_ascii=False, indent=4)

    with open(events_list_filepath, "r", encoding="utf-8") as f:
      ev = json.load(f)
      if len(events_list)==len(ev):
        return(time_now.strftime('%d %b %Y, %H:%M')," : Event data (" + str(len(ev)) + " events) from Jönköping websites have been successfully scraped and saved")
      else:
        return("Problems with scraping the website. Please try again later")
  else :
     return("Problems with scraping the website. Please try again later")


