# insta_memers - Motivation
Memes are a big part of my life. Short, succinct catchphrases that are straight to the point and widely entertaining. They bring humour to the daily mundane. Sharing memes on my personal instagram story have become such a personal daily ritual that my friends and family have come to love them

Hence the idea - create an ETL automated pipeline that schedules meme uploads to my personal Instagram Story. This is a personal project to learn to build something myself, and gain exposure to a variety of automation tools

# insta_memers - ETL Description
## Extract
- A repo with huge file storage is needed to store memes (as they are all image files)
  - Decided to go with imgur as they offer unlimited uploads and downloads (limit on upload: 50 / day for free account)
  - Imgur API is also free for non-commercial usage
- Learning: Exposure to API, JSON file formats, requests

## Transform
- As IG stories only support fixed resolutions, an image processing engine is required to fit images to predefined resolutions
  - Expected tasks:
    - Image resizing (to change either height, or width or both dimensions of the image)
    - Image padding (to "gracefully" manipulate image dimension size while keeping original image untouched)
    - Image collage (to collage multiple images together)
- Bash/Python file handling
  - Basic python commands for file handling (like mv, ls, cp, rm, mkdir along with their options: equivalents of bash)
- Learning: Exposure to variety of image processing libraries. Chance to use numpy, and get more familiar with python file commands equivalent of bash

## Load
- IG has 2 types of APIs:
  - Instagram Basic Display API
    - Allows for app builders to share to insta story, but setup is relatively cumbersome. There is also no officially, maintained IG python package
  - Instagram Graph API
    - API cannot access Instagram consumer accounts (i.e., non-Business or non-Creator Instagram accounts)
- There are other 3rd party APIs to perform this required task, but for a home-made simple project, and interest in learning other python libraries, will opt to explore the API next time
- This method heavily leverages on WebScraper library Selenium and mouse clicks (it's very "manual", "home_made", and "rough"). But it does not get taken down in a matter of months (like other 3rd party APIs)
- Learning: Exposure to variety of Python libraries: Selenium, PyAutoGUI, time, ctypes

# Progress
## Changelog
### 1. 31_01_2022
- Built a skeleton code that uses a variety of Python libraries to execute tasks on IG story: (1) Login, (2) Close pop-ups/notifications, (3) Select and upload image of interest
- Just found out that there are other unofficially maintained API to perform this function. To explore further next time

# Tasks at hand
## Preparation
- [ ] Compile my personal memes (from various sources) into one folder
- [ ] Create IMGUR account
- [ ] Upload my personal memes into IMGUR (limit is 50 uploads per day)
## Extract
- [ ] Explore IMGUR API, especially commands to: {download images, delete images from album, upload images from album}
- [ ] Might require knowledge of using Postman
## Transform
- [ ] Explore Python libraries to perform image operations: {resizing, padding, make collages}
- [ ] Explore Python methods for file handling
## Load
- [x] Explore Selenium commands to: {initialize browser in dev/mobile mode, login to IG.com, close IG pop-ups}
- [x] Explore other Python libraries to: {navigate in an opened windows explorer since IG Story API is not available to POST images like jpeg afaik}
- [ ] Clean up code: {enable argument parsing, repeated uploads}
- [ ] Explore IG Basic API (future enhancement)
