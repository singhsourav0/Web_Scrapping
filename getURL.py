from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

try:
    
    driver.get("https://pythonexamples.org/python-selenium-get-current-url/")

     
    # Find the element containing the specified text
    element = driver.find_element(By.LINK_TEXT , "Sitemap")

    #get url 
    print("URL of the element:", element.get_attribute("href"))
    driver.implicitly_wait(1)
    
    #url of present page
    print(driver.current_url)

finally:
    
    driver.quit()
