import json
import datetime
import boto3
from contextlib import closing
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CHUNK_SIZE = 1024
client = boto3.client('polly')


def handler(event, context):
    logger.info('received api gateway event: %s', event)

    path = ''
    if 'pathParameters' in event and event['pathParameters'] is not None:
        path = event['pathParameters'].get('proxy', '')
        logging.info('received request for %s', path)


    # Convert text to speech
    text = 'Welcome to space needle!'
    #TODO: figure out how to use application/x-json-stream
    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        VoiceId='Emma'
    )

    # Read audio data out of response stream from Polly
    audio = None
    if "AudioStream" in response:
        with closing(response.get("AudioStream")) as auto_closing_audio_stream:
            audio = auto_closing_audio_stream.read()

    # Convert to base64 string since Lambda's response is JSON
    base64_audio = base64.b64encode(audio).decode('ascii')

    headers = {}
    if 'stream' in path:
        response_body = json.dumps(base64_audio)
        headers = {'Content-Type': 'audio/mpeg'}
    else:
        response_body = json.dumps({
            'audio': {
                'data': base64_audio,
                'format': 'mp3',
                'encoding': 'base64'
            }
        })
        headers = {'Content-Type': 'application/json'}

    return {
        'statusCode': 200,
        'body': response_body,
        'headers': headers
    }
