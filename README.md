# m4m - Motivation
Memes are a big part of my life. Short, succinct catchphrases that are straight to the point and widely entertaining. They bring humour to the daily mundane. Sharing memes on my personal instagram story have become such a personal daily ritual that my friends and family have come to love them

Hence the idea - create an ETL automated pipeline that schedules meme uploads to my personal Instagram Story. This is a personal project to learn to build something myself, and gain exposure to a variety of automation tools: <b>Memes for masses</b>


# ETL Description
## Extract
### Objective
- Download/retrieve memes from a storage space into local memory - in preparation for image processing
### Considerations
- A repo with huge file storage is needed to store memes (as they are all image files)
  - Decided to go with imgur as they offer unlimited uploads and downloads
  - Imgur API is also confirmed to be free for non-commercial usage # https://apidocs.imgur.com/
### Learning
- Exposure to API, JSON file formats, requests

## Transform
### Objective
- Image processing - convert the meme into a resolution that people can read, and will not be distorted when uploaded into IG story
### Considerations
- IG stories only support fixed resolutions, so an image processing engine is required to fit images to predefined resolutions
  - Expected tasks:
    - Image resizing (to change either height, or width or both dimensions of the image)
    - Image padding (to "gracefully" manipulate image dimension size while keeping original image untouched)
    - Image collage (to collage multiple images together)
- Bash/Python file handling
  - Basic python commands for file handling (like mv, ls, cp, rm, mkdir along with their options: equivalents of bash)
### Learning
- Exposure to variety of image processing libraries like PIL and OpenCV (just need to choose one)
- Chance to practise numpy, and get more familiar with python file handling commands (aka: the os utility module)

## Egress
### Objective
- Upload the transformed or edited image onto IG (and/or: Imgur)
### Considerations
- Do it using: (1) API, or (2) Web crawling (this is very manual)\
<u>(1) API</u>
- IG has 2 types of official APIs, both of them are not suitable for my purpose:
  - Instagram Basic Display API
    - Allows app builders to interact with Instagram. However, this is mostly for Android/iOS developers and does not serve my purpose, which is simply to share memes
  - Instagram Graph API
    - API cannot access Instagram consumer accounts (i.e., non-Business or non-Creator Instagram accounts)
- As is also no officially maintained IG API for Python (it has been taken down a while ago in 2021)
- It goes against IG TOS to share code for unofficial APIs online, as it probably uses legacy access tokens, so using something like that could be infringement
  - These APIs come and go within a few months, and spending time to learn how to tweak it each time does not sound palatable
  - 3rd Party API: There are other 3rd party APIs available (others have ported/cloned Instagram API before it got taken down). They use existing tokens that expires after a set period of time (i believe it refreshes every 90days)

<u>(2) Web crawling</u>
- Use web scraping libraries to navigate in IG website
  - Well known ones are BeautifulSoup, or Selenium
  - Might need some keyboard and mouse click libraries like keyboard, Robot, or PyAutoGUI
- Cons: 
  - As this is semi "automated", might not be the most elegant way
  - There is a chance that another computer's browser will respond differently

<u>Choice</u>
- For a home-made simple project, and interest in learning other python libraries, will opt to explore 3rd party APIs another time (for code enhancements/improvements). After all, i am already having some exposure to API in Extract stage
- Hence decided to go with the web crawling method. It heavily leverages on Python libraries like Selenium and PyAutoGUI for keyboard and mouse clicks. This is very  "home_made", and "rough". But it does not get taken down in a matter of months (like other 3rd party APIs). It's also good exposure for a beginner (like me)
- The libraries i decided to go with are Selenium and PyAutoGUI as they are highly versatile (learning them might come in handy with future projects)
### Learning
- Exposure to variety of Python libraries: Selenium, PyAutoGUI, time, ctypes


# Progress
## Tasks at hand
### Preparation
- [ ] Compile my personal memes (from various sources) into one folder
- [ ] Create IMGUR account
- [ ] Upload my personal memes into IMGUR (limit is 50 per day)
### Extract
- [ ] Explore IMGUR API, especially commands to: {download images, delete images from album, upload images from album}
### Transform
- [x] Explore Python libraries to perform image operations: {resizing, padding, make collages}
- [ ] Build skeleton code
- [ ] Explore Python methods for file handling
### Egress
- [x] Explore Selenium commands to: {initialize browser in dev/mobile mode, login to IG.com, close IG pop-ups}
- [x] Explore other Python libraries to: {navigate in an opened windows explorer since IG Story API is not available to POST images like jpeg afaik}
- [x] Clean code
- [x] Enhance code: {enable argument parsing, repeated uploads}
- [ ] Enable logger before leaving it autopilot

## Changelog
### 1. 31_01_2022
- Built a skeleton code that uses a variety of Python libraries to execute tasks on IG story: (1) Login, (2) Close pop-ups/notifications, (3) Select and upload image of interest
- Just found out that there are other unofficially maintained API to perform this function. To explore further next time
### 2. 01_02_2022
- Read up about PIL and OpenCV package resizizing methods. Thought about the "flow" to resize and conditions needed to trigger so
- Both packages seem similar and can fulfill my use cases. Another enhancement that is possible is to use K-means clustering to pad the images with the most dominant colour. Will choose OpenCV as it seems to be more versatile
- Just discovered a fatal oversight - IMGUR only allows for 50 uploads per day. The number of memes that I have locally are easily >5k. This prompts me to quickly learn how to interact with IMGUR API
### 3. 02_02_2022
- Cleaned app_egress.py <i>(or egress)</i> main code, added in argparse notations and organized the code into main and function methods for better clarify. This enables iteration of strings later on (or multiple jpeg files)


# Future enhancements (for consideration)
## Extract
- [ ] Possibly execute the commands using Postman (?)
## Transform
- [ ] Write a personal K-means clustering to return the most dominant color for a given image (can be used to pad images)
## Load
- [ ] Explore IG Basic API (future enhancement)
