from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import os
import wget
import time
from dotenv import load_dotenv

website = 'https://www.zoya.com/content/category/Zoya_Nail_Polish.html'

load_dotenv()
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

ser = Service()
op = Options()
# Keep Chrome open after script runs
op.add_experimental_option("detach", True)
# Disable DevTools listening message (https://bugs.chromium.org/p/chromedriver/issues/detail?id=2907#c3)
op.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=ser, options=op)
driver.get(website)

time.sleep(10)

# CSS selector (https://stackoverflow.com/questions/58422998/selenium-python-find-elements-by-class-name-returns-nothing)
products = driver.find_elements(By.CLASS_NAME, 'itemContainer.item')

nail_polishes = []

for product in products:
    code = product.find_element(By.CLASS_NAME, 'category-list-partnumber').text
    if not re.match(r'ZP\d+', code):
        continue
    else:
        name = product.find_element(By.CLASS_NAME, 'category-list-name').text
        link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
        image = product.find_element(By.TAG_NAME, 'img').get_attribute('src')
        polish = dict()
        polish['code'] = code
        polish['name'] = name
        polish['link'] = link
        polish['image'] = image
        nail_polishes.append(polish)

# Create images folder
path = os.getcwd()
path = os.path.join(path, 'images')
try:
    os.mkdir(path)
except FileExistsError:
    pass

#Download images
for polish in nail_polishes:
    save_as = os.path.join(path, polish['name'] + '.jpg')
    wget.download(polish['image'], save_as)

print(nail_polishes)