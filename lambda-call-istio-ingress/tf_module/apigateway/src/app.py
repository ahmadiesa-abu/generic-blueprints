# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
import json
import logging
import base64
from datetime import datetime

import sys
import subprocess

subprocess.call('pip install requests -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sys.path.insert(1, '/tmp/')
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logging.info(json.dumps(event, indent=2))
    queryString = event["queryStringParameters"]
    url = 'http://ad433e6da1dd9438cb8d9bf25b64b113-1003399247.eu-west-1.elb.amazonaws.com/ms1?name={0}'
    url = url.format(queryString.get("name", ""))
    response = requests.get(url).content.decode('utf-8')

    # eventObject["queryString"] = queryString
    if event["requestContext"]["httpMethod"] == "POST":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message ": response
            })
        }
    else:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message ": response
            })
        }
