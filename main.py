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

		st = str(self.driver.page_source)
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
		if "bioLink" in st:
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

		self.driver.quit()

def arg_parse():
	parser = argparse.ArgumentParser(description="TikTok WebScrapping")
	parser.add_argument("--username", help="Profile Username", required=True, nargs=1)
	return parser.parse_args()

def main():
	args = arg_parse()
	tb = TikTokBot(args.username[0])

main()
