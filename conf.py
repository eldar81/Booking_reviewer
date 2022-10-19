import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
VIDEO_DIR = os.path.join(DATA_DIR, "video")
PARSING_DIR = os.path.join(DATA_DIR, 'parsing')
TEMP_FILES = os.path.join(VIDEO_DIR, "temporary files")
TEMP_IMGS = os.path.join(TEMP_FILES, "images")
PERM_FILES = os.path.join(VIDEO_DIR, "permanent files")
OUTPUT_VIDEO = os.path.join(VIDEO_DIR, 'output video')
VIDEO_PATH = os.path.join(OUTPUT_VIDEO, 'video.mp4')
METADATA_PATH = os.path.join(OUTPUT_VIDEO, 'meta.json')
THUMBNAIL_PATH = os.path.join(OUTPUT_VIDEO, 'thumbnail.jpg')
COOKIES_PATH = os.path.join(BASE_DIR, "cookies")

REFERRAL_LINK1 = "Your referral link 1"
REFERRAL_LINK2 = "Your referral link 2"
REFERRAL_LINK3 = "Your referral link 3"
REFERRAL_LINK4 = "Your referral link 4"
