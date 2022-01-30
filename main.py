### Import Libraries ###
# Import selenium classes
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options

# Import other modules
import time
import login_cfg
import pyautogui
import ctypes

### Initialize variables ###
# Login variables
userName = login_cfg.userName
somepassword=login_cfg.somepassword

# Other key variables
sleep_timer=10
website_url='https://www.instagram.com/'
emulated_device="iPhone X" # valid devices: https://source.chromium.org/chromium/chromium/src/+/main:chrome/test/chromedriver/chrome/mobile_device_list.cc
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Initialize selenium webdriver options: in mobile version
mobile_emulation = { "deviceName": emulated_device }
# mobile_emulation = {
#    "deviceMetrics": { "width": 768, "height": 768, "pixelRatio": 1.0 },
#    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
#    }

options = webdriver.ChromeOptions()
# options.add_argument("window-size=1039,859")
options.add_experimental_option("mobileEmulation", mobile_emulation)

## Initialize selenium webdriver options: with devtools open
options.add_argument("start-maximized")
# options.add_argument("--auto-open-devtools-for-tabs")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

# Initialize selenium webdriver
driver = webdriver.Chrome(options=options, executable_path='C:\\Program Files (x86)\\chromedriver.exe')


### Application start ###
# Launch selenium webdriver to IG main page
print('Launching selenium webdriver to: {0}'.format(website_url))
driver.get(website_url)
pyautogui.press(['win+left'])

# Close the pop-up that says: Log-in
wait = WebDriverWait(driver, 20)
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))).click()

# Login to IG using selenium explicit waits
print('Logging into {0} using selenium explicit waits'.format(website_url))
wait.until(EC.element_to_be_clickable((By.NAME, 'username'))).send_keys(userName)
wait.until(EC.element_to_be_clickable(( By.NAME, "password"))).send_keys(somepassword)
# wait.until(EC.element_to_be_clickable(( By.XPATH, "//div[text()='Log In']/.."))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
# print('Login successfully triggered. Wait for {0} seconds for page to load'.format(sleep_timer))

for i in range(sleep_timer):
	time.sleep(1)
	print('Completed sleep for: {0} seconds'.format(i+1))

# Close 2 pop-ups after login: 1. Save login info. 2. Add IG to home page
print('Use selenium explicit waits to close IG login pop-ups')
print('Close pop-up that requests to save login info')
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))).click()

print('Close pop-up that asks to add IG to home page')
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='aOOlW   HoLwm ']"))).click()


print('Initalized IG account home page. Now attempting to post. SLEEP for 5 first')
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mTGkH']"))).click()
print('Sleep for {} seconds'.format(5))
for i in range(5):
	time.sleep(1)
	print('Completed sleep for: {0} seconds'.format(i+1))

print('start experimental keyboard')
# pyautogui.press(['F4','ctrl+a','backspace'],interval=1)
pyautogui.press('F4', interval=1)
pyautogui.hotkey('ctrl','a',interval=1)
pyautogui.press('backspace',interval=1)
# time.sleep(1)
# keyboard.press_and_release('ctrl+a')
# time.sleep(1)
# keyboard.press_and_release('backspace')
# time.sleep(1)
pyautogui.write('file_path_to_Desktop')
time.sleep(1)
pyautogui.press('enter')

pyautogui.press('F6', presses=6, interval=0.5)

pyautogui.write('name_of_meme.jpg')
pyautogui.press('enter')

# print('Execute experimental path')
# #wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mTGkH']")))
# driver.find_element(By.XPATH, "//input[@class='tb_sK']").send_keys("C:\\Users\\bennb\\OneDrive\\Desktop\\yoda.jpg")

print('Executing other keyboard modules')
pyautogui.click(x=screensize[0]/2, y=screensize[1]/2)
for i in range(3):
	time.sleep(1)
	print('Completed sleep for: {0} seconds. mouse has clicked'.format(i+1))

pyautogui.hotkey('ctrl','shift','j', interval=3)
pyautogui.hotkey('ctrl','shift','m',interal=3)

# pyautogui.press(['ctrl+shift+j', 'ctrl+shift+m'], interval=3)

# keyboard.press_and_release('ctrl+shift+j')
# for i in range(5):
# 	time.sleep(1)
# 	print('Completed sleep for: {0} seconds'.format(i+1))

# keyboard.press_and_release('ctrl+shift+m')
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))).click()

for i in range(3):
	time.sleep(1)
	print('Completed sleep for: {0} seconds'.format(i+1))

for i in range(5):
	time.sleep(1)
	print('Completed sleep for: {0} seconds'.format(i+1))
### Close selenium webdriver ###
print('Quitting selenium webdriver')
driver.quit()

