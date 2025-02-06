from detail_scraper import DetailScraper
import json
import os

BASE_URL = "https://orcsmustdie.fandom.com"

URL_LIST_FILE = "./item_urls/weapon_list.json"
DETAILS_FILE = "weapon_details.json"

if __name__ == "__main__":
    with open(URL_LIST_FILE, "r") as fn:
        trap_urls = json.load(fn)

    all_trap_urls = trap_urls["all_scenarios"]

    for url in all_trap_urls:
        full_url = f"{BASE_URL}{url}"
        scraper = DetailScraper(full_url)
        scraper.scrape()
        data = scraper.get_trap_data()

        if os.path.exists(DETAILS_FILE):
            with open(DETAILS_FILE, "r") as fn:
                existing_data = json.load(fn)
            
            existing_data.append(data)
            with open(DETAILS_FILE, "w") as fn:
                json.dump(existing_data, fn)
        else:
            with open(DETAILS_FILE, "w") as fn:
                json.dump([data], fn)
