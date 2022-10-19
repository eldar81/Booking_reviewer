from youtube_uploader_selenium import cookies_getter
from logger import logger

# Download cookies in JSON format to log in the channel
def get_cookies():
    login = input("Enter login: ")
    password = input("Enter password: ")
    proxy = input("Enter proxy (ip:port): ")
    proxy_ip = proxy.split(':')[0]
    proxy_port = int(proxy.split(':')[1])
    cookies_name = input("Enter the country of the channel: ").title()
    try:
        cookies_getter(login, password, cookies_name, proxy_ip, proxy_port)
        logger.info("Cookies downloaded")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    get_cookies()
