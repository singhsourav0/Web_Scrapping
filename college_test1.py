#This repo is written by SOURAV KUMAR(singhsourav0).
#This repo is the for enter the text on any search or text box.
#In  this repo our target is to find email and phone number of our batchment from registation number.
#this repo will run in google_colab not in local system

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument('--no-sandbox')  # Required in Colab

driver = webdriver.Chrome(options=chrome_options)


driver.get("http://akuexams.in/akuexam/StudentServices/frmStudentForgotPassword.aspx")

driver.find_element(By.NAME, "txtuserid").send_keys("22105128036")
# driver.find_element(BY.NAME , "pass").send_keys("xxxxxx")
driver.find_element(By.ID , "btnGo").click()

act_title = driver.title
 
exp_title ="Change Password"
 
if act_title == exp_title:
     print("login test passed")
else:
     print("test not passed")
     
driver.save_screenshot("Image.png")

#*********************for get screenshot of range of data...********************************

for i in range(20105128000, 20105128056  + 1):
    driver.find_element(By.NAME, "txtuserid").clear()
    driver.find_element(By.NAME, "txtuserid").send_keys(str(i))
    driver.find_element(By.ID, "btnGo").click()

    # Check if the login page is displayed
    if driver.title == "Change Password":
        print(f"Login successful for user ID {i}")
        driver.save_screenshot(f"Image{i}.png")
    else:
        print(f"Login failed for user ID {i}")

driver.close()
