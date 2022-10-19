class Constant:
    """A class for storing constants for YoutubeUploader class"""
    YOUTUBE_URL = 'https://www.youtube.com'
    YOUTUBE_STUDIO_URL = 'https://studio.youtube.com'
    YOUTUBE_UPLOAD_URL = 'https://www.youtube.com/upload'
    USER_WAITING_TIME = 1
    USER_WAITING_TIME_LONG = 20
    VIDEO_TITLE = 'title'
    VIDEO_DESCRIPTION = 'description'
    VIDEO_TAGS = 'tags'
    VIDEO_CATEGORY = 'category'
    VIDEO_LOCATION = 'location'
    DESCRIPTION_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/' \
                            'ytcp-uploads-details/div/ytcp-uploads-basics/ytcp-mention-textbox[2]'
    TEXTBOX = 'textbox'
    TEXT_INPUT = 'text-input'
    RADIO_LABEL = 'radioLabel'
    STATUS_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/' \
                       'div/div[1]/ytcp-video-upload-progress/span'
    NOT_MADE_FOR_KIDS_LABEL = 'VIDEO_MADE_FOR_KIDS_NOT_MFK'

    MORE_BUTTON = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog' \
                  '/div/ytcp-animatable[1]/ytcp-video-metadata-editor/div/div/ytcp-button/div'
    TAGS_INPUT_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog' \
                           '/div/ytcp-animatable[1]/ytcp-video-metadata-editor' \
                           '/div/ytcp-video-metadata-editor-advanced/div[3]' \
                           '/ytcp-form-input-container/div[1]/div[2]/ytcp-free-text-chip-bar/ytcp-chip-bar/div'

    TAGS_INPUT = 'text-input'
    NEXT_BUTTON = 'next-button'
    PUBLIC_BUTTON = 'PUBLIC'
    VIDEO_URL_CONTAINER = "//span[@class='video-url-fadeable style-scope ytcp-video-info']"
    VIDEO_URL_ELEMENT = "//a[@class='style-scope ytcp-video-info']"
    HREF = 'href'
    UPLOADED = 'Uploading'
    ERROR_CONTAINER = '//*[@id="error-message"]'
    VIDEO_NOT_FOUND_ERROR = 'Could not find video_id'
    DONE_BUTTON = 'done-button'
    INPUT_FILE_VIDEO = "//input[@type='file']"
    INPUT_FILE_THUMBNAIL = "//input[@id='file-loader']"

    YOUTUBE_SIGNIN_BUTTON = '//*[@id="buttons"]/ytd-button-renderer/a'
    GOOGLE_SIGNIN_CARD_EMAIL = '//*[@id="identifierId"]'
    GOOGLE_SIGNIN_CARD_EMAIL_NEXT = '//*[@id="identifierNext"]/div/button'
    GOOGLE_SIGNIN_CARD_PASSWORD = '//*[@id="password"]/div[1]/div/div[1]/input'
    GOOGLE_SIGNIN_CARD_PASSWORD_NEXT = '//*[@id="passwordNext"]/div/button'

    INPUT_LOCATION = "//*[@id='location']/ytcp-form-autocomplete/ytcp-dropdown-trigger/div/div[2]/input"
    LOCATION_SEARCH_CONTAINER = "//ytcp-text-menu[@id='search-results']"
    LOCATION_1_RESULT = 'text-item-2'
    INPUT_CATEGORY = "//ytcp-form-select[@id='category']"
    CATEGORY_TRAVEL = "//tp-yt-paper-item[@test-id='CREATOR_VIDEO_CATEGORY_TRAVEL']"

    BOOKING_ALL_DESTINATIONS_BUTTON = '//*[@id="searchboxInc"]/div[1]/div/div/div[1]/div[21]/button'
    BOOKING_COOKIES_ACCEPT_BUTTON = '//*[@id="onetrust-accept-btn-handler"]'
