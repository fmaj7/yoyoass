import json
import datetime
import boto3
from contextlib import closing
import base64

CHUNK_SIZE = 1024
client = boto3.client('polly')

def handler(event, context):
    data = {
        'output': 'Hello World, yoyoasses',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    #TODO: figure out how to use application/x-json-stream
    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text='Welcome to space needle!',
        VoiceId='Emma'
    )
    print("polly response")
    print(response)

    audio = None
    if "AudioStream" in response:
        with closing(response.get("AudioStream")) as auto_closing_audio_stream:
            audio = auto_closing_audio_stream.read()

    base64_audio = base64.b64encode(audio).decode('ascii')

    return {
        'statusCode': 200,
        'body': {
            "audio": {
                "data": base64_audio,
                "format": "mp3",
                "encoding": "base64"
            }
        },
        'headers': {'Content-Type': 'application/json'}
    }
