from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import os
import time
import uuid
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
service = Service("C:/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.instagram.com/")

time.sleep(5)
username = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
username.send_keys(config['username'])
password = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
password.send_keys(config['password'])
password.send_keys(Keys.ENTER)

time.sleep(10)
instagram_profiles = ["Kalopsia.tn"]
all_data = {}
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

    bio = more_infos.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/h1")

    data = {
        'user': user,
        'posts_count': number_of_posts.text,
        'followers_count': followers.text,
        'followees_count': followees.text,
        'bio':bio.text,
        'posts': [],
        'O':0,
        'C':0,
        'E':0,
        'A':0,
        'N':0
    }

    post_count = 0
    downloaded_urls = set()
    while post_count < 20:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        posts = driver.find_elements(By.CLASS_NAME, '_aagv')

        for post in posts:
            if post_count >= 20:
                break

            # Navigate up to the closest ancestor 'a' element
            ancestor_a = post.find_element(By.XPATH, ".//ancestor::a")

            # Now, you can get the href attribute
            href_value = ancestor_a.get_attribute('href')
            print(href_value)

            image = post.find_element(By.TAG_NAME, 'img')
            post_caption = image.get_attribute('alt')
            image_url = image.get_attribute('src')

            driver.execute_script("window.open('');")
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)
            driver.get(href_value)
            time.sleep(5)
            #more_infos = driver.find_element(By.TAG_NAME, "ul")
            try:
                date = driver.find_element(By.XPATH,
                                       "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/div/span[2]/time").text
            except NoSuchElementException:
                date = driver.find_element(By.XPATH,
                                       "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/div/span[4]/time").text

            author = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/div/span[1]/div/a/div/div/span").text

            print("date:", date)
            print('author:',author)

            driver.close()
            original_tab = driver.window_handles[0]
            driver.switch_to.window(original_tab)

            time.sleep(10)
            if (image_url not in downloaded_urls) and (user == author):
                post_count += 1
                downloaded_urls.add(image_url)
                post_id = str(uuid.uuid4())
                data['posts'].append({
                    'post_id': post_id,
                    'caption': post_caption,
                    'url': image_url,
                    'date': date
                })
                response = requests.get(image_url)
                if response.status_code == 200:
                    os.makedirs(f"images/{user}", exist_ok=True)
                    with open(f"images/{user}/{post_id}.jpg", "wb") as file:
                        file.write(response.content)
                    print(f"Image {post_count} de {user} téléchargée avec succès.")
                else:
                    print(f"Échec du téléchargement de l'image {post_count} de {user}.")


    all_data[user] = data

    # Append data to data.json file
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


