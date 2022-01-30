# insta_memers - Motivation
Over the past few years, memes have become a big part of my life\
Short, succinct catchphrases that are widely entertaining because they bring humour to daily routine\
Sharing memes on my personal instagram story have become such a personal daily ritual, my friends and family have come to love them

Hence the idea - create an ETL automated pipeline that schedules meme uploads to my personal Instagram Story\
While there are plugins and other schedulers available, this is a personal project to learn to build something myself, and gain exposure to personal automation skills

# insta_memers - ETL Description
## Extract
- A repo with huge file storage is needed to store memes (as they are all image files)
  - For this i have decided to go with imgur as they offer unlimited uploads and downloads (limit on upload: 50 / day for free account)
  - Imgur API is also free for non-commercial usage
- Learning: Exposure to API, JSON file formats, requests

## Transform
- As IG stories only support fixed resolutions, an image processing engine is required
  - Expected tasks to fit image to IG story screen size:
    - Image resizing (to change either height, or width or both dimensions of the image)
    - Image padding (to "gracefully" manipulate image dimension size while keeping original image untouched)
    - Image collage (to collage multiple images together)
- Bash/Python file handling
  - Basic python commands for file handling (like mv, ls, cp, rm, mkdir along with their options: equivalents of bash)
- Learning: Exposure to variety of image processing libraries. Chance to use numpy, and get more familiar with python file commands equivalent of bash

## Load
- Upload the formatted image to IG story by heavily leveraging on WebScraper library Selenium
- Learning: Exposure to variety of Python libraries: Selenium, PyAutoGUI, time, ctypes

# Progress
## Changelog
### 31_01_2022
Built a skeleton code that uses a variety of Python libraries to execute tasks on IG story: (1) Login, (2) Close pop-ups/notifications, (3) Select and upload image of interest

# Tasks at hand
## Extract
- [ ] Create IMGUR account
- [ ] Explore IMGUR API, especially commands to: {download images, delete images from album, upload images from album}
- [ ] Might require knowledge of using Postman
## Transform
- [ ] Explore Python libraries to perform image operations: {resizing, padding, make collages}
- [ ] Explore Python methods for file handling
## Load
- [x] Explore Selenium commands to: {initialize browser in dev/mobile mode, login to IG.com, close IG pop-ups}
- [x] Explore other Python libraries to: {navigate in an opened windows explorer since IG Story API is not available to POST images like jpeg afaik}
- [ ] Clean up code
