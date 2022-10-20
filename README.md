# Automated hotel reviewer
This program:
1. Parse hotel data from Booking.com and store it in SQLite database
2. Generate video reviews on hotels out from this data
3. Upload videos to YouTube via Selenium web driver

![image](https://user-images.githubusercontent.com/88551054/196950982-7c69c8e9-1218-4aa0-9c22-fd4e8835be35.png)


## 1. Parsing Booking.com
Parser divided into 2 files *search_parser.py* and *hotel_parser.py*

### Search_parser.py
Search_parser.py parse search results based on the request you send. Via URL parameters you can specify search requests as you do it on the booking webpage. For example, you can choose the city or country you are searching for, only 4-starts hotels, currency, and even sort mode.
The script collects all the hotels from the search results and stores them in a database. In this phase you have:
- Hotel id
- URL
- Price
- Currency

*Be sure to set up correct check-in and check-out dates*

### Hotel_parser.py
Hotel_parser.py goes through the database and updates missing information:
- Hotel name
- Country
- City
- District
- Stars
- Rating
- Nearest airport
- Distance from an airport
- Photo URLs (up to 30)
- Hotel description

To increase speed multithreading is implemented with the help of a concurrent.futures library.

*Before use check if there are no changes in HTML tags on booking.com*

## 2. Generate videos
Video creation is set up in *editor.py* file.

To automatically generate videos moviepy library which is based on the FFMPEG module is used.
The process is divided into 7 parts:
1. Taking parsed hotel data from the database
2. Generate JSON file with metadata for future video uploading
3. Generate review text
4. Synthesize natural-sounding human speech from text with the help of Amazon Polly (*amazon_polly.py*)
5. Download hotel images from Booking.com
6. Generate a slideshow and add a speech to it
7. Render and save the video

## 3. Upload videos on YouTube
*upload.py* and *runner.py* store the code for the video uploading. To set up auto-uploading I modify the script written by [linouk23](https://github.com/linouk23/youtube_uploader_selenium). It uses Selenium headless browser. For my purposes I:
1. Changed script path on YouTube.com
2. Add cookies downloader
3. Add log-in via cookies

Because it is too hard to go through Google bot detection with a simple email&password log in I decided to log in via cookies. It works but you have to be really careful with your IP. I recommend using only one proxy for one YouTube channel.

Cookies can be downloaded with the help of *cookies_getter.py* and will be stored in JSON format.

## To sum up
There is also an SQLite database and simple logger implemented in this project. I also added Selenium.exe and Geckodriver.exe files to the repository.

In /data directory you can see videos that can be created with the help of this script.

And it is one of the channels I used to upload such videos: https://www.youtube.com/channel/UCuoo5uULgSHW7dU8fhOzSXg
