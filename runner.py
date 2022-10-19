from conf import VIDEO_PATH, METADATA_PATH, THUMBNAIL_PATH
from db_code import get_hotels_to_render, write_data_to_db
from editor import render, NoHotelPhotoException
from youtube_uploader_selenium import UploadLimitException
from upload import upload_video
import time
from logger import logger
from amazon_polly import AmazonPollyError

# Definitely should be just a dictionary in Keys.py ...
# But you can fill this function or write a dict
def define_proxy(country):
    proxy_ip = None
    proxy_port = None
    if country == 'Italy':
        proxy_ip = ''
        proxy_port = 1
    elif country == 'United Arab Emirates':
        proxy_ip = ''
        proxy_port = 1
    elif country == 'Egypt':
        proxy_ip = ''
        proxy_port = 1
    elif country == 'Turkey':
        proxy_ip = ''
        proxy_port = 1
    elif country == 'Russia':
        proxy_ip = ''
        proxy_port = 1
    elif country == 'France':
        proxy_ip = ''
        proxy_port = 1
    elif country == 'Germany':
        proxy_ip = ''
        proxy_port = 1
    elif country == 'Thailand':
        proxy_ip = ''
        proxy_port = 1
    elif country == 'Mexico':
        proxy_ip = ''
        proxy_port = 1
    elif country == 'Spain':
        proxy_ip = ''
        proxy_port = 1
    return proxy_ip, proxy_port


def start_uploading():
    country = input("Write channel's countries separated by commas: ").title()
    country_list = country.replace(", ", ",").split(',')
    n = int(input("How many videos you would like to upload to each channel: "))
    t0 = time.time()
    for country in country_list:
        proxy_ip, proxy_port = define_proxy(country)  # define proxy for country
        unupl_hotels = get_hotels_to_render(country)  # return all not uploaded hotels of given country from database
        logger.info(f'Country: {country}')
        logger.info(f'Proxy: {proxy_ip}:{proxy_port}')
        logger.info(f'Not posted hotels: {len(unupl_hotels)}')
        unupl_hotels = [item for t in unupl_hotels for item in t]  # morph list of tuples into list
        unupl_hotels_n = unupl_hotels[0:n]  # return chosen number of hotels
        logger.info(f'Hotels in the queue: {len(unupl_hotels_n)}')

        # Open browser and insert cookies
        for i, hotel in enumerate(unupl_hotels_n):
            logger.info(f'Processing {i+1}/{n} hotel: {hotel}')
            try:
                render(hotel)
            except NoHotelPhotoException:
                logger.warning('Hotel without photos. Go to the next one')
                # Future improvement: delete hotel from database
                continue
            except AmazonPollyError:
                logger.warning('AmazonPolly error. Go to the next one')
                # Future improvement: delete hotel from database
                continue

            # Start uploading videos to channel
            try:
                upload_video(country, VIDEO_PATH, proxy_ip, proxy_port, METADATA_PATH)
                write_data_to_db('uploaded', 1, hotel)
                logger.info(f'Hotel {hotel} is uploaded')
            except UploadLimitException:
                logger.error('Uploading limit reached')
                break
    t1 = time.time()
    logger.info(f"Work took {round(t1 - t0)//60} m. {round(t1 - t0)%60} s.")


if __name__ == "__main__":
    logger.info("Start working")
    start_uploading()
