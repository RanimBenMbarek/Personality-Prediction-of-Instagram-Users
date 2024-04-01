from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests
import os
import time
import uuid
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
service = Service("C:/Users/dossc/Desktop/Pfa/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.instagram.com/")

time.sleep(2)
username = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
username.send_keys(config['username'])
password = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
password.send_keys(config['password'])
password.send_keys(Keys.ENTER)

time.sleep(10)
instagram_profiles =  ["edward_barber","noahschnacky",
"noahschnapp","harrywinks"]

for user in instagram_profiles:
    driver.get(f"https://www.instagram.com/{user}/")
    time.sleep(10)
    more_infos = driver.find_element(By.TAG_NAME, "ul")
    number_of_posts = more_infos.find_element(By.XPATH,
                                              "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span")
    followers = more_infos.find_element(By.XPATH,
                                         "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span")
    try:
        followees = more_infos.find_element(By.XPATH,
                                        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span")
    except NoSuchElementException:
        followees = more_infos.find_element(By.XPATH,
                                          "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/span/span")
    
    try:
        inner_bio = driver.find_element(By.XPATH, '//*[contains(@class, "_ap3a") and contains(@class, "_aaco") and contains(@class, "_aacu") and contains(@class, "_aacx") and contains(@class, "_aad6") and contains(@class, "_aade")]').text
    except NoSuchElementException:
        inner_bio = "N/A"
    try:
       bio = driver.find_element(By.XPATH, '//div[contains(@class, "x9f619")]/div[@class="_ap3a _aaco _aacu _aacy _aad6 _aade"]').text
    except NoSuchElementException:
        bio = "N/A"

    data = {
     'user': user,
        'posts_count': number_of_posts.text,
        'followers_count': followers.text,
        'followees_count': followees.text,
        'posts': [],
        'bio':[bio,inner_bio],
        'O':0,
        'C':0,
        'E':0,
        'A':0,
        'N':0
    }

    post_count = 0
    downloaded_urls = set()
    while post_count < 100:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        posts = driver.find_elements(By.CLASS_NAME, '_aagv')
        for post in posts:
            if post_count >= 100:
                break
            image = post.find_element(By.TAG_NAME, 'img')

            post_caption = image.get_attribute('alt')
            image_url = image.get_attribute('src')

            if image_url not in downloaded_urls:
                post_count += 1
                downloaded_urls.add(image_url)
                post_id = str(uuid.uuid4())
                data['posts'].append({
                    'post_id': post_id,
                    'caption': post_caption,
                    'url': image_url,
                })
                response = requests.get(image_url)
                if response.status_code == 200:
                    os.makedirs(f"images/{user}", exist_ok=True)
                    with open(f"images/{user}/{post_id}.jpg", "wb") as file:
                        file.write(response.content)
                    print(f"Image {post_count} de {user} téléchargée avec succès.")
                else:
                    print(f"Échec du téléchargement de l'image {post_count} de {user}.")

    # Append data to captions.json file
    filename = 'data.json'
    try:
        with open(filename, 'r') as json_file:
            existing_data = json.load(json_file)
    except json.decoder.JSONDecodeError:
        existing_data = []

    existing_data.append(data)
    with open(filename, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

driver.quit()
