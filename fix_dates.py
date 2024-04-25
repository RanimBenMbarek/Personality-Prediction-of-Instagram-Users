from datetime import datetime

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
                if item.get('most_recent_date') != info.get('most_recent_date'):
                    item['most_recent_date'] = info['most_recent_date']
                    item['least_recent_date'] = info['least_recent_date']

                    updated = True
                    print(f"Dates of {user} are Updated Successfully")
                    break
        if not updated:
            existing_data.append({
                'most_recent_date': info['most_recent_date'],
                'least_recent_date': info['least_recent_date']
            })
            print(f"New user {user} is added with bio and dates")

    return existing_data


with open('config.json', 'r') as config_file:
    config = json.load(config_file)

service = Service("C:/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.instagram.com/")

time.sleep(2)
username_input = driver.find_element(By.XPATH,
                                     "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
username_input.send_keys(config['username'])
password_input = driver.find_element(By.XPATH,
                                     "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
password_input.send_keys(config['password'])
password_input.send_keys(Keys.ENTER)

time.sleep(10)
instagram_profiles = [
    "theweeknd",
]
data = {}
for user in instagram_profiles:
    driver.get(f"https://www.instagram.com/{user}/")
    time.sleep(3)
    post_count = 0
    downloaded_urls = set()
    done = False

    more_infos = driver.find_element(By.TAG_NAME, "ul")
    number_of_posts = more_infos.find_element(By.XPATH,
                                              "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span")

    min_date = datetime.max.strftime('%Y-%m-%d')
    max_date = datetime.min.strftime('%Y-%m-%d')
    while post_count < 100:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        elements = driver.find_elements(By.CSS_SELECTOR,
                                        '.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x2pgyrj.xbkimgs.xfllauq.xh8taat.xo2y696')
        for i, element in enumerate(elements):
            if post_count >= 100:
                break
            post = element.find_element(By.CLASS_NAME, '_aagv')
            try:
                pinned = element.find_element(By.CLASS_NAME, '_aatp')
            except NoSuchElementException:
                pinned_exists = False

            # Navigate up to the closest ancestor 'a' element
            ancestor_a = post.find_element(By.XPATH, ".//ancestor::a")

            # Now, you can get the href attribute
            href_value = ancestor_a.get_attribute('href')

            try:
                svg_element = pinned.find_element(By.TAG_NAME, 'svg')
                title_element = svg_element.get_attribute('aria-label')
                if title_element == "Pinned post icon":
                    pinned_exists = True
                else:
                    pinned_exists = False
            except NoSuchElementException:
                pinned_exists = False

            image = post.find_element(By.TAG_NAME, 'img')
            post_caption = image.get_attribute('alt')
            image_url = image.get_attribute('src')
            if image_url in downloaded_urls:
                continue

            if done is False:
                if pinned_exists == False:
                    done = True
                driver.execute_script("window.open('');")
                new_tab = driver.window_handles[-1]
                driver.switch_to.window(new_tab)

                driver.get(href_value)

                time.sleep(5)
                try:
                    date_element = driver.find_element(By.XPATH,
                                                       '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div/div/a/span/time')
                    datetime_value = date_element.get_attribute('datetime')
                    parsed_datetime = datetime.strptime(datetime_value, '%Y-%m-%dT%H:%M:%S.%fZ')
                    # Format the datetime object to display only the date in the format 'YYYY-MM-DD'
                    formatted_date = parsed_datetime.strftime('%Y-%m-%d')

                    if formatted_date > max_date:
                        max_date = formatted_date

                except NoSuchElementException:
                    print("Datetime element not found.")

                driver.close()

                original_tab = driver.window_handles[0]
                driver.switch_to.window(original_tab)

            number_of_posts_text = number_of_posts.text.replace(',', '')
            if post_count == int(number_of_posts_text) - 1 or post_count == 99:
                driver.execute_script("window.open('');")
                new_tab = driver.window_handles[-1]
                driver.switch_to.window(new_tab)

                driver.get(href_value)

                time.sleep(5)
                try:
                    date_element = driver.find_element(By.XPATH,
                                                       '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div/div/a/span/time')
                    datetime_value = date_element.get_attribute('datetime')
                    parsed_datetime = datetime.strptime(datetime_value, '%Y-%m-%dT%H:%M:%S.%fZ')
                    # Format the datetime object to display only the date in the format 'YYYY-MM-DD'
                    min_date = parsed_datetime.strftime('%Y-%m-%d')

                except NoSuchElementException:
                    print("Datetime element not found.")
                driver.close()

                original_tab = driver.window_handles[0]
                driver.switch_to.window(original_tab)
            if image_url not in downloaded_urls:
                post_count += 1
                downloaded_urls.add(image_url)
                print("photo num ", post_count)

    data[user] = {
        'most_recent_date': max_date,
        'least_recent_date': min_date,
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
