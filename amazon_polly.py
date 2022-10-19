import os
import boto3
import botocore.exceptions
from conf import TEMP_FILES
from Keys import AWSSecretKey, AWSAccessKeyId
from logger import logger


class AmazonPollyError(Exception):
    pass


def polly(text):
    try:
        polly_client = boto3.Session(
                        aws_access_key_id=AWSAccessKeyId,
                        aws_secret_access_key=AWSSecretKey,
                        region_name='us-west-2').client('polly')
        response = polly_client.synthesize_speech(
            VoiceId='Matthew',
            OutputFormat='mp3',
            Text=text,
            Engine='neural')

        file = open(os.path.join(TEMP_FILES, 'speech.mp3'), 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        logger.debug('Speech file is written')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'TextLengthExceededException':
            logger.error(f"Text is too long: {e}")
            raise AmazonPollyError
        else:
            logger.error(f"Unexpected error: {e}")
