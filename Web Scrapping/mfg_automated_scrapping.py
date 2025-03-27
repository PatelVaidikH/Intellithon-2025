import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define parameters
continents = [
    ("United+States", "united-states"),
    ("Europe", "europe"),
    ("Asia", "asia"),
    ("Canada", "canada"),
    ("Mexico+%2F+South+America", "mexico-south-america"),
]

capabilities = [
    ("Extrusions", "extrusions"),
    ("Fabrication", "fabrication"),
    ("Investment+Casting", "investment-casting"),
    ("Machining", "machining"),
    ("Thermoforming", "thermoforming"),
    ("Tube+Modification", "tube-modification"),
]

# Base URL format
base_url = "https://www.mfg.com/manufacturer-directory/page/{page}/?manufacturing_location={cont}&ep_filter_manufacturing_location={filter_cont}&capability={cap}&ep_filter_capability={filter_cap}&search="

all_manufacturers = []
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; CustomScraper/1.0; +http://example.com/)"
}

max_retries = 5
retry_delay = 20  # seconds

# Iterate over all continents
for cont, filter_cont in continents:
    print(f"Scraping continent: {cont}")
    
    for cap, filter_cap in capabilities:
        print(f"  Scraping capability: {cap}")
        page = 1
        
        while True:
            page_url = base_url.format(
                page=page, cont=cont, filter_cont=filter_cont, cap=cap, filter_cap=filter_cap
            )
            print(f"    Scraping page {page}: {page_url}")
            
            retries = 0
            while retries < max_retries:
                response = requests.get(page_url, headers=headers)
                if response.status_code == 200:
                    break
                elif response.status_code == 429:
                    retries += 1
                    print(f"    Page {page} returned 429. Retry {retries}/{max_retries} after {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"    Failed to fetch page {page}: Status code {response.status_code}")
                    break

            if response.status_code != 200:
                print(f"    Skipping page {page} due to errors.")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            containers = soup.select("div.bg-white.container.hover-glow.p-4.mb-3")

            if not containers:
                print(f"    No manufacturer containers found on page {page}. Stopping pagination.")
                break

            print(f"    Found {len(containers)} manufacturer containers on page {page}.")

            for container in containers:
                name_tag = container.select_one("h2.d-inline-block.mr-4.my-0 a")
                name = name_tag.get_text(strip=True) if name_tag else "N/A"
                details_url = name_tag['href'] if name_tag and name_tag.has_attr('href') else "N/A"
                if details_url.startswith("/"):
                    details_url = "https://www.mfg.com" + details_url

                location_tag = container.select_one("p[title='Location']")
                location = location_tag.get_text(strip=True) if location_tag else "N/A"

                rating_tag = container.select_one("strong.text-dark")
                rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

                desc_tag = container.select_one("div[id^='smry']")
                description = desc_tag.get_text(separator=" ", strip=True) if desc_tag else "N/A"

                capability_tags = container.select("div.d-contents.capabilities a.badge-pill.bg-secondary")
                capabilities_list = ", ".join([cap.get_text(strip=True) for cap in capability_tags]) if capability_tags else "N/A"

                post_tag_container = container.select_one("div.collapse.col-12.col-md-11.pl-0")
                post_tags = ", ".join([pt.get_text(strip=True) for pt in post_tag_container.select("a.badge-pill.bg-light")]) if post_tag_container else "N/A"

                manufacturer = {
                    "Name": name,
                    "Details URL": details_url,
                    "Location": location,
                    "Rating": rating,
                    "Description": description,
                    "Capabilities": capabilities_list,
                    "Post Tags": post_tags,
                    "Continent": cont,
                    "Capability": cap
                }

                all_manufacturers.append(manufacturer)
            
            page += 1
            time.sleep(1)

print(f"Total manufacturers scraped: {len(all_manufacturers)}")

df = pd.DataFrame(all_manufacturers)
df.to_csv("manufacturers_data.csv", index=False)
print("Data saved to manufacturers_data.csv")
