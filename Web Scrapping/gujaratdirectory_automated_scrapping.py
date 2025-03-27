import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

product = input("Enter the product to search: ").replace(" ", "-").lower()
url = f"https://www.gujaratdirectory.com/product/{product}.html"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

suppliers = []

listings = soup.select('div.result_container--right-title a')

if not listings:
    print("No data found for this product.")
    exit()

for listing in listings:
    name = listing.get_text(strip=True)
    raw_location = listing.get('title', '')

    contact_person_match = re.search(r"Contact person - ([^,]+)", raw_location)
    contact_person = contact_person_match.group(1).strip() if contact_person_match else "N/A"

    phone_match = re.search(r"Tel no - (\d+)", raw_location)
    phone_number = phone_match.group(1) if phone_match else "N/A"

    pincode_match = re.search(r"(\d{6})", raw_location)
    pincode = pincode_match.group(1) if pincode_match else "N/A"

    city_state_match = re.search(r"([\w\s]+)-\d{6}", raw_location)
    if city_state_match:
        city_state = city_state_match.group(1).strip().split(',')
        city = city_state[-1].strip()
        state = city_state[-2].strip() if len(city_state) > 1 else "N/A"
    else:
        city, state = "N/A", "N/A"

    address_match = re.search(r"Address - (.*?)(?:,\s*\w+ - \d{6}|, Tel no -|$)", raw_location)
    address = address_match.group(1).strip() if address_match else "N/A"

    suppliers.append({
        "Name": name,
        "Contact Person": contact_person,
        "Address": address,
        "City": city,
        "State": state,
        "Pincode": pincode,
        "Phone Number": phone_number
    })

df = pd.DataFrame(suppliers)
output_file = f'{product}_suppliers_data.xlsx'
df.to_excel(output_file, index=False)

print(f"Data successfully saved to {output_file}")