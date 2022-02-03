### Import Libraries ###
# Import selenium classes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Import other modules
import time
import pyautogui
import ctypes
import logging
import argparse
import os

# Import config files
import login_cfg

### Helper Functions ###
# Initialize logger function
# logging.basicConfig(
# 	filename="sample.log", 
# 	level=logging.DEBUG,
# 	format="[%(levelname)s.%(levelno)s] %(asctime)s - %(message)s",
# 	filemode='w'
# 	)
#logging.getLogger()

# Custom sleep function that prints or logs sleep progress
def sleep_timer(a: int, b: str = 'print', c: str = 'debug') -> None:
	"""
	Sleeps for a specified time. Print or log each second's progress
	a: time in seconds
	b: specify 'print' or 'log' the progress. If 'log' is specified, provide c as logger command level
	c: 'debug', 'info', 'warning', 'error', 'critical'. Default is debug
	"""
	if b == 'print':
		print('To sleep for {0} seconds'.format(a))
		for i in range(a):
			time.sleep(1)
			print('Completed sleep for: {0} seconds'.format(i+1))
	elif b == 'log':
		if c == 'debug':
			logger.DEBUG('To sleep for {0} seconds'.format(a))
			for i in range(a):
				time.sleep(1)
				logger.DEBUG('Completed sleep for: {0} seconds'.format(i+1))
		elif c == 'info':
			logger.INFO('To sleep for {0} seconds'.format(a))
			for i in range(a):
				time.sleep(1)
				logger.INFO('Completed sleep for: {0} seconds'.format(i+1))
		elif c == 'warning':
			logger.WARNING('To sleep for {0} seconds'.format(a))
			for i in range(a):
				time.sleep(1)
				logger.WARNING('Completed sleep for: {0} seconds'.format(i+1))
		elif c == 'error':
			logger.ERROR('To sleep for {0} seconds'.format(a))
			for i in range(a):
				time.sleep(1)
				logger.ERROR('Completed sleep for: {0} seconds'.format(i+1))
		elif c == 'critical':
			logger.CRITICAL('To sleep for {0} seconds'.format(a))
			for i in range(a):
				time.sleep(1)
				logger.CRITICAL('Completed sleep for: {0} seconds'.format(i+1))
		else:
			return "syntax error: c needs to be specified properly"
	return


### Initialize variables ###
# Login variables
userName = login_cfg.userName
somepassword=login_cfg.somepassword

# Other key variables
website_url='https://www.instagram.com/'
emulated_device="iPhone X" # valid devices: https://source.chromium.org/chromium/chromium/src/+/main:chrome/test/chromedriver/chrome/mobile_device_list.cc
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


### Application functions ###
def login_ig_home_page()->tuple:
	"""
	Launch selenium and close various pop-ups. To initialize to IG home page
	"""
	# Initialize selenium webdriver options
	options = webdriver.ChromeOptions()

	# Selenium webdriver options: in mobile version
	mobile_emulation = { "deviceName": emulated_device }
	# mobile_emulation = {
	#    "deviceMetrics": { "width": 768, "height": 768, "pixelRatio": 1.0 },
	#    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
	#    }
	options.add_experimental_option("mobileEmulation", mobile_emulation)

	# Selenium webdriver options: window size
	options.add_argument("start-maximized")
	# options.add_argument("window-size=1039,859")
	# options.add_argument("--headless")

	# Initialize selenium webdriver options: with devtools open
	# options.add_argument("--auto-open-devtools-for-tabs")
	# options.add_experimental_option("excludeSwitches", ["enable-automation"])
	# options.add_experimental_option('useAutomationExtension', False)

	# Initialize selenium webdriver to IG main page
	print('Launching selenium webdriver to: {0}'.format(website_url))
	driver = webdriver.Chrome(service=Service('C:\\Program Files (x86)\\chromedriver.exe'), options=options)
	driver.get(website_url)

	# Close the pop-up that says: Log-in
	wait = WebDriverWait(driver, 20)
	wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))).click()

	# Login to IG using selenium explicit waits
	print('Login into {0} using selenium explicit waits'.format(website_url))
	sleep_timer(2)

	wait.until(EC.element_to_be_clickable((By.NAME, 'username'))).send_keys(userName)
	wait.until(EC.element_to_be_clickable(( By.NAME, "password"))).send_keys(somepassword)
	# wait.until(EC.element_to_be_clickable(( By.XPATH, "//div[text()='Log In']/.."))).click()
	wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

	print('Login submitted. Wait for {} seconds for page to load'.format(3))
	sleep_timer(3)

	# Close 2 pop-ups after login: 1. Save login info. 2. Add IG to home page
	print('Using selenium explicit waits to close IG login pop-ups')
	print('Closing pop-up that requests to save login info')
	wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))).click()
	print('Closing pop-up that asks to add IG to home page')
	wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='aOOlW   HoLwm ']"))).click()

	print('IG account home page initalized. Sleep for {} seconds'.format(3))
	sleep_timer(3)

	return (driver, wait)

def post_ig_story(parent_dir: str, file_name: str, driver: object, wait: object)->None:
	"""
	From IG home page, post IG story
	parent_dir: Parent directory as a string
	file_name: File name as a string (inclusive of file extension)
	"""
	# Click on 'New Story' button
	wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mTGkH']"))).click()

	# Load meme as IG story input
	pyautogui.press('F4', interval=1)
	pyautogui.hotkey('ctrl','a',interval=1)
	pyautogui.press('backspace',interval=1)
	pyautogui.write(parent_dir)
	sleep_timer(1)
	pyautogui.press('enter')
	pyautogui.press('F6', presses=6, interval=0.5)
	pyautogui.write(file_name)
	pyautogui.press('enter')

	# IG story screen
	print('Executing other keyboard modules')
	pyautogui.click(x=screensize[0]/2, y=screensize[1]/2)
	sleep_timer(3)
	pyautogui.hotkey('ctrl','shift','j', interval=3)
	pyautogui.hotkey('ctrl','shift','m',interal=3)
	wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))).click()

	print('Upload button selected. Wait for {} seconds'.format(4))
	sleep_timer(4)
	return

def close_selenium(timeout: int)->None:
	"""
	Calls sleep_timer function. Before a given timeout, closes selenium webdriver
	"""
	print('Quitting selenium webdriver in {} seconds'.format(timeout))
	sleep_timer(timeout)
	driver.quit()

### Application main ###
if __name__=="__main__":

	# Parse arguments
	my_parser = argparse.ArgumentParser(prog='app_egress.py', description='Upload Image to IG Story', usage='%(prog)s "${strings_of_file_paths[@]}"')
	my_parser.add_argument("meme_absolute_file_paths", help="Array consisting of absolute paths to image files as strings. Use backslash for windows file paths", type=str, nargs='+')
	my_args = my_parser.parse_args()

	# Application Start
	webdr_object, webdr_wait_object = login_ig_home_page()
	for i in my_args.meme_absolute_file_paths:
		parent_dir=os.path.split(i)[0]
		file_name=os.path.split(i)[1]
		post_ig_story(parent_dir, file_name, webdr_object, webdr_wait_object)
	close_selenium()
