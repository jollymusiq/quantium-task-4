import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Point to chromedriver
service = Service("C:\\Users\\HP\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open Google
driver.get("http://www.google.com/")

# Find search box and search for "ChromeDriver"
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("ChromeDriver")
search_box.submit()

 # See the results

