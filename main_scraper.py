from omd_url_scraper import OMDUrlScraper
from omd_details_scraper import OMDDetailsScraper
import json
import os

BASE_URL = "https://orcsmustdie.fandom.com"
URL_DIR = "./item_urls"
URL_FILES = {
    "weapons": f"{URL_DIR}/weapon_list.json",
    "trinkets": f"{URL_DIR}/trinket_list.json",
    "traps": f"{URL_DIR}/trap_list.json"
}
DETAILS_DIR = "./details"
DETAILS_FILES = {
    "weapons": f"{DETAILS_DIR}/weapon_details.json",
    "trinkets": f"{DETAILS_DIR}/trinket_details.json",
    "traps": f"{DETAILS_DIR}/trap_details.json"
}
CATEGORY_URLS = {
    "weapons": "https://orcsmustdie.fandom.com/wiki/Category:Weapons_(OMD3)",
    "trinkets": "https://orcsmustdie.fandom.com/wiki/Category:Trinkets_(OMD3)",
    "traps": "https://orcsmustdie.fandom.com/wiki/Category:Traps_(OMD3)"
}

def ensure_directories():
    os.makedirs(URL_DIR, exist_ok=True)
    os.makedirs(DETAILS_DIR, exist_ok=True)

def ensure_url_file(category):
    url_file = URL_FILES[category]
    if not os.path.exists(url_file):
        scraper = OMDUrlScraper(CATEGORY_URLS[category], url_file)
        scraper.scrape()

def scrape_details(category):
    url_file = URL_FILES[category]
    details_file = DETAILS_FILES[category]
    
    if not os.path.exists(url_file):
        print(f"Warning: URL file {url_file} not found. Skipping {category}.")
        return
    
    with open(url_file, "r") as fn:
        trap_urls = json.load(fn)
    
    all_trap_urls = trap_urls.get("all_scenarios", [])
    
    all_data = []
    if os.path.exists(details_file):
        with open(details_file, "r") as fn:
            all_data = json.load(fn)
    
    for url in all_trap_urls:
        full_url = f"{BASE_URL}{url}"
        scraper = OMDDetailsScraper(full_url)
        scraper.scrape()
        data = scraper.get_trap_data()
        all_data.append(data)
    
    with open(details_file, "w") as fn:
        json.dump(all_data, fn, indent=4)

if __name__ == "__main__":
    ensure_directories()
    for category in CATEGORY_URLS.keys():
        ensure_url_file(category)
        scrape_details(category)
