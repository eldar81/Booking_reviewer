import requests
import time
from bs4 import BeautifulSoup
import concurrent.futures
import multiprocessing as mp
from db_code import get_links_from_db, write_whole_data_to_db
from logger import logger


# Majority of data is taken from desktop version of the site
def get_desktop_html(url, params=None):
    HEADERS_DESKTOP = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/96.0.4664.45 Safari/537.36', 'accept': '*/*'}  # Imitates desktop browser
    r = requests.get(url, headers=HEADERS_DESKTOP)
    # with open(os.path.join(PARSING_DIR, 'html_desk.html'), 'w', encoding='utf-8') as file:  # Write html in file
    #     file.write(r.text)

    return r


# However, description of hotel is possible to take only from mobile version of HTML
# 'etg' parameter opens description popup
def get_mobile_html(url, params=None):
    HEADERS_MOBILE = {'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36'
                                    ' (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
                      'accept': '*/*'}  # Imitates mobile browser
    r = requests.get(url, headers=HEADERS_MOBILE, params={'etg': 'hp_m_description_opened'})
    return r


# Before use check if there are no changes in HTML tags on booking.com
def get_desk_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    country = soup.select('li[data-google-track*="country"]')[0]\
        .find('a', class_='bui-link bui-link--primary bui_breadcrumb__link').text.strip()
    city = soup.select('li[data-google-track*="city"]')[0]\
        .find('a', class_='bui-link bui-link--primary bui_breadcrumb__link').text.strip()
    try:
        district = soup.select('li[data-google-track*="district"]')[0]\
            .find('a', class_='bui-link bui-link--primary bui_breadcrumb__link').text.strip()
    except:
        district = ''
    try:
        stars = len(soup.find('span', class_='fbb11b26f5 e23c0b1d74').find_all('span'))
    except:
        stars = ''
    try:
        rating = float(soup.find('div', class_='b5cd09854e d10a6220b4').get_text())
    except:
        rating = ''
    try:
        airport = soup.find('ul', class_='dc227fec5c d795cf7e54 f18d6175be')\
            .find('div', class_='b1e6dd8416 aacd9d0b0a').text.strip()  # get first airport from list of airports
    except:
        airport = ''
    try:
        airport_dist = float(
            soup.find('ul', class_='dc227fec5c d795cf7e54 f18d6175be')
                .find('div', class_='db29ecfbe2 c90c0a70d3').text.strip().replace(' km', '').replace(' m', ''))
    except:
        airport_dist = ''
    list_of_desk_data = [country, city, district, stars, rating, airport, airport_dist]
    return list_of_desk_data


# Before use check if there are no changes in HTML tags on booking.com
def get_mob_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    description = str(soup.find('div', id='hotel-desc-full').p)
    description = description.replace('<p>', '').replace('<br/>', '').replace('</p>', '')[1:-1]

    photo_list = []
    photo_1 = soup.find('div', id='hotel-photos').find('li', class_='swpg__item')['data-src']  # get first image
    photo_list.append(photo_1)
    photos = soup.find('div', id='hotel-photos')\
        .find_all('li', class_='swpg__item swpg__item--secondary')  # get all another images
    for photo in photos:
        link = photo['data-src']
        photo_list.append(link)
        if len(photo_list) == 30:  # stop parsing if it gets 30 photos
            break
    while len(photo_list) < 30:  # if got less append list with empty elements
        photo_list.append('')

    hotel = soup.find('span', class_='hp-header--title--text').get_text().strip()

    list_of_mob_data = [hotel, description]
    list_of_mob_data = list_of_mob_data + photo_list
    return list_of_mob_data


# Writes  content to data base
def write_content_to_db(link):
    hotel_link = link[0]
    html_desc = get_desktop_html(hotel_link)
    time.sleep(0.25)
    html_mob = get_mobile_html(hotel_link)
    list_of_whole_data = get_desk_content(html_desc.text) + get_mob_content(html_mob.text)
    list_of_whole_data.append(hotel_link)
    write_whole_data_to_db(list_of_whole_data)
    with _COUNTER.get_lock():
        _COUNTER.value += 1
        print(_COUNTER.value, end=' ')


# Allows count processed hotels in console
def init_globals(counter):
    global _COUNTER
    _COUNTER = counter


# Run parsing in multithreading mode
def parse():
    t0 = time.time()
    counter = mp.Value('i', 0)
    links = get_links_from_db()  # return unparsed hotels
    logger.info(f"Отелей в очереди: {len(links)}")
    max_threads = 20
    threads = min(max_threads, len(links))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads,
                                               initializer=init_globals, initargs=(counter,)) as executor:
        for _ in executor.map(write_content_to_db, links):
            pass
    print()
    t1 = time.time()
    logger.info(f"Парсинг занял {round(t1 - t0, 2)} секунд.")


if __name__ == "__main__":
    parse()
