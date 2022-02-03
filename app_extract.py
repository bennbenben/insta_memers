### Import libraries ###
# Import selenium classes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Import other libraries
from imgurpython import ImgurClient
import configparser
import argparse
from collections import defaultdict
from datetime import datetime

### Helper functions ###
def valid_date(s):
	"""
	Helper function that checks the command line input that execution_date is specified correctly. In this case: %Y-%m-%d
	"""
	try:
		return datetime.strptime(s, "%Y%m%d_%H%M")
	except ValueError:
		err_msg = "not a valid datetime: {0}. Use this format:{1}".format(s,"%Y%m%d_%H%M")
		raise argparse.ArgumentTypeError(err_msg)

### Initialize variables ###
# Initialize key variables



### Application functions ###
def auth(auth_config_file_path: str)->object:
	"""
	Inputs absolute file path to auth.ini file (to onbtain login variables to imgur)
	Use both imgur API and selenium to authenticate imgur for a response token (valid for 60 mins)
	"""
	# Obtain login variables from authentication file
	config=configparser.ConfigParser()
	config.read(auth_config_file_path)
	client_id=config.get('credentials','client_id')
	client_secret=config.get('credentials','client_secret')
	imgur_username = config.get('credentials','imgur_username')
	imgur_password = config.get('credentials','imgur_password')

	# Initialize imgur client instance
	client = ImgurClient(client_id=client_id, client_secret=client_secret)
	auth_url = client.get_auth_url(response_type='pin')

	# Selenium handling 
	## Login to imgur authentication website
	driver = webdriver.Chrome(service=Service('C:\\Program Files (x86)\\chromedriver.exe'))
	driver.get(auth_url)
	username = driver.find_element(By.XPATH,'//*[@id="username"]')
	password = driver.find_element(By.XPATH,'//*[@id="password"]')
	username.clear()
	username.send_keys(imgur_username)
	password.send_keys(imgur_password)	
	driver.find_element(By.NAME, "allow").click()

	## Obtain pin from imgur website
	wait = WebDriverWait(driver, 20)
	wait.until(EC.presence_of_element_located((By.ID, 'pin')))
	pin=driver.find_element(By.XPATH, '//*[@id="pin"]').get_attribute('value')
	driver.close() # close selenium after obtaining the pin value

	# Set the imgur client instance with authorized pin. Obtain access and refresh tokens
	credentials=client.authorize(pin,grant_type='pin') # credentials is a dictionary
	client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
	print('Authentication success')
	# print(credentials, type(credentials))
	# print(client)

	return client

if __name__ == "__main__":

	# Parse arguments
	my_parser = argparse.ArgumentParser(prog='app_extract.py', description='Python script that connects to Imgur and downloads, and rearrange memes (within Imgur account). For personal use', usage='%(prog)s execution_date: object format:%%Y-%%m-%%d_%%H-%%M "authentication_file_path: str" "dl_directory_file_path: str" number_of_memes: int')

	my_parser.add_argument("execution_date", help="Input execution datetime as %Y%m%d_%H%M", type=valid_date)
	my_parser.add_argument("authentication_file_path", help="Input absolute file path to authentication file", type=str)
	my_parser.add_argument("dl_dir", help="Input download directory to store memes", type=str)
	my_parser.add_argument("num_of_memes", help="Number of memes to download", type=int)
	my_args=my_parser.parse_args()

	print(my_args) # check arguments

	# Start application
	c = auth(my_args.authentication_file_path)

	# for i in args.num_of_memes:

# Algo
# 1. Authenticate with Imgur - obtain response pin
# 2. Download the specified number of memes (to further explore on download method)

# items = client.gallery()
# # for i in items:
# # 	print(i.link)
# # 	print(i.title)
# # 	print(i.views)
# max_item=None
# max_views=0
# for i in items:
# 	if i.views > max_views:
# 		max_item = i
# 		max_views = i.views
# print(max_item.title)
