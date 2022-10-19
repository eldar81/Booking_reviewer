# Automated hotel reviewer
This program automatically:
1. Parse hotel data from Booking.com and store it in SQLite database
2. Generate video reviews on hotels out from this data
3. Upload videos to YouTube via Selenium webdriver

## 1. Parsing Booking.com
Parser devided into 2 files *search_parser.py* and *hotel_parser.py*

### Search_parser.py
Search_parser.py parse search results based on the request you send. Via URL parameters you can specify search request as you do it on booking webpage. For example, you can choose: city or country you are searching, only 4-starts hotels, currency and even sort mode.
Script collects all the hotel from the search results and store them in database. On this phase you have:
- Hotel id
- URL
- Price
- Currency

*Be sure to set up correct chech-in and chech-out dates*

### Hotel_parser.py
Hotel_parser.py goes through the database and update missing information:
- Hotel name
- Country
- City
- District
- Stars
- Rating
- Hearest airport
- Distance from an airport
- Photo's URLs (up to 30)
- Hotel description

To increase spead multithreading is implemented with the help of concurrent.futures library.

*Before use check if there are no changes in HTML tags on booking.com*

## 2. Generate videos
Video creation is set up in *editor.py* file.

To automatically generate videos moviepy library which is based on FFMPEG module is used.
Process devided into 7 parts:
1. Taking parsed hotel's data from database
2. Generate JSON file with metadata for future video uploading
3. Generate review text
4. Synthesize natural-sounding human speech from text with the help of Amazon Polly (*amazon_polly.py*)
5. Download hotel images from Booking.com
6. Generate slideshow and add speech to it
7. Render and save the video

## 3. Upload videos on YouTube
*upload.py* and *runner.py* store the code for video uploading. To set up auto-uploading I modify script written by [linouk23](https://github.com/linouk23/youtube_uploader_selenium). It uses Selenium headless browser. For my purposes I:
1. Changed path script do on YouTube.com
2. Add cookies downloader
3. Add log in via cookies

Because it is too hard to go through Google bot detection with simple email&password log in I decided to log in via cookies. It works but you have to be really careful with your IP. I recommend to use only one proxy for one YouTube channel.

Cookies can be downloaded with the help of *cookies_getter.py* and will be stored in JSON format.

## To sum up
There is also SQLite database and simple logger implemented in this project. I also added Selenium.exe and Geckodriver.exe files in repository.

In /data directory you can see video which can be created with the help of this script.

And it it one of the channel I used to upload such videos: https://www.youtube.com/channel/UCuoo5uULgSHW7dU8fhOzSXg
