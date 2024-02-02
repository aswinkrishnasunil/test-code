import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

options = Options()

options.add_experimental_option("detach",True)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

driver.get("https://globalenergymonitor.org")

# Find the link with the text "Download Data" using XPath
download_link = driver.find_element(By.XPATH, '//a[contains(@href, "?download-data")]')
# Click on the "Download Data" link
download_link.click()
# Find the links with the specified text and print their href values
plant_types = ["Coal Plants", "Oil and Gas Plants", "Solar Farms", "Hydropower", "Geothermal Plants", "Wind Farms", "Bioenergy Plants"]
#"Nuclear Plants"
#Steel_Plants = driver.find_element(By.XPATH, '//a[text()="Steel Plants"]')
plant_links = []
links_list = []
plant_type_to_sheet_id_list = []

# Loop through the plant types and find their respective links
for plant_type in plant_types:
    plant_link = driver.find_element(By.XPATH, f'//a[text()="{plant_type}"]')
    plant_links.append(plant_link.get_attribute("href"))

# Print the list of links
#print("Plant Links:", plant_links)

# Loop through each plant link and click on "Summary Tables"
for link in plant_links:
    driver.get(link)
    #time.sleep(3)  # Add a delay to allow the page to load (you can adjust the time based on your needs)
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Summary Tables"]')))
    # Find the "Summary Tables" link
    summary_tables_link = driver.find_element(By.XPATH, '//aside[@class="sidebar"]//a[text()="Summary Tables"]')

    # Click on the "Summary Tables" link
    summary_tables_link.click()

    # Extract links inside "Summary Tables" using the name
    names = ["Newly Operating Coal Plants by Year, 2000-2023 (MW)",
             "Newly Operating Oil and Gas Plants by Year 2000-H1 2023 (MW)",
             "New Solar Capacity Added by Country and Year",
             "New Wind Power Capacity Added by Country and Year",
             "Hydropower Capacity Added by Year and Country (MW)",
             "New Geothermal Capacity Added by Country and Year",
             "Bioenergy Capacity (MW) by Country and Year"]

    for name in names:
        try:
            # Search for each name within the "Summary Tables" section
            link = driver.find_element(By.XPATH, f'//a[contains(text(), "{name}")]')
            link_url = link.get_attribute('href')
            links_list.append((name, link_url))
            match = re.search(r'/d/([a-zA-Z0-9-_]+)', link_url)


            if match:
                sheet_id = match.group(1)
                # Append the tuple to the list
                plant_type_to_sheet_id_list.append((plant_type, sheet_id))
                print(f"{plant_type}: Sheet ID - {sheet_id}")
            else:
                print("Sheet ID not found in the URL.")
            #plant_links.append(plant_link.get_attribute("href"))
            #print(f"{name}: {link_url}")
        except Exception as e:
            #print(f"Link not found for {name}")
            print("-")

    #except Exception as e:
     #print(f"Error: {str(e)}")

    # Navigate back to the main page for the next iteration
    driver.back()


# Close the browser
driver.quit()
print(links_list)
print(plant_type_to_sheet_id_list)

import pandas as pd

sheet_id = '1j35F0WrRJ9dbIJhtRkm8fvPw0Vsf-JV6G95u7gT-DDw'

gid = '647531100'
# List of plant_types
plant_types = ["Coal Plants", "Oil and Gas Plants", "Solar Farms", "Hydropower", "Geothermal Plants", "Wind Farms",
               "Bioenergy Plants"]

# Initialize an empty dictionary to store DataFrames
plant_type_to_dataframe = {}

# Construct csv_url for each plant_type and read into DataFrame
for plant_type in plant_types:
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    try:
        # Read the CSV data into a Pandas DataFrame
        df = pd.read_csv(csv_url)

        # Store the DataFrame in the dictionary
        plant_type_to_dataframe[plant_type] = df

        print(f"{plant_type}: DataFrame loaded successfully.")
    except Exception as e:
        print(f"Error loading DataFrame for {plant_type}: {str(e)}")

# Access the DataFrames using plant_type_to_dataframe dictionary
for plant_type, df in plant_type_to_dataframe.items():
    print(f"{plant_type} DataFrame:")
    print(df)
