# coding: utf-8

import os
from twilio.twiml.voice_response import VoiceResponse


stage = os.getenv('STAGE')


def callcenterTwilioResponse():
    r = VoiceResponse()
    r.record(
        timeout=10,
        maxLength=180,
        playBeep=True,
        trim='trim-silence',
        recordingStatusCallback='/'+stage+'/callback',
        recordingStatusCallbackMethod='POST'
    )
    return str(r)


def record(event, context):
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/xml"
        },
        "body": callcenterTwilioResponse()
    }
    print(response)

    return response


if __name__ == "__main__":
    event = {}
    print(record(event, {}))
