import time
from logger import logger
from conf import METADATA_PATH, VIDEO_PATH
from youtube_uploader_selenium import YouTubeUploader
from typing import Optional

# This function uppload videos to the channel
def upload_video(cookies: str, video_path: str, proxy_ip: Optional[str] = None,
                 proxy_port: Optional[int] = None, metadata_path: Optional[str] = None,
                 thumbnail_path: Optional[str] = None) -> object:
    t0 = time.time()
    uploader = YouTubeUploader(cookies, video_path, proxy_ip, proxy_port, metadata_path, thumbnail_path)
    was_video_uploaded, video_id = uploader.upload()
    assert was_video_uploaded
    t1 = time.time()
    logger.info(f"Uploading took {round(t1 - t0, 2)} s.")

# upload_video('test', VIDEO_PATH, metadata_path=METADATA_PATH)