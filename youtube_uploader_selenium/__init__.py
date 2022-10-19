"""This module implements uploading videos on YouTube via Selenium using metadata JSON file
	to extract its title, description etc."""
import os
from typing import DefaultDict, Optional
from selenium_firefox.firefox import Firefox, By, Keys
from collections import defaultdict
import json
import time
from conf import COOKIES_PATH, LOGS_DIR
from .Constant import *
from pathlib import Path
from logger import logger
import platform
from selenium.common.exceptions import ElementClickInterceptedException


# Create custom exception for case if uploading limit error raise
class UploadLimitException(Exception):
    pass


# Get cookies for entering your account. If you have some problems use screenshots to see what is wrong
def cookies_getter(login, password, cookies_name, proxy_ip, proxy_port):
    browser = Firefox(COOKIES_PATH, str(Path.cwd()), headless=False, host=proxy_ip,
                      port=proxy_port, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                  'Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59')
    logger.debug(f'{cookies_name} - {proxy_ip}:{proxy_port}')
    browser.get('https://youtube.com')
    logger.debug('Youtube.com opened')
    time.sleep(Constant.USER_WAITING_TIME)
    time.sleep(3)
    # browser.find(By.XPATH, '//*[@id="openid-buttons"]/button[1]').click()
    logger.debug('Clicking sign in button on top right corner')
    browser.find(By.XPATH, Constant.YOUTUBE_SIGNIN_BUTTON).click()
    time.sleep(Constant.USER_WAITING_TIME)
    # browser.driver.save_screenshot('screen2.png')
    logger.debug('Attempting to fill email')
    browser.find(By.XPATH, Constant.GOOGLE_SIGNIN_CARD_EMAIL).send_keys(login)
    time.sleep(Constant.USER_WAITING_TIME)
    logger.debug('Attempting to click next')
    browser.find(By.XPATH, Constant.GOOGLE_SIGNIN_CARD_EMAIL_NEXT).click()
    time.sleep(Constant.USER_WAITING_TIME)
    logger.debug('Attempting to fill password')
    # browser.driver.save_screenshot('screen3.png')
    browser.find(By.XPATH, Constant.GOOGLE_SIGNIN_CARD_PASSWORD).send_keys(password)
    time.sleep(Constant.USER_WAITING_TIME)
    logger.debug('Try to login')
    browser.find(By.XPATH, Constant.GOOGLE_SIGNIN_CARD_PASSWORD_NEXT).click()
    time.sleep(Constant.USER_WAITING_TIME)
    logger.debug('Coming back to youtube.com')
    browser.get(Constant.YOUTUBE_URL)
    time.sleep(Constant.USER_WAITING_TIME)
    with open(os.path.join(COOKIES_PATH, f'{cookies_name}.json'), 'w') as filehandler:
        json.dump(browser.driver.get_cookies(), filehandler)
    logger.debug('Cookies downloaded')
    time.sleep(Constant.USER_WAITING_TIME)
    browser.driver.quit()
    logger.debug('Browser is closed')


def load_metadata(metadata_json_path: Optional[str] = None) -> DefaultDict[str, str]:
    if metadata_json_path is None:
        return defaultdict(str)
    with open(metadata_json_path, encoding='utf-8') as metadata_json_file:
        return defaultdict(str, json.load(metadata_json_file))


