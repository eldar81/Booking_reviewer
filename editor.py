import json
from fake_useragent import UserAgent
import random
import time
import requests
from moviepy.video.fx.scroll import *
from moviepy.video.fx.resize import *
from moviepy.audio.fx.audio_fadein import *
from moviepy.audio.fx.audio_fadeout import *
from moviepy.editor import *
import math
from amazon_polly import polly
from conf import TEMP_FILES, OUTPUT_VIDEO, PERM_FILES, TEMP_IMGS, METADATA_PATH, \
    REFERRAL_LINK1, REFERRAL_LINK2, REFERRAL_LINK3, REFERRAL_LINK4
from db_code import get_hotel_data_from_db, write_data_to_db, get_all_imgs
from logger import logger
from Keys import PROXY_LIST


# Create custom exception for case if there is no photos of the hotel
class NoHotelPhotoException(Exception):
    pass


# Use your proxy for requests to booking.com incase you have it
def get_ua_and_proxy():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    if len(PROXY_LIST) == 0:
        proxy_dict = None
        random_proxy = None
    else:
        random_proxy = random.choice(PROXY_LIST)
        proxy_dict = {
            "http": f"http://{random_proxy}",
            "https": f"http://{random_proxy}",
            "ftp": f"ftp://{random_proxy}"
        }
    return headers, proxy_dict


