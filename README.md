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
  - Imgur API is also confirmed to be free for non-commercial usage (https://apidocs.imgur.com/)
### Learning
- Exposure to API, `json, requests`

## Transform
### Objective
- Image processing - convert the meme into a resolution that people can read, and will not be distorted when uploaded into IG story
### Considerations
- IG stories only support fixed resolutions, so an image processing engine is required to fit images to predefined resolutions
  - Expected tasks:
    - Image resizing (to change either height, or width or both dimensions of the image)
    - Image padding (to "gracefully" manipulate image dimension size while keeping original image untouched)
    - Image collage (to collage multiple images together)
- Bash file handling
  - Basic shell scripting for file handling and passing variables into <i>app_transform.py</i>
### Learning
- Exposure to variety of image processing libraries like `PIL and OpenCV` (just need to choose one)
- Chance to practise `numpy`, and get more familiar with python file handling commands (aka: the `os` utility module)

## Egress
### Objective
- Upload the transformed or edited image onto IG (and/or: Imgur)
### Considerations
- Do it using: (1) API, or (2) Web crawling (this is very manual)

<ins>(1) API</ins>
- IG has 2 types of official APIs, both of them are not suitable for my purpose:
  - Instagram Basic Display API
    - Allows app builders to interact with Instagram. However, this is mostly for Android/iOS developers and does not serve my purpose, which is simply to share memes
  - Instagram Graph API
    - API cannot access Instagram consumer accounts (i.e., non-Business or non-Creator Instagram accounts)
- As is also no officially maintained IG API for Python (it has been taken down a while ago in 2021)
- It goes against IG TOS to share code for unofficial APIs online, as it probably uses legacy access tokens, so using something like that could be infringement
  - These APIs come and go within a few months, and spending time to learn how to tweak it each time does not sound palatable
  - 3rd Party API: There are other 3rd party APIs available (others have ported/cloned Instagram API before it got taken down). They use existing tokens that expires after a set period of time (i believe it refreshes every 90days)

<ins>(2) Web crawling</ins>
- Use web scraping libraries to navigate in IG website
  - Well known ones are `beautifulsoup, selenium`
  - Might need some keyboard and mouse click libraries like `keyboard, Robot, or PyAutoGUI`
- Cons: 
  - As this is semi "automated", might not be the most elegant way
  - There is a chance that another computer's browser will respond differently

<ins>Choice</ins>
- Decided to go with the web crawling method. It heavily leverages on Python libraries like Selenium and PyAutoGUI for keyboard and mouse clicks. This is very  "home_made", and "rough". But it does not get taken down in a matter of months (like other 3rd party APIs; no need to deal with any access tokens). It's also good exposure for a beginner
- For a home-made simple project, and interest in learning other python libraries, will opt to explore 3rd party APIs another time (for code enhancements/improvements). After all, i am already having some exposure to API in Extract stage
- The libraries i decided to go with are `selenium and PyAutoGUI` as they are highly versatile (learning them might come in handy with future projects)
### Learning
- Exposure to variety of Python libraries: `selenium, PyAutoGUI, time, ctypes`


# Progress
## Tasks at hand
### Preparation
- [x] Compile my personal memes (from various sources) into one folder
- [x] Create IMGUR account
- [ ] Upload my personal memes into IMGUR (limit is 50 per day)
### Extract
- [x] Explore IMGUR API, especially commands to: {download images, delete images from album, upload images from album}
- [ ] Build skeleton code
### Transform
- [x] Explore Python libraries to perform image operations: {resizing, padding, make collages}
- [x] Build skeleton code
- [x] Clean code & include argparse notations. Include ability to iterate and save multiple files with proper names
- [ ] Enable logger before leaving it autopilot
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
- Both packages seem similar and can fulfill my use cases. Another enhancement that is possible is to use K-means clustering to choose the most dominant color for image padding. Will choose OpenCV as it seems to be more versatile
- Just discovered a fatal oversight - IMGUR only allows for 50 uploads per day. The number of memes that I have locally are easily >5k. This means my personal memes might need some time before it is stored online
### 3. 02_02_2022
- Cleaned <i>app_egress.py</i> code, added in argparse notations and organized the code into main and function methods for better clarity. This also enables iteration of strings (and hence multiple jpeg files) when called upon by an external program (probably a bash script: can call Extract, Transform, and Egress in sequence)
- Created an IMGUR account and started to get familiar with the structure
- Downloaded existing memes into local C:\\ and removed them from google photos
- Completed skeleton code of app_transform.py
- Cleaned <i>app_transform.py</i> code, added in argparse and iterative behaviour and saving to output file directories with iterative file names
### 4. 03_02_2022
- Starting building skeleton code for app_extract.py


# Future enhancements (for consideration)
## Extract
- [ ] Possibly execute the commands using Postman (?)
## Transform
- [ ] Use K-means clustering to return the most dominant color for a given image (to pad the image)
## Load
- [ ] Explore IG Basic API (future enhancement)
