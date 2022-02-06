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
def valid_date(s):
	"""
	Helper function that checks the command line input that execution_date is specified correctly. In this case: %Y-%m-%d_%H%M
	"""
	try:
		return datetime.strptime(s, "%Y%m%d_%H%M")
	except ValueError:
		err_msg = "not a valid datetime: {0}. Use this format:{1}".format(s,"%Y%m%d_%H%M")
		raise argparse.ArgumentTypeError(err_msg)

### Initialize variables ###
# Initialize key variables
album_ids=['53qPFVC', 'ogO04u0'] # album ids of: (1) Memes album, (2) m4m album
img_ext = '.jpg' # file extension to be added to the end of image URL (for download)


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

	return client, imgur_username

def get_meme_details(client: object, album_ids:list, num_of_memes: int)->tuple:
	"""
	Sends a 'GET' request to retrieve all the image objects within the specified album in the form of a list
	Iterates through the list and returns 2 lists which are subsets of it: image ID, and image URL for the num_of_memes that is specified
	"""
	# Sends 'GET' request to retrieve all image objects
	meme_ids=list(); meme_links=list()
	album_images = client.get_album_images(album_id=album_ids[1])

	# Iterate through all the image objects and retrieve image_id, image_links
	for i in range(num_of_memes):
		meme_ids.append(album_images[i].id)
		meme_links.append(album_images[i].link)

	return client, meme_ids, meme_links

def historize_and_dl(client:object, album_ids:list, meme_ids:list, meme_links:list, num_of_memes:int, execution_datetime: object, dl_dir:str, img_ext: str)->None:
	"""
	Historize:
	1. Sends a 'POST' request to add the meme_ids into Memes album
	2. Sends a 'DELETE' remove to the meme_ids from m4m album
	Download:
	3. Downloads the memes into dl_dir
	"""
	# Move the meme_ids images from m4m album into memes album
	client.album_add_images(album_id=album_ids[0], ids=meme_ids)
	client.album_remove_images(album_id=album_ids[1], ids=meme_ids)

	# Download the memes into dl_dir
	exec_date = datetime.strftime(execution_datetime, "%Y%m%d")
	exec_time = datetime.strftime(execution_datetime, "%H%M")

	os.makedirs(dl_dir,mode=0o777,exist_ok=True)

	for i in range(len(meme_links)):
		r = requests.get(meme_links[i])
		with open(os.path.join(dl_dir, '{0}_{1}_{2}{3}'.format(exec_date, exec_time, i, img_ext)), 'wb') as f:
			f.write(r.content)


if __name__ == "__main__":

	# Parse arguments
	my_parser = argparse.ArgumentParser(prog='app_extract.py', description='Python script that connects to Imgur and downloads, and rearrange memes (within Imgur account). For personal use', usage='%(prog)s execution_date: object format is %%Y%%m%%d_%%H%%M "authentication_file_path: str" "dl_directory_file_path: str" number_of_memes: int')

	my_parser.add_argument("execution_date", help="Input execution datetime as %Y%m%d_%H%M", type=valid_date)
	my_parser.add_argument("authentication_file_path", help="Input absolute file path to authentication file", type=str)
	my_parser.add_argument("dl_dir", help="Input download directory to store memes", type=str)
	my_parser.add_argument("num_of_memes", help="Number of memes to download", type=int)
	my_args=my_parser.parse_args()

	# Start application
	client, username = auth(my_args.authentication_file_path)
	client, meme_ids, meme_links = get_meme_details(client, album_ids, my_args.num_of_memes)
	historize_and_dl(client, album_ids, meme_ids, meme_links, my_args.num_of_memes, my_args.execution_date, my_args.dl_dir, img_ext)
