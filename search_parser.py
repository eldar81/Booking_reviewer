import requests
import re
import time
from bs4 import BeautifulSoup
from db_code import write_ids_links_prices
from logger import logger


# Generate search result link
# Before use check if there are no changes in URL parameters
# Only hotels, only 3,4,5 stars, sorted by top reviewed
def link_generator(dest_id: int, dest_type: str, currency: str):
    check_in = [12, 22, 2022]
    check_out = [12, 23, 2022]
    group_adults = 1
    group_children = 0
    dest_type = dest_type  # country or city
    order = "score"
    url = f"https://www.booking.com/searchresults.html?" \
          f"label=gen173nr-1FCAEoggI46AdIIVgEaMIBiAEBmAEhuAEXyAEM2AEB6AEB-AECiAIBqAI" \
          f"DuAKRp6-NBsACAdICJGY1MzBkODNkLTFhNDEtNGM1ZS04YjQzLTkzMjQ1OWYwMTA5NtgCBeACAQ;" \
          f"sid=a616a2c0ae51a4525b35bb40e6380d26;" \
          f"tmpl=searchresults;" \
          f"checkin_month={check_in[0]};" \
          f"checkin_monthday={check_in[1]};" \
          f"checkin_year={check_in[2]};" \
          f"checkout_month={check_out[0]};" \
          f"checkout_monthday={check_out[1]};" \
          f"checkout_year={check_out[2]};" \
          f"class_interval=1;" \
          f"dest_id={dest_id};" \
          f"dest_type={dest_type};" \
          f"from_sf=1;" \
          f"group_adults={group_adults};" \
          f"group_children={group_children};" \
          f"label_click=undef;" \
          f"nflt=ht_id%3D204%3Bclass%3D4%3Bclass%3D5%3Bclass%3D3;" \
          f"no_rooms=1;" \
          f"order={order};" \
          f"room1=A%2CA;" \
          f"sb_price_type=total;" \
          f"shw_aparth=1;" \
          f"slp_r_match=0;" \
          f"srpvid=3d7693f1be7d0081;" \
          f"top_ufis=1&;" \
          f"selected_currency={currency};"
    return url


def get_html(url, params=None):  # get html page from web
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0'
                      '.4664.45 Safari/537.36', 'accept': '*/*'}  # Imitates browser
    r = requests.get(url, headers=headers, params=params)
    return r

# Return amount of the whole hotels given by the booking.com
def get_num_of_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    num_of_results_str = soup.find('h1',
                               class_='e1f827110f d3a14d00da').get_text()
    num_of_results_str = num_of_results_str[num_of_results_str.find(':') + 1:]  # return text after ':'
    num_of_results_str = re.findall(r'\d+', num_of_results_str)
    num_of_results_int = ''
    for i in num_of_results_str:
        num_of_results_int = num_of_results_int + str(i)
    num_of_results_int = int(num_of_results_int)  # return only digits
    return num_of_results_int


# Return list of HTML elements (hotel's cards)
def get_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('a', class_='e13098a59f')
    return tags


# Return list of hotel's links
def get_links(tags):
    hotel_links = []
    for tag in tags:  # Return list of links on hotels
        hotel_links.append(tag.get('href'))
    return hotel_links


# Return list of hotels's ids
def get_hotel_ids(tags):
    hotel_ids = []
    for tag in tags:  # Return list of hotel ids
        hotel_ids.append(tag.get('href').partition('booking.com/hotel/')[2].partition('.en-gb.html?')[0])
    return hotel_ids


# Return list of hotel's prices
def get_price(html):
    hotel_prices = []
    soup = BeautifulSoup(html, 'html.parser')
    price_tags = soup.find_all('span', class_='fcab3ed991 bd73d13072')
    for tag in price_tags:
        price = tag.text
        price = [str(x) for x in price if x.isdigit()]
        price = int("".join(price))
        hotel_prices.append(price)
    return hotel_prices


# Write data to database
def write_db(hotel_ids, hotel_links, hotel_prices, currency):
    currency = f'{currency}'+' '
    list_of_currency = (currency * 25).rstrip()
    list_of_currency = list_of_currency.split()
    list_to_db = list(zip(hotel_ids, hotel_links, hotel_prices, list_of_currency))
    for hotel in list_to_db:
        write_ids_links_prices(hotel)


# Run parsing
def parse(dest_id: int, dest_type: str, currency: str):
    url = link_generator(dest_id, dest_type, currency)
    logger.info(f'Parsing link: {url}')
    html = get_html(url)
    if html.status_code == 200:
        last_offset = get_num_of_results(html.text)//25*25  # This part of code create list of offsets
        i = last_offset
        list_of_offsets = []
        while i >= 0:
            list_of_offsets.append(i)
            i -= 25
        list_of_offsets.reverse()

        count_hotels = 0
        for i, offset in enumerate(list_of_offsets):  # Cycle runs through pagination and collects links
            html = get_html(url, params={'offset': offset})  # get html
            hotel_links = get_links(get_tags(html.text))  # get links from html
            hotel_ids = get_hotel_ids(get_tags(html.text))  # get ids from html
            hotel_prices = get_price(html.text)
            write_db(hotel_ids, hotel_links, hotel_prices, currency)  # write links and ids to db
            count_hotels += len(hotel_ids)
            logger.info(f'{i+1}/{len(list_of_offsets)} pages are processed')
            time.sleep(0.25)  # sleep time between requests
        logger.info(f'Parsing is over. Finally: {count_hotels} links')
    else:
        logger.error("Booking doesn't respond")


if __name__ == "__main__":
    dest_type = input("Enter the type of destination (city, country): ")
    dest_id = int(input("Enter dest_id: "))
    currency = input("Enter currency (EUR, USD, RUB): ")
    parse(dest_id, dest_type, currency)