class YouTubeUploader:
    """A class for uploading videos on YouTube via Selenium using metadata JSON file
	to extract its title, description etc"""

    def __init__(self, cookies_name: str, video_path: str, proxy_ip: Optional[str] = None,
                 proxy_port: Optional[int] = None, metadata_json_path: Optional[str] = None,
                 thumbnail_path: Optional[str] = None) -> None:
        self.video_path = video_path
        self.thumbnail_path = thumbnail_path
        self.metadata_dict = load_metadata(metadata_json_path)
        self.cookies_path = os.path.join(COOKIES_PATH, f'{cookies_name}.json')
        current_working_dir = str(Path.cwd())
        # You can set headless=True if you want to see the browser
        self.browser = Firefox(COOKIES_PATH, current_working_dir, headless=False, host=proxy_ip, port=proxy_port,
                               user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; '
                                          'x64; rv:77.0) Gecko/20100101 Firefox/77.0')
        self.logger = logger
        # self.logger.setLevel(logging.DEBUG)  # set level of logger
        self.__validate_inputs()

        self.is_mac = False
        if not any(os_name in platform.platform() for os_name in ["Windows", "Linux"]):
            self.is_mac = True

    def __validate_inputs(self):
        if not self.metadata_dict[Constant.VIDEO_TITLE]:
            self.logger.warning(
                "The video title was not found in a metadata file")
            self.metadata_dict[Constant.VIDEO_TITLE] = Path(
                self.video_path).stem
            self.logger.warning("The video title was set to {}".format(
                Path(self.video_path).stem))
        if not self.metadata_dict[Constant.VIDEO_DESCRIPTION]:
            self.logger.warning(
                "The video description was not found in a metadata file")

    def upload(self):
        try:
            self.__login()
            return self.__upload()
        except Exception as e:
            print(e)
            self.__quit()
            raise

    def __login(self):
        self.logger.debug('Open youtube.com')
        self.browser.get(Constant.YOUTUBE_URL)
        time.sleep(Constant.USER_WAITING_TIME)
        self.logger.debug('Delete all cookies')
        self.browser.driver.delete_all_cookies()
        time.sleep(Constant.USER_WAITING_TIME)
        self.logger.debug('Insert cookies')
        with open(self.cookies_path, 'r') as inputdata:
            cookies = json.load(inputdata)
        for cookie in cookies:
            self.browser.driver.add_cookie(cookie)
        self.logger.debug('Refresh youtube.com page')
        time.sleep(Constant.USER_WAITING_TIME)
        self.browser.refresh()


    def __write_in_field(self, field, string, select_all=False):
        field.click()

        time.sleep(Constant.USER_WAITING_TIME)
        if select_all:
            if self.is_mac:
                field.send_keys(Keys.COMMAND + 'a')
            else:
                field.send_keys(Keys.CONTROL + 'a')
            time.sleep(Constant.USER_WAITING_TIME)
        field.send_keys(string)

    def __upload(self) -> (bool, Optional[str]):
        # self.browser.get(Constant.YOUTUBE_URL)
        time.sleep(Constant.USER_WAITING_TIME)
        self.logger.debug('Go to youtube.com/upload')
        self.browser.get(Constant.YOUTUBE_UPLOAD_URL)
        time.sleep(Constant.USER_WAITING_TIME)
        if self.browser.find(By.XPATH, '//*[@id="html-body"]/ytcp-warm-welcome-dialog',
                             timeout=2):  # close welcome popup
            self.browser.find(By.XPATH, '//*[@id="dismiss-button"]/div').click()
            self.logger.debug('Welcome hint is closed')
            time.sleep(Constant.USER_WAITING_TIME)
        absolute_video_path = str(Path.cwd() / self.video_path)
        self.logger.debug('Start attaching video')
        try:
            self.browser.find(By.XPATH, Constant.INPUT_FILE_VIDEO, timeout=15).send_keys(
                absolute_video_path)
            self.logger.debug('Attached video {}'.format(self.video_path))
        except (ElementClickInterceptedException, TypeError) as e:
            time.sleep(4)
            self.browser.driver.save_screenshot(os.path.join(LOGS_DIR, 'error_screenshot.png'))
            self.logger.error(f'Error while attaching video\n{e}')
            self.__quit()
        try:
            title_field = self.browser.find(By.ID, Constant.TEXTBOX, timeout=15)
            self.__write_in_field(
                title_field, self.metadata_dict[Constant.VIDEO_TITLE], select_all=True)
            self.logger.debug('The video title was set to \"{}\"'.format(
                self.metadata_dict[Constant.VIDEO_TITLE]))
        except (ElementClickInterceptedException, TypeError, AttributeError) as e:
            if self.browser.find(By.XPATH, "//*[contains(text(), 'Загрузка недоступна.')]", timeout=7):
                self.logger.error('Uploading limit error')
                self.browser.driver.save_screenshot(os.path.join(LOGS_DIR, 'uploading_limit_error.png'))
                self.__quit()
                raise UploadLimitException
            time.sleep(3)
            self.browser.driver.save_screenshot(os.path.join(LOGS_DIR, 'error_screenshot.png'))
            self.logger.error(f'Error while setting title\n{e}')
            self.__quit()
        video_description = self.metadata_dict[Constant.VIDEO_DESCRIPTION]
        video_description = video_description.replace("\n", Keys.ENTER);
        if video_description:
            try:
                description_field = self.browser.find_all(By.ID, Constant.TEXTBOX, timeout=15)[1]
                self.__write_in_field(description_field, video_description, select_all=True)
                self.logger.debug('Description filled.')
            except (ElementClickInterceptedException, TypeError, AttributeError) as e:
                if self.browser.find(By.XPATH, "//*[contains(text(), 'Загрузка недоступна.')]", timeout=7):
                    self.logger.error('Uploading limit error')
                    self.browser.driver.save_screenshot(os.path.join(LOGS_DIR, 'uploading_limit_error.png'))
                    self.__quit()
                    raise UploadLimitException
                time.sleep(3)
                self.browser.driver.save_screenshot(os.path.join(LOGS_DIR, 'error_screenshot.png'))
                self.logger.error(f'Error while setting title\n{e}')
                self.__quit()

        if self.thumbnail_path is not None:
            absolute_thumbnail_path = str(Path.cwd() / self.thumbnail_path)
            time.sleep(Constant.USER_WAITING_TIME)
            try:
                self.browser.find(By.XPATH, Constant.INPUT_FILE_THUMBNAIL).send_keys(absolute_thumbnail_path)
                self.logger.debug('Attached thumbnail {}'.format(self.thumbnail_path))
            except (ElementClickInterceptedException, TypeError) as e:
                time.sleep(4)
                self.browser.driver.save_screenshot(os.path.join(LOGS_DIR, 'error_screenshot.png'))
                self.logger.error(f'Error while attaching thumbnail\n{e}')
                self.__quit()
            time.sleep(Constant.USER_WAITING_TIME)

        # Not for kids options sets automatically so I commented this part of code

        # kids_section = self.browser.find(
        # 	By.NAME, Constant.NOT_MADE_FOR_KIDS_LABEL)
        # try:
        # 	self.browser.find(By.ID, Constant.RADIO_LABEL, kids_section).click()
        # except (ElementClickInterceptedException, TypeError) as e:
        # 	time.sleep(4)
        # 	self.browser.driver.save_screenshot('error_screenshot.png')
        # 	self.logger.error(f'Error while clicking children radiobutton\n{e}')
        # 	self.__quit()
        # self.logger.debug('Selected \"{}\"'.format(
        # 	Constant.NOT_MADE_FOR_KIDS_LABEL))

        # Advanced options
        self.browser.find(By.XPATH, Constant.MORE_BUTTON).click()
        self.logger.debug('Clicked MORE OPTIONS')

        tags_container = self.browser.find(By.XPATH,
                                           Constant.TAGS_INPUT_CONTAINER)
        tags_field = self.browser.find(
            By.ID, Constant.TAGS_INPUT, element=tags_container)
        self.__write_in_field(tags_field, ','.join(
            self.metadata_dict[Constant.VIDEO_TAGS]))
        self.logger.debug(
            'The tags were set to \"{}\"'.format(self.metadata_dict[Constant.VIDEO_TAGS]))

        # Set location based on given metadata
        location = self.metadata_dict[Constant.VIDEO_LOCATION]
        location_field = self.browser.find(By.XPATH, Constant.INPUT_LOCATION)
        self.__write_in_field(location_field, location, select_all=True)
        time.sleep(Constant.USER_WAITING_TIME)
        location_search_container = self.browser.find(By.XPATH, Constant.LOCATION_SEARCH_CONTAINER)
        location_search_1_result = self.browser.find(By.ID, Constant.LOCATION_1_RESULT,
                                                     element=location_search_container)
        location_search_1_result.click()
        self.logger.debug('Location added')
        time.sleep(Constant.USER_WAITING_TIME)

        # Set travel category to video
        category_field = self.browser.find(By.XPATH, Constant.INPUT_CATEGORY)
        category_field.click()
        time.sleep(Constant.USER_WAITING_TIME)
        self.browser.find(By.XPATH, Constant.CATEGORY_TRAVEL).click()
        self.logger.debug('Category added')
        time.sleep(Constant.USER_WAITING_TIME)

        self.browser.find(By.ID, Constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} one'.format(Constant.NEXT_BUTTON))

        self.browser.find(By.ID, Constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} two'.format(Constant.NEXT_BUTTON))

        self.browser.find(By.ID, Constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} three'.format(Constant.NEXT_BUTTON))
        public_main_button = self.browser.find(By.NAME, Constant.PUBLIC_BUTTON)
        self.browser.find(By.ID, Constant.RADIO_LABEL,
                          public_main_button).click()
        self.logger.debug('Made the video {}'.format(Constant.PUBLIC_BUTTON))

        video_id = self.__get_video_id()

        status_container = self.browser.find(By.XPATH,
                                             Constant.STATUS_CONTAINER)
        while True:
            in_process = status_container.text.find(Constant.UPLOADED) != -1
            if in_process:
                time.sleep(Constant.USER_WAITING_TIME)
            else:
                break

        done_button = self.browser.find(By.ID, Constant.DONE_BUTTON)

        # Catch error "File is a duplicate of a video you have already uploaded"
        if done_button.get_attribute('aria-disabled') == 'true':
            error_message = self.browser.find(By.XPATH,
                                              Constant.ERROR_CONTAINER).text
            self.logger.error(error_message)
            time.sleep(4)
            self.browser.driver.save_screenshot(os.path.join(LOGS_DIR, 'error_screenshot.png'))
            self.logger.error(f'Error video is not uploaded')
            return False, None

        done_button.click()
        self.logger.debug(
            "Published the video with video_id = {}".format(video_id))
        time.sleep(Constant.USER_WAITING_TIME)
        self.browser.get(Constant.YOUTUBE_URL)
        self.__quit()
        return True, video_id

    def __get_video_id(self) -> Optional[str]:
        video_id = None
        try:
            video_url_container = self.browser.find(
                By.XPATH, Constant.VIDEO_URL_CONTAINER)
            video_url_element = self.browser.find(By.XPATH, Constant.VIDEO_URL_ELEMENT,
                                                  element=video_url_container)
            video_id = video_url_element.get_attribute(
                Constant.HREF).split('/')[-1]
        except:
            self.logger.warning(Constant.VIDEO_NOT_FOUND_ERROR)
            pass
        return video_id

    def __quit(self):
        self.browser.driver.quit()
        logger.debug('Browser is closed')
