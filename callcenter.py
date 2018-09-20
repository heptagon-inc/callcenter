# coding: utf-8


import os
import requests
import boto3
from twilio.twiml.voice_response import VoiceResponse


stage = os.getenv('STAGE')
bucket_name = os.getenv('BUCKET_NAME')


class Rec():
    def __init___(self):
        pass

    def response_xml(self):
        response = VoiceResponse()
        response.record(
            timeout=10,
            maxLength=180,
            playBeep=True,
            trim='trim-silence',
            recordingStatusCallback='/' + stage + '/callback',
            recordingStatusCallbackMethod='POST'
        )
        return str(response)


class File():
    def __init__(self):
        pass

    def download(self, url):
        response = requests.get(url)
        return response.content

    def upload(self, key, data):
        s3 = boto3.client('s3')
        s3.upload_fileobj(data, bucket_name, key)

    def remove(self):
        # remove from twilio storage
        pass

    def move(self, url, key, data):
        content = self.download(url)
        self.upload(key, data)
        self.remove()
