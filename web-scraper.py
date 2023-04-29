from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re

website = 'https://www.zoya.com/content/category/Zoya_Nail_Polish.html'
#path = r'C:\Users\Francisco\Downloads\chromedriver.exe'

ser = Service(r"C:\Users\Francisco\Downloads\chromedriver.exe")
op = Options()
# Keep Chrome open after script runs
op.add_experimental_option("detach", True)
# Disable DevTools listening message (https://bugs.chromium.org/p/chromedriver/issues/detail?id=2907#c3)
op.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=ser, options=op)
driver.get(website)

products = driver.find_elements(By.CLASS_NAME, 'category-list-title')


#for product in products:
#    name = product.find_element(By.CLASS_NAME, 'category-list-name')
#    print(name.text)

nail_polishes = []

for product in products:
    code = product.find_element(By.CLASS_NAME, 'category-list-partnumber').text
    if not re.match(r'ZP\d+', code):
        continue
    else:
        name = product.find_element(By.CLASS_NAME, 'category-list-name').text
        polish = dict()
        polish['code'] = code
        polish['name'] = name
        nail_polishes.append(polish)
        
print(nail_polishes)