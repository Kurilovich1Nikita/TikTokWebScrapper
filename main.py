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
	def __init__(self, username):
		self.driver = webdriver.Chrome()
		self.username = username
		self.retrieve_user_data()

	def create_dir(self):
		i = 0
		while True:
			try:
				os.mkdir(self.username)
				os.chdir(self.username)
				break
			except FileExistsError:
				i += 1

	def save_data(self, data_ar):
		with open(f'{self.username}_profile_data.txt','w') as f:
			for i in data_ar:
				f.write(i)
				f.write('\n')
		print(f"Profile data saved to {os.getcwd()}")

	def capture_token_signature(self):
		caps = DesiredCapabilities.CHROME
		caps['goog:loggingPrefs'] = {'performance': 'ALL'}
		self.driver = webdriver.Chrome(desired_capabilities=caps)
		self.driver.get('https://tiktok.com/'+self.username)

		def process_browser_log_entry(entry):
			response = json.loads(entry['message'])['message']
			return response

		browser_log = self.driver.get_log('performance') 
		events = [process_browser_log_entry(entry) for entry in browser_log]
		events = [event for event in events if 'Network.response' in event['method']]

		for event in events:
			str_event = str(event)
			if 'https://www.tiktok.com/api/user/detail/' in str_event:
				return str(str_event.split("url': '", 1)[1].split("'}", 1)[0])

	def retrieve_user_data(self):
		url = self.capture_token_signature()
		print(url)

		self.driver.get(url)

		data_ar = []

		st = str(self.driver.page_source)
		id = st.split("id\":\"", 1)[1].split("\"", 1)[0]
		data_ar.append("Id: " + id)
		print(data_ar[0])
		unique_id = st.split("uniqueId\":\"", 1)[1].split("\"", 1)[0]
		data_ar.append("Unique Id: " + unique_id)
		print(data_ar[1])
		nickname = st.split("nickname\":\"", 1)[1].split("\"", 1)[0]
		data_ar.append("Nickname: " + nickname)
		print(data_ar[2])
		signature = st.split("signature\":\"", 1)[1].split("\"", 1)[0]
		data_ar.append("Signature: " + signature)
		print(data_ar[3])
		verified = st.split("verified\":", 1)[1].split(",", 1)[0]
		data_ar.append("Verified: " + verified)
		if "bioLink" in st:
			bio_link = st.split("bioLink\":{\"link\":\"", 1)[1].split("\"", 1)[0]
			data_ar.append("Bio Link: " + bio_link)
		private_account = st.split("privateAccount\":", 1)[1].split(",", 1)[0]
		data_ar.append("Private account: " + private_account)
		print(data_ar[5])
		isUnderAge18 = st.split("isUnderAge18\":", 1)[1].split("}", 1)[0]
		data_ar.append("Is under age 18: " + isUnderAge18)
		print(data_ar[6])
		following_count = st.split("followingCount\":", 1)[1].split(",", 1)[0]
		data_ar.append("Following count: " + following_count)
		print(data_ar[7])
		follower_count = st.split("followerCount\":", 1)[1].split(",", 1)[0]
		data_ar.append("Follower count: " + follower_count)
		print(data_ar[8])
		heart_count = st.split("heartCount\":", 1)[1].split(",", 1)[0]
		data_ar.append("Heart count: " + heart_count)
		print(data_ar[9])
		video_count = st.split("videoCount\":", 1)[1].split(",", 1)[0]
		data_ar.append("Video count: " + video_count)
		print(data_ar[10])

		self.create_dir()
		self.save_data(data_ar)

		self.driver.quit()

def arg_parse():
	parser = argparse.ArgumentParser(description="TikTok WebScrapping")
	parser.add_argument("--username", help="Profile Username", required=True, nargs=1)
	return parser.parse_args()

def main():
	args = arg_parse()
	tb = TikTokBot(args.username[0])

main()
