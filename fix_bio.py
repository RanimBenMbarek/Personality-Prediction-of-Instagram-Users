from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import json

def update_json(existing_data, new_data):
    for user, info in new_data.items():
        updated = False
        for item in existing_data:
            if item.get('user') == user:
                if item.get('bio') != info.get('bio'):
                    item['bio'] = info['bio']
                    updated = True
                    print(f"Bio of {user} is Updated Sucessfully")
                    break
        if not updated:
            existing_data.append({'user': user, 'bio': info['bio']})
            print(f"Bio of {user} is added as new user")
    return existing_data

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

service = Service("C:/Users/dossc/Desktop/Pfa/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.instagram.com/")

time.sleep(2)
username_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
username_input.send_keys(config['username'])
password_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
password_input.send_keys(config['password'])
password_input.send_keys(Keys.ENTER)

time.sleep(10)
instagram_profiles =[

   "connealymd",
]
data = {}
for user in instagram_profiles:
    driver.get(f"https://www.instagram.com/{user}/")
    time.sleep(3)
    try:
        bio = driver.find_element(By.XPATH, '//*[contains(@class, "_ap3a") and contains(@class, "_aaco") and contains(@class, "_aacu") and contains(@class, "_aacx") and contains(@class, "_aad6") and contains(@class, "_aade")]').text
    except NoSuchElementException:
        bio = ""
    try:
        inner_bio = driver.find_element(By.XPATH, '//div[contains(@class, "x9f619")]/div[@class="_ap3a _aaco _aacu _aacy _aad6 _aade"]').text
    except NoSuchElementException:
        inner_bio = ""
    data[user] = {
        'bio': [inner_bio, bio],
    }

filename = 'data.json'
try:
    with open(filename, 'r') as json_file:
        existing_data = json.load(json_file)
except json.decoder.JSONDecodeError:
    existing_data = []

updated_data = update_json(existing_data, data)

with open('data.json', 'w') as file:
    json.dump(updated_data, file, indent=4)

driver.quit()
