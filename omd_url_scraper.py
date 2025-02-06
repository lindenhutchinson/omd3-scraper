import requests
from bs4 import BeautifulSoup
import json

class OMDUrlScraper:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.all_scenarios = []
        self.war_scenarios = []
    
    def scrape(self):
        try:
            # Send GET request to the page
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
            
            # Parse the page content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the first .fandom-table element
            table = soup.find('table', class_='fandom-table')
            if not table:
                print("No table found on the page.")
                return

            # Iterate over each td in the table
            for td in table.find_all('td'):
                a_tag = td.find('a', href=True)
                if a_tag:
                    url = a_tag['href']
                    # Check for background color
                    bg_color = td.get('style', '')
                    if 'background-color: #bf8c68;' in bg_color:
                        # Add to war_scenarios list if the background color matches
                        self.war_scenarios.append(url)
                    else:
                        # Otherwise, add to all_scenarios
                        self.all_scenarios.append(url)
            
            # Export both lists to a JSON file
            self.save_to_json()
            
            print(f"Scraping completed. Data saved to {self.filename}.")
        
        except requests.RequestException as e:
            print(f"An error occurred while fetching the URL: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def save_to_json(self):
        try:
            # Prepare the data to be saved
            data = {
                'all_scenarios': self.all_scenarios,
                'war_scenarios': self.war_scenarios
            }
            # Write the data to the file
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def get_scenarios(self):
        return self.all_scenarios, self.war_scenarios


if __name__ == "__main__":
    # url = "https://orcsmustdie.fandom.com/wiki/Category:Traps_(OMD3)"
    # url = "https://orcsmustdie.fandom.com/wiki/Category:Trinkets_(OMD3)"
    url = "https://orcsmustdie.fandom.com/wiki/Category:Weapons_(OMD3)"
    filename = "weapon_list.json"
    
    scraper = OMDUrlScraper(url, filename)
    scraper.scrape()
