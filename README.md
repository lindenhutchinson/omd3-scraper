# Web Scraper Application

A Python-based web scraping application designed to extract data from the *Orcs Must Die! 3* (OMD3) wiki.

## Features

- **URL Scraper**: Extracts scenario URLs from category pages.
- **Details Scraper**: Scrapes detailed information from individual scenario pages.
- **Automated File Handling**: Checks for existing data before scraping to avoid redundant requests.
- **Flexible Data Storage**: Saves extracted data in JSON and CSV formats.
- **Configurable Scraping Parameters**: Easily modify target categories and output formats.

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-repo/web-scraper.git
   cd web-scraper
   ```

2. Install required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Running the Main Scraper

This script first checks if URL files exist; if not, it scrapes them. It then extracts details from each scenario.

```sh
python main_scraper.py
```

### Output Files

- `item_urls/weapon_list.json` - URLs for weapons
- `item_urls/trinket_list.json` - URLs for trinkets
- `item_urls/trap_list.json` - URLs for traps
- `data/weapon_details.json` - Detailed weapon data
- `data/trinket_details.json` - Detailed trinket data
- `data/trap_details.json` - Detailed trap data

## Configuration

Modify `main_scraper.py` to adjust:

- **Target categories** (weapons, trinkets, traps)
- **Output directories**
- **Logging verbosity**
