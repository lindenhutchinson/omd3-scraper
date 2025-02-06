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
            # Send GET request to the page
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
            
            # Parse the page content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get the trap name
            title = soup.find('span', {'class': 'mw-page-title-main'})
            if title:
                self.trap_data['name'] = title.get_text(strip=True)
            else:
                print("Trap name not found.")
                self.trap_data['name'] = 'N/A'
            
            description = soup.select(".portable-infobox + p + p", limit=1)
            if description:
                self.trap_data["description"] = description.get_text()
            else:
                print("Description not found")
                self.trap_data["description"] = "N/A"
                
            # Find the relevant attributes (trigger range, cooldown, etc.)
            attributes = soup.find_all('div', {'class': 'pi-item pi-data pi-item-spacing pi-border-color'})
            for attribute in attributes:
                label = attribute.find('h3', {'class': 'pi-data-label'})
                value = attribute.find('div', {'class': 'pi-data-value'})
                if label and value:
                    label_text = label.get_text(strip=True).lower().replace(' ', '_')
                    value_text = value.get_text(strip=True)
                    self.trap_data[label_text] = value_text

            # Get upgrades (Level Upgrades and Unique Upgrades)
            level_upgrades = []
            unique_upgrades = []
            upgrades_table = soup.find('table', {'class': 'article-table'})
            if not upgrades_table:
                upgrades_table = soup.find('table', {'class': 'fandom-table'})

            if upgrades_table:
                rows = upgrades_table.find_all('tr')[1:]  # Skip header row
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        level_upgrade = cells[0].get_text(strip=True)
                        unique_upgrade = cells[1].get_text(strip=True)
                        level_upgrades.append(level_upgrade)
                        unique_upgrades.append(unique_upgrade)
                self.trap_data['level_upgrades'] = level_upgrades
                self.trap_data['unique_upgrades'] = unique_upgrades
            else:
                print(f"No upgrades table found. - {self.trap_data['name']}")
                self.trap_data['level_upgrades'] = []
                self.trap_data['unique_upgrades'] = []

            print(f"Scraping successful. - {self.trap_data['name']}")
        except requests.RequestException as e:
            print(f"An error occurred while fetching the URL: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_trap_data(self):
        return self.trap_data

    def save_to_json(self, filename):
        """Utility function to save trap details to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.trap_data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving to JSON: {e}")



    def save_to_csv(self, filename):
        """Utility function to save trap details to a CSV file, appending if the file exists."""
        try:
            # Prepare trap data for CSV, serializing lists into a string
            data_for_csv = self.trap_data.copy()
            
            # Convert lists (like level_upgrades and unique_upgrades) into a single string
            for key in ['level_upgrades', 'unique_upgrades']:
                if key in data_for_csv and isinstance(data_for_csv[key], list):
                    data_for_csv[key] = "; ".join(data_for_csv[key])  # Join list items with a semicolon separator

            # Check if the file exists
            file_exists = os.path.isfile(filename)
            
            # Open file in append mode, write header only if the file doesn't exist
            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data_for_csv.keys())
                
                if not file_exists:  # Write header if the file doesn't exist
                    writer.writeheader()
                    
                writer.writerow(data_for_csv)
            
            print(f"Data successfully saved to {filename}.")
        except Exception as e:
            print(f"Error saving to CSV: {e}")



# Example usage:
if __name__ == "__main__":
    url = "https://orcsmustdie.fandom.com/wiki/Acid_Geyser_(OMD3)"  # Replace with actual URL
    scraper = OMDDetailsScraper(url)
    scraper.scrape()
    
    trap_info = scraper.get_trap_data()
    scraper.save_to_csv("acid-geyser.csv")
    print(trap_info)