def render(hotel_id):
    # Getting all hotel's data from database
    logger.debug(f"Getting hotel data")
    hotel_data = get_hotel_data_from_db('id', hotel_id)
    country = hotel_data[0]
    city = hotel_data[1]
    district = hotel_data[2]
    hotel_name = hotel_data[3]
    short_hotel_name = hotel_name.split(' -')[0].strip().split(' |')[0].strip()
    stars = hotel_data[4]
    rating = hotel_data[5]
    if rating == '':
        rating = 'high'
    price = hotel_data[6]
    currency = hotel_data[7]
    if currency == 'EUR':
        currency = 'euro'
    elif currency == 'USD':
        currency = 'dollars'
    # airport = hotel_data[8]  # doesn't use
    # airport_dist = hotel_data[9]  # doesn't use
    description = hotel_data[10]

    # Create JSON file with metadata for video
    logger.debug("Creating metadata file")
    title = f'🏨 {short_hotel_name} Review 2022. {city}, {country}'
    if len(title) > 100:
        title = f'🏨 {short_hotel_name} Review 2022. {city}'
        if len(title) > 100:
            title = f'🏨 {short_hotel_name} Review 2022'
            if len(title) > 100:
                title = f'🏨 {short_hotel_name} Review'
                if len(title) > 100:
                    title = f'{short_hotel_name} Review'
    data_to_json = {
        "title": title,
        "description": f"🛌 Book {short_hotel_name}: {REFERRAL_LINK1}\n"
                       f"✈ Buy tickets to {city}: {REFERRAL_LINK2}\n"
                       f"🚗 Rent a car in {city} with $100 discount: {REFERRAL_LINK3}\n"
                       f"🏛 Find museums, shows and attractions in {city}: {REFERRAL_LINK4}\n\n"
                       f"Review of {short_hotel_name}. This is {stars} stars hotel located in {city}, {country}.",
        "tags": [short_hotel_name, f'{short_hotel_name} review', f'{short_hotel_name} {city}',
                 f'{short_hotel_name} {country}', f'{short_hotel_name} {stars}*'],
        "location": country
    }
    json_object = json.dumps(data_to_json)  # serializing json
    with open(METADATA_PATH, "w") as outfile:  # writing meta.json
        outfile.write(json_object)

    # Creating description text
    logger.debug("Creating speech text")
    greetings = ['Hello ladies and gentlemen! Today we are reviewing ', 'Hi everyone! Today we are looking at ',
                 'Hello there! Let me introduce you ', 'Hi there! Today I wanna show you ',
                 'Good day, ladies and gentlemen! Let me introduce you ']
    goodbye = ['I wish you all the best. Goodbye!', 'Have a nice day, bye!', 'See you in the next video. Goodbye!',
               'Choose your hotel wisely. Bye-bye!', 'Hope you will have a nice vacation. Goodbye!']
    if district == '':
        talk = f"{random.choice(greetings)}{short_hotel_name}. {stars} stars hotel with " \
               f"{rating} rating on booking.\n\n" + description + \
               f'\n\n{short_hotel_name} located in {district} area of beautiful {city}. ' \
               f'Room prices starts from {price} {currency}.\n\n' + \
               f'If you want to get more information or book {short_hotel_name} check the link in the description ' \
               f'of this video.\n' f'{random.choice(goodbye)}'  # Future improvement: add pauses to the speech
    else:
        talk = f"{random.choice(greetings)}{short_hotel_name}. " \
               f"{stars} stars hotel with {rating} rating on booking.\n\n" + description + \
               f'\n\n{short_hotel_name} located in beautiful {city}. Room prices starts from {price} ' \
               f'{currency}.\n\n' + f'If you want to get more information or book {short_hotel_name} check the link ' \
                                    f'in the description of this video.\n' \
                                    f'{random.choice(goodbye)}'  # Future improvement: add pauses to the speech

    # Create audio
    polly(talk)
    speech_path = os.path.join(TEMP_FILES, 'speech.mp3')
    speech = AudioFileClip(speech_path)
    speech_duration = speech.duration
    duration = int(speech_duration) + 5  # Add 5 seconds of silence in the end

    bg_sound_path = os.path.join(PERM_FILES, 'bg_music.mp3')
    bg_sound = AudioFileClip(bg_sound_path).set_duration(duration).volumex(0.1)  # Set up duration and decrease volume
    bg_sound = audio_fadein(bg_sound, 3)
    bg_sound = audio_fadeout(bg_sound, 3)

    audioclip = CompositeAudioClip([speech, bg_sound])  # Compose speech and background sound
    logger.debug("Audio is composed")

    # Create video
    logger.debug('Getting images links from database')
    image_duration = 5  # set slide duration
    all_imgs = list(filter(None, get_all_imgs(hotel_id)))
    need_imgs = math.ceil(duration / image_duration)  # get number of images needed for video

    # Download images of hotel
    n2 = 1
    dwnld_imgs = 0
    for link in all_imgs:  # download needed images
        if dwnld_imgs < need_imgs:
            if n2 >= 10:
                n1 = ''
            else:
                n1 = 0
            img_response = requests.get(link, headers=get_ua_and_proxy()[0], proxies=get_ua_and_proxy()[1])
            if img_response.status_code != 404:  # check if image still exists (error 404 checker)
                img_data = img_response.content  # get image
                with open(os.path.join(TEMP_IMGS, f'img{n1}{n2}.jpg'), 'wb') as handler:
                    handler.write(img_data)
                n2 += 1
                dwnld_imgs += 1
            time.sleep(0.25)
        else:
            break

    # If hotel don't have images function stops
    if dwnld_imgs == 0:
        logger.info("Hotel doesn't have images")
        raise NoHotelPhotoException
    logger.debug(f'{dwnld_imgs} images were downloaded')

    # Resize images
    logger.debug('Resizing images')
    list_imgs_names = os.listdir(TEMP_IMGS)  # get list of images names
    image_duration_upd = duration / dwnld_imgs  # update slide duration (in case there are less images than we need)
    all_images = []
    for image in list_imgs_names:  # create list of clips
        clip = (ImageClip(os.path.join(TEMP_IMGS, image))
                .set_duration(image_duration_upd)
                )
        w, h = clip.size  # Get height of image (booking vertical images height=768, horizontal images width=1024)
        if h > w:
            clip = resize(clip, width=1920)  # resize to full hd
            clip = scroll(clip, h=1080, w=1920, x_speed=0, y_speed=-15, x_start=0, y_start=h/1.5)  # add scroll effect
        else:
            clip = resize(clip, width=1920*1.2)
            clip = scroll(clip, h=1080, w=1920, x_speed=15, y_speed=0, x_start=0, y_start=h)
        all_images.append(clip)

    # Add title
    logger.debug("Adding title")
    hotel_title_dur = 8  # duration of hotel name text in the beginning
    txt_clip = TextClip(f"{hotel_name}", fontsize=120, color='white', font="Montserrat",  # creates title with hotel name
                        size=(1920*0.85, 1080*0.85), stroke_color='black', stroke_width=2,
                        method='caption', align='center')
    txt_clip = txt_clip.set_duration(hotel_title_dur).set_fps(24).set_position('center')

    # Create final video sequence
    # Here is the trick, I use different composing methods to improve render speed. One for first slides with next and
    # another for the rest of the video
    logger.debug("Creating final sequence")
    # return number of images meeded to create sequence with title
    n_of_imgs_for_compose_with_text = math.ceil(hotel_title_dur / image_duration_upd)
    # return list of clips needed to create first sequence
    first_imgs_for_txt = all_images[0:n_of_imgs_for_compose_with_text]
    # creates clip made of images for title sequence
    video1 = concatenate_videoclips(first_imgs_for_txt, method="chain")
    # create sequence with title
    video1_text = CompositeVideoClip([video1, txt_clip])
    video1_text_seq = [video1_text]
    # add all the other clips(images) to title sequence
    video1_text_seq.extend(all_images[n_of_imgs_for_compose_with_text:])
    # creates final sequence
    video_final = concatenate_videoclips(video1_text_seq, method="chain")
    # add audio to video
    video_final.audio = audioclip

    # Render video
    logger.debug("Start rendering")
    output_video = os.path.join(OUTPUT_VIDEO, "video.mp4")
    t0 = time.time()
    video_final.write_videofile(output_video, fps=24, threads=4, codec='h264', logger=None)
    write_data_to_db('rendered', 1, hotel_id)
    t1 = time.time()
    logger.info(f"Render took {round(t1 - t0, 2)} seconds.")

    logger.debug("Deleting image files")

    # Delete images after video is done
    for img in list_imgs_names:
        os.remove(os.path.join(TEMP_IMGS, img))
