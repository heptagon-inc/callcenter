# coding: utf-8

import json
import urllib
from callcenter import Rec, File, S3, Speech, Sqs, Slack
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

rec = Rec()
file = File()
s3 = S3()
speech = Speech()
sqs = Sqs()
slack = Slack()


def record(event, context):
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/xml"
        },
        "body": rec.response_xml()
    }
    print(response)
    return response


def callback(event, context):
    query_params = event['body']
    params = urllib.parse.parse_qs(query_params)
    recordingUrl = params['RecordingUrl'][0]
    filename = recordingUrl.split('/')[-1] + '.wav'
    file.move(recordingUrl, filename)
    response = {
        "statusCode": 200,
        "body": json.dumps({'result': True})
    }
    return response


def speech_to_text(event, context):
    key = event['Records'][0]['s3']['object']['key']
    content = s3.get_object(key)
    text = speech.to_text(content)
    sqs.send(text)
    print(text)
    return True


def notify_slack(event, context):
    message = event['Records'][0]['body']
    print(message)
    slack.post(message)
    return True


if __name__ == "__main__":
    event = {}
    print(record(event, {}))
