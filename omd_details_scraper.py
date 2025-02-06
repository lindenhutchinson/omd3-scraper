import requests
from bs4 import BeautifulSoup
import json
import csv
import os


class OMDDetailsScraper:
    def __init__(self, url):
        self.url = url
        self.trap_data = {}

    def scrape(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('span', {'class': 'mw-page-title-main'})
            self.trap_data['name'] = title.get_text(strip=True) if title else 'N/A'

            description = soup.select_one(".portable-infobox ~ p ~ p")
            self.trap_data["description"] = description.get_text(strip=True) if description else "N/A"

            attributes = soup.find_all('div', {'class': 'pi-item pi-data pi-item-spacing pi-border-color'})
            for attribute in attributes:
                label = attribute.find('h3', {'class': 'pi-data-label'})
                value = attribute.find('div', {'class': 'pi-data-value'})
                if label and value:
                    label_text = label.get_text(strip=True).lower().replace(' ', '_')
                    value_text = value.get_text(strip=True)
                    self.trap_data[label_text] = value_text

            level_upgrades, unique_upgrades = [], []
            upgrades_table = soup.find('table', {'class': 'article-table'}) or soup.find('table', {'class': 'fandom-table'})
            
            if upgrades_table:
                rows = upgrades_table.find_all('tr')[1:]
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        level_upgrades.append(cells[0].get_text(strip=True))
                        unique_upgrades.append(cells[1].get_text(strip=True))
                
            self.trap_data['level_upgrades'] = level_upgrades or []
            self.trap_data['unique_upgrades'] = unique_upgrades or []

            print(f"Scraping successful. - {self.trap_data['name']}")
        except requests.RequestException as e:
            print(f"An error occurred while fetching the URL: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_trap_data(self):
        return self.trap_data

    def save_to_json(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.trap_data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving to JSON: {e}")

    def save_to_csv(self, filename):
        try:
            data_for_csv = self.trap_data.copy()
            for key in ['level_upgrades', 'unique_upgrades']:
                if key in data_for_csv and isinstance(data_for_csv[key], list):
                    data_for_csv[key] = "; ".join(data_for_csv[key])
            
            file_exists = os.path.isfile(filename)
            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data_for_csv.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data_for_csv)
            print(f"Data successfully saved to {filename}.")
        except Exception as e:
            print(f"Error saving to CSV: {e}")


if __name__ == "__main__":
    url = "https://orcsmustdie.fandom.com/wiki/Acid_Geyser_(OMD3)"
    scraper = OMDDetailsScraper(url)
    scraper.scrape()
    scraper.save_to_csv("acid-geyser.csv")
    print(scraper.get_trap_data())
