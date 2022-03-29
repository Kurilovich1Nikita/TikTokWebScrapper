import argparse
import json
import os
import random
import requests
import sys
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TikTokBot():
	def __init__(self):
		self.driver = webdriver.Chrome()

	def create_dir(self):
		i = 0
		while True:
			try:
				os.mkdir(self.username)
				os.chdir(self.username)
				break
			except FileExistsError:
				i += 1

def arg_parse():
	parser = argparse.ArgumentParser(description="TikTok WebScrapping")
	parser.add_argument("--username", help="Profile Username", required=True, nargs=1)
	return parser.parse_args()

args = arg_parse()

# bot = TikTokBot()
# bot.driver.get('https://tiktok.com/'+args.username[0])
# soup = BeautifulSoup(bot.driver.page_source, "html.parser")
# meta_needed = soup.find_all('meta')
# st = str(meta_needed[5])
# likes = st.split("Лайки: ", 1)[1].split("Фанаты:", 1)[0]
# fans = st.split("Фанаты: ", 1)[1].split(" ", 1)[0]
# description = st.split(fans + " ", 1)[1].split(" data-rh", 1)[0]
# print("Description: " + description)
# print("Likes: " + likes)
# print("Fans: " + fans)
# bot.driver.quit()

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)
driver.get('https://tiktok.com/'+args.username[0])

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

browser_log = driver.get_log('performance') 
events = [process_browser_log_entry(entry) for entry in browser_log]
events = [event for event in events if 'Network.response' in event['method']]
#print(events)


url_needed = ''

for event in events:
	str_event = str(event)
	if 'https://www.tiktok.com/api/user/detail/' in str_event:
		#print(str_event)
		#print(str_event.split("url", 1)[1].split("}", 1)[0])
		url_needed = str_event.split("url': '", 1)[1].split("'}", 1)[0]

#print(url_needed)

#driver.get(url_needed)

#driver.quit()

#r = requests.get(url_needed)

#soup = BeautifulSoup(r.text, "html.parser")

#print(soup)

#r = requests.get(url_needed)

#print(r.text)

driver.get(url_needed)

#print(driver.page_source)

st = str(driver.page_source)
id = st.split("id\":\"", 1)[1].split("\"", 1)[0]
print("Id: " + id)
unique_id = st.split("uniqueId\":\"", 1)[1].split("\"", 1)[0]
print("Unique Id: " + unique_id)
nickname = st.split("nickname\":\"", 1)[1].split("\"", 1)[0]
print("Nickname: " + nickname)
signature = st.split("signature\":\"", 1)[1].split("\"", 1)[0]
print("Signature: " + signature)
verified = st.split("verified\":", 1)[1].split(",", 1)[0]
print("Verified: " + verified)
bio_link = st.split("bioLink\":{\"link\":\"", 1)[1].split("\"", 1)[0]
print("Bio Link: " + bio_link)
private_account = st.split("privateAccount\":", 1)[1].split(",", 1)[0]
print("Private account: " + private_account)
isUnderAge18 = st.split("isUnderAge18\":", 1)[1].split("}", 1)[0]
print("Is under age 18: " + isUnderAge18)
following_count = st.split("followingCount\":", 1)[1].split(",", 1)[0]
print("Following count: " + following_count)
follower_count = st.split("followerCount\":", 1)[1].split(",", 1)[0]
print("Follower count: " + follower_count)
heart_count = st.split("heartCount\":", 1)[1].split(",", 1)[0]
print("Heart count: " + heart_count)
video_count = st.split("videoCount\":", 1)[1].split(",", 1)[0]
print("Video count: " + video_count)



driver.quit()