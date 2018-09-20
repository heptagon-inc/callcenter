# coding: utf-8


import json
import os
import requests
import boto3
from twilio.twiml.voice_response import VoiceResponse, Say
from google.cloud import speech
from google.cloud.speech import types


stage = os.getenv('STAGE')
bucket_name = os.getenv('BUCKET_NAME')
sqs_queue_url = os.getenv('SQS_QUEUE_URL')
slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')


class Rec():
    def __init___(self):
        pass

    def response_xml(self):
        response = VoiceResponse()
        response.say(
            '　ピーっという発信音の後、お問い合わせ内容をお申し付けください。',
            voice='alice',
            language='ja-JP')
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
        return s3.put_object(
            Body=data,
            Bucket=bucket_name,
            Key=key)
        # return s3.upload_fileobj(data, bucket_name, key)

    def remove(self):
        # remove from twilio storage
        pass

    def move(self, url, key):
        content = self.download(url)
        self.upload(key, content)
        self.remove()
        return True


class S3():
    def __init__(self):
        pass

    def get_object(self, key):
        s3 = boto3.client('s3')
        response = s3.get_object(
            Bucket=bucket_name,
            Key=key)
        return response['Body'].read()


class Speech():
    def __init__(self):
        pass

    def to_text(self, content):
        client = speech.SpeechClient()
        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(language_code='ja-JP')
        response = client.recognize(config, audio)
        r = []
        for result in response.results:
            r.append(result.alternatives[0].transcript)
        return '. '.join(r)


class Sqs():
    def __init__(self):
        pass

    def send(self, message):
        sqs = boto3.client('sqs')
        sqs.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=(message))
        return True


class Slack():
    def __init__(self):
        pass

    def post(self, message):
        payload = {"text": message}
        data = json.dumps(payload)
        requests.post(slack_webhook_url, data)
