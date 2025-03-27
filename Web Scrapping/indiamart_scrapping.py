from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Chrome options for headless scraping
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--log-level=3")

# Launch Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Get product input from user
product = input("Enter the product to search: ").replace(" ", "+").lower()
url = f"https://dir.indiamart.com/search.mp?ss={product}&src=as-popular"

# Open the page
driver.get(url)
time.sleep(5)

# Scroll to load all results
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract data from the fully loaded page
company_data = []
product_cards = driver.find_elements(By.CSS_SELECTOR, "div.cardbody")

for card in product_cards:
    try:
        company_name = card.find_element(By.CSS_SELECTOR, "div.companyname a").text.strip()
    except:
        company_name = "N/A"
    
    try:
        location = card.find_element(By.CSS_SELECTOR, "div.newLocationUi span.elps").text.strip()
    except:
        location = "N/A"
    
    try:
        rating = card.find_element(By.CSS_SELECTOR, "div[id^='sellerrating_'] span.bo.color").text.strip()
    except:
        rating = "No Rating"
    
    try:
        reviews = card.find_element(By.CSS_SELECTOR, "div[id^='sellerrating_'] span.color").text.strip().replace("(", "").replace(")", "")
    except:
        reviews = "0"

    company_data.append({
        "Company Name": company_name,
        "Location": location,
        "Rating": rating,
        "Reviews": reviews
    })

# Close the browser
driver.quit()

# Save to Excel
if company_data:
    df = pd.DataFrame(company_data)
    output_file = f"{product}_suppliers.xlsx"
    df.to_excel(output_file, index=False)
    print(f"✅ Data saved to {output_file}")
else:
    print("❌ No data found. Try a different product or check the page structure.")
