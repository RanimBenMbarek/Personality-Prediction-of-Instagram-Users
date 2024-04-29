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
        # Dynamically find keys that match 'captionX' pattern and sort them
        caption_keys = sorted([key for key in info if key.startswith('caption')], key=lambda x: int(x[7:]))
        for item in existing_data:
            if item.get('user') == user:
                # Iterate over each post and corresponding caption key
                for post, caption_key in zip(item.get('posts'), caption_keys):
                    new_caption = info[caption_key]
                    if post.get('caption') != new_caption:
                        post['caption'] = new_caption
                        print(f"Updated caption : {new_caption} ")
    return existing_data



with open('config.json', 'r') as config_file:
    config = json.load(config_file)

service = Service("C:/Users/katko/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
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
    "yoorajung","zendaya",
    #"vancityreynolds",
    #"toby.hadoke","tomhanks","tonyleung_official","thesupertoken","tchalamet"
]
post_hops=1
data = {}
for user in instagram_profiles:
    driver.get(f"https://www.instagram.com/{user}/")
    time.sleep(3)
    post_count = 0
    downloaded_urls = set()
    done = False
    start_time = time.time()
    more_infos = driver.find_element(By.TAG_NAME, "ul")
    number_of_posts = more_infos.find_element(By.XPATH,
                                              "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span")

    diff_time=time.time()-start_time
    while post_count < 100+post_hops and diff_time<300:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        elements = driver.find_elements(By.CSS_SELECTOR,
                                        '.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x2pgyrj.xbkimgs.xfllauq.xh8taat.xo2y696')
        for i, element in enumerate(elements):
            if post_count >= 100+post_hops:
                break
            post = element.find_element(By.CLASS_NAME, '_aagv')


            # Navigate up to the closest ancestor 'a' element
            ancestor_a = post.find_element(By.XPATH, ".//ancestor::a")

            # Now, you can get the href attribute
            href_value = ancestor_a.get_attribute('href')

            image = post.find_element(By.TAG_NAME, 'img')
            post_caption = image.get_attribute('alt') #change this
            if post_caption.lower().startswith("photo"):
                driver.execute_script("window.open('');")
                new_tab = driver.window_handles[-1]
                driver.switch_to.window(new_tab)
                driver.get(href_value)
                time.sleep(5)
                #more_infos = driver.find_element(By.TAG_NAME, "ul")
                try:
                    post_caption = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/span").text
                except NoSuchElementException:
                    post_caption = "N/A"
                driver.close()
                original_tab = driver.window_handles[0]
                driver.switch_to.window(original_tab)

                time.sleep(2)
            image_url = image.get_attribute('src')
            if image_url in downloaded_urls:
                continue
            if image_url not in downloaded_urls:
                post_count += 1
                downloaded_urls.add(image_url)
                #print("photo num ", post_count,post_caption)
            if user not in data:
                data[user] = {}
            if post_count>post_hops:
                number="caption"+str(post_count)
                data[user][number] = post_caption
            diff_time=time.time()-start_time



filename = 'data2.json'
try:
    with open(filename, 'r') as json_file:
        existing_data = json.load(json_file)
except json.decoder.JSONDecodeError:
    existing_data = []

print(data)

updated_data = update_json(existing_data, data)
print(updated_data)
with open('test.json', 'w') as file:
    json.dump(updated_data, file, indent=4)

driver.quit()

#%%
