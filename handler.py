# coding: utf-8

import json
from callcenter import Rec, File

rec = Rec()
file = File()


def record(event, context):
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/xml"
        },
        "body": rec.response_xml()
    }
    return response


def callback(event, context):
    print(event)
    response = {
        "statusCode": 200,
        "body": json.dumps(event)
    }
    return response


if __name__ == "__main__":
    event = {}
    print(record(event, {}))
