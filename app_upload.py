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
from datetime import datetime
import requests
import os

### Helper functions ###
album_ids=['53qPFVC', 'ogO04u0'] # album ids of: (1) Memes album, (2) m4m album


### Application functions ###
def auth(auth_config_file_path: str)->tuple:
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

	return client

def upload_to_album(client:object, image_path_list:list, album_id: str)->None:
	"""
	Takes in: 1. initiated client object, 2. list of image file paths, 3. imgur album id
	Performs: 1. uploading all the images in the image_file_paths specified, and saving their image_ids, 2. adds them to the specified album_id
	"""
	image_path_ids=list()
	for i in image_path:
		image = client.upload_from_path(image_path)
		image_path_ids.append(image.id)
	print("Done!")

	client.album_add_images(album_id=album_id, ids=image_path_ids)
	print("Added to album!")

	return

def get_upload_vars(parent_dir:str,destination_album:str):
	"""
	Takes in 2 strings: upload parent directory and the subfolder
	Returns a tuple of: (list of all images in the folder, correspond imgur album_id)
	"""
	image_path_list=list()
	folder_dir=os.path.join(parent_dir,destination_album)

	for i in os.listdir(folder_dir): image_path_list.append(os.path.join(parent_dir,i))

	print('destination_album is:{}'.format(destination_album))

	if destination_album=='memes':
		meme_album_id=album_ids[0]
		return image_path_list, meme_album_id

	elif destination_album=='m4m':
		m4m_album_id=album_ids[1]
		return image_path_list, m4m_album_id

if __name__ == "__main__":

	# Parse arguments
	my_parser = argparse.ArgumentParser(prog='app_extract.py', description='Python script that connects to Imgur and downloads, and rearrange memes (within Imgur account). For personal use', usage='%(prog)s execution_date: object format is %%Y%%m%%d_%%H%%M "authentication_file_path: str" "dl_directory_file_path: str" number_of_memes: int')

	my_parser.add_argument("authentication_file_path", help="Input absolute file path to authentication file", type=str)
	my_parser.add_argument("parent_dir", help="File path to parent directory that contains memes", type=str)
	my_parser.add_argument("destination_album", help="subfolder inside parent_dir that contains memes. m4m or memes", choices=['memes','m4m'], type=str)

	my_args=my_parser.parse_args()

	image_path_list, imgur_album_id=get_upload_vars(parent_dir=my_args.parent_dir,destination_album=my_args.destination_album)
	print('image_path_list is:{}'.format(image_path_list))
	print('imgur_album_id is: {}'.format(imgur_album_id))


	# Start application
	client = auth(my_args.authentication_file_path)
	upload_to_album(client=client,image_path_list=image_path_list ,album_id=imgur_album_id)

	
