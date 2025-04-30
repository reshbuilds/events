
import requests
from bs4 import BeautifulSoup
import json
import datetime

from src.paths import *

# Scrape event data from Jönköping municipality website
def get_events_gov():
  lan_url = "https://www.jonkoping.se/evenemangskalender/evenemangskalender?filters=%7B%7D&page=1000&pageMode=all&query=&sv.12.27b6a9cc17cdfe279de33aae.route=%2Fsearch&sv.target=12.27b6a9cc17cdfe279de33aae&timestamp=1743355834489"
  lan_header = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Referer": "https://www.jonkoping.se/",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.5",
  }

  try:
    time_now = datetime.datetime.now()
    lan_resp = requests.get(lan_url,headers=lan_header)
    if lan_resp.status_code == 200:
      lan_soup = BeautifulSoup(lan_resp.text,features="html.parser")
      lan_json_data = lan_soup.find(id="Evenemangslistning").next_sibling
      lan_json_dict = json.loads(lan_json_data)

      events_lan_list = lan_json_dict["searchHits"]
      events_lan_total = lan_json_dict["searchInfo"]["totalHits"]

      events_lan_list_filepath = RAW_PATH + "events_lan_list_" + time_now.strftime('%d_%m_%Y_%H%M') + ".json"
      with open(events_lan_list_filepath, "w", encoding="utf-8") as f:
        json.dump(events_lan_list, f, ensure_ascii=False, indent=4)
      
      with open(events_lan_list_filepath, "r", encoding="utf-8") as f:
          lan_ev = json.load(f)
          if events_lan_total==len(lan_ev):
            return(time_now.strftime('%d %b %Y, %H:%M')," : Event data (" + str(len(lan_ev)) + " events) from Jönköping Evenemangskalender has been successfully scraped and saved")
    else:
      return("The website is down. Please try again later : ",lan_resp.status_code)
  except Exception as e:
    return("Problems with scraping the website. Please check the following error message :", e)
  

# Scrape event data from Destination Jönköping's JKPG website
def get_events_private():
  try:
    dj_url = "https://jkpg.com/sv/step/api/v1/public-experience-list/?strict=0&skip=10000&take=18"
    dj_resp = requests.get(dj_url)
    if dj_resp.status_code == 200:
      dj_soup = BeautifulSoup(dj_resp.text,features="html.parser")
      events_dj_total = json.loads(dj_soup.text)["total_experiences"]
      
      time_now = datetime.datetime.now()
      events_dj_list = []
      for skip_val in range(0,events_dj_total+1,18):
        dj_url_t = "https://jkpg.com/sv/step/api/v1/public-experience-list/?strict=0&skip=" + str(skip_val) + "&take=18"
        dj_resp_t = requests.get(dj_url_t)
        if dj_resp_t.status_code == 200:
          dj_soup_t = BeautifulSoup(dj_resp_t.text,features="html.parser")
          el = json.loads(dj_soup_t.text)["experiences"]
          events_dj_list += el
        else:
          return("The website is down. Please try again later : ",dj_resp_t.status_code)
          #break
        
      events_dj_list_filepath = RAW_PATH + "events_dj_list_" + time_now.strftime('%d_%m_%Y_%H%M') + ".json"
      with open(events_dj_list_filepath, "w", encoding="utf-8") as f:
        json.dump(events_dj_list, f, ensure_ascii=False, indent=4)
      
      with open(events_dj_list_filepath, "r", encoding="utf-8") as f:
          dj_ev = json.load(f)
          if events_dj_total==len(dj_ev):
            return(time_now.strftime('%d %b %Y, %H:%M')," : Event data (" + str(len(dj_ev)) + " events) from Destination Jönköping has been successfully scraped and saved")
    else:
      return("The website is down. Please try again later : ",dj_resp.status_code)
  except Exception as e:
    return("Invalid website. Please check the following error message :", e)

