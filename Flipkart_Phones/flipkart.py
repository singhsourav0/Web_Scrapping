
# # Setting up Selenium WebDriver
# driver = webdriver.Chrome()
# url = 'https://www.flipkart.com/search?q=mobile+phones'
# driver.get(url)

# products = []
# # Function to extract product details
# def extract_product_details():
#  items = driver.find_elements(By.CLASS_NAME, '_75nlfW')

#  for item in items:
#     try:

#         # print("yes!!") tUxRFH
#         # 'hl05eU'

#         product_name = item.find_element(By.CLASS_NAME, 'KzDlHZ').text
#         price_current = item.find_element(By.CSS_SELECTOR, 'div.Nx9bqj._4b5DiR').text.strip().replace('₹', '').replace(',', '')
#         price_original = item.find_element(By.CSS_SELECTOR, 'div.yRaY8j.ZYYwLA').text.strip().replace('₹', '').replace(',', '')
#         rating = item.find_element(By.CLASS_NAME, 'XQDdHH').text
#         products.append({
#             'product_name': product_name,
#             'price_current': price_current,
#             'price_original': price_original,
#             'rating': rating,
#         })

#         # print("No!")Nx9bqj _4b5DiR
#         # print(price)KzDlHZ
#         # rating = item.find_element(By.CLASS_NAME, 'XQDdHH').text
#         # print("no!!")
#         # print(rating)
#         # products.append({
#         #     'product_name': product_name,
#         #     'price': price,
#         #     'rating': rating
#         # })
#     except:
#         print("nhi hua")
#         continue
# def go_to_next_page():
#     try:
#         next_button = driver.find_element(By.CSS_SELECTOR, 'a._9QVEpD')
#         next_button.click()
#         time.sleep(4)  # Wait for the next page to load
#         return True
#     except Exception as e:
#         print(f"Error clicking next button or no more pages: {e}")
#         return False

# # Closing the driver
# driver.quit()

# # Convert the list of dictionaries to a DataFrame
# df = pd.DataFrame(products)

# # Define the file name
# file_name = 'flipkart_dframe3.csv'

# # Save the DataFrame to a CSV file
# df.to_csv(file_name, index=False)

# print(f"Prices saved to {file_name}")

# # Define the file name
# file_name = 'products.csv'

# # Save the products list to a CSV file
# with open(file_name, 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=['product_name'])
#     writer.writeheader()
#     writer.writerows(products)

# print(f"Products saved to {file_name}")
'''
Extracting product details

items = driver.find_elements(By.CLASS_NAME, 'cPHDOP.col-12-12')
Add to Compare
Motorola G34 5G (Ice Blue, 128 GB)
4.296,879 Ratings & 6,823 Reviews
8 GB RAM | 128 GB ROM
16.51 cm (6.5 inch) HD+ Display
50MP + 2MP | 16MP Front Camera
5000 mAh Battery
Snapdragon 695 5G Processor
1 Year on Handset and 6 Months on Accessories
₹11,999
₹14,99920% off
Free delivery
Save extra with combo offers
Upto
₹8,600
 Off on Exchange
Bestseller
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Setting up Selenium WebDriver
driver = webdriver.Chrome()

# Function to extract product details
def extract_product_details():
    products = []
    items = driver.find_elements(By.CLASS_NAME, '_75nlfW')
    for item in items:
        try:
            #name
            index = item.find_element(By.CLASS_NAME, 'KzDlHZ').text
            # i = min(index.find(','), index.find('('))
            product_name = index[:min(index.find('|'), index.find(')'))]
            #price
            price_current = item.find_element(By.CSS_SELECTOR, 'div.Nx9bqj._4b5DiR').text.strip().replace('₹', '').replace(',', '')
            price_original_elements = item.find_elements(By.CSS_SELECTOR, 'div.yRaY8j.ZYYwLA')
            price_original = price_original_elements[0].text.strip().replace('₹', '').replace(',', '') if price_original_elements else None
            #rating
            rating = item.find_element(By.CLASS_NAME, 'XQDdHH').text

            ul_element = item.find_element(By.CLASS_NAME, 'G4BRas')
            # Extract all 'li' elements within the 'ul' element
            li = ul_element.find_elements(By.TAG_NAME, 'li')

            ram = li[0].text
            part1 = ram.split('|')
            # Strip any leading/trailing whitespace from the parts
            Ram = part1[0].strip()
            Rom = part1[1].strip()   if len(part1) > 1 else ""

            Display=li[1].text
            Display_size = Display[:Display.find('(')]

            li_text = li[2].text

            # Safely split and unpack the text
            parts = li_text.split('|')
            Real_camera = parts[0].strip()
            selfie = parts[1].strip() if len(parts) > 1 else ""


            battery= li[3].text
            processor = li[4].text
            #adding in list
            products.append({
                'product_name': product_name,
                'price_current': price_current,
                'price_original': price_original,
                'rating': rating,
                'ram': Ram,
                'Rom': Rom,
                'Display_size': Display_size,
                'Camera': Real_camera,
                'selfie':selfie,
                'battery':battery,
                'processor':processor
            })
        except Exception as e:
            print(f"Error extracting product details: {e}")
            continue
    return products

def go_to_next_page():
    try:
        # Find all buttons with the same CSS selector
        buttons = driver.find_elements(By.CLASS_NAME, '_9QVEpD')
        
        # Iterate through buttons to find the "Next" button
        next_button = None
        for button in buttons:
            if button.text.strip().lower() == 'next':
                next_button = button
                break
        
        # If "Next" button found, click it
        if next_button:
            next_button.click()
            time.sleep(4)  # Wait for the next page to load
            return True
        else:
            print("Next button not found or could not be clicked.")
            return False
    
    except Exception as e:
        print(f"Error clicking next button: {e}")
        return False


all_products = []

# Initial URL
url = 'https://www.flipkart.com/search?q=mobile+phones'
driver.get(url)
time.sleep(4)  # Wait for the initial page to load

# Loop to scrape multiple pages
for page_number in range(40):  
    print(f"Scraping page {page_number + 1}")
    products = extract_product_details()
    all_products.extend(products)
    if page_number < 3:  
        go_to_next_page()

# Closing the driver
driver.quit()

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_products)

# Define the file name
file_name = 'flipkart_dframe40.csv'

# Save the DataFrame to a CSV file
df.to_csv(file_name, index=False)

print(f"Product details saved to {file_name}")
