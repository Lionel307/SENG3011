"""
The service that allows for a user to save their data to the API
Written by Alex O'Neill (z5359415)
"""

import sys
sys.path.insert(0, 'package/')
import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
def handler(event, context):
    """ Allows users to save data by reusing the CreateWeather schema """
    try:
        # Loads data from JSON input
        data = json.loads((event)['body'])

        # Sends properly formatted GraphQL to our weather API 
        link = "https://5qmp4gs3ud.execute-api.ap-southeast-2.amazonaws.com/F12A_PAPA/weather"
        graphql = """\"mutation CreateWeather {\\n    createWeather(location: \\"Cape Byron\\", hours:5) {\\n   success\\n   errors\\n    data_model\\n        }\\n}\"""".replace("Cape Byron", data["location"]).replace("5", str(data["hours"]))
        query = """{ "query" : """+graphql+"""}"""
        request = requests.post(link, json=json.loads(query), timeout=10)
        req = request.text
        status = request.status_code
        print("THERE")
        if status != 200:
            return {
                "statusCode": status,
                "body": str(req),
                "headers": {
                    "Content-Type": "application/json",
                },
            }
        print("GOES HERE")
        # Extracts the data model from our weather API
        result = eval(req)["data"]["createWeather"]["data_model"]

        # Uses F14A_SIERRA's lovely upload service to upload our data to the S3 Bucket
        verify = requests.post('https://afzpve4n13.execute-api.ap-southeast-2.amazonaws.com/F14A_SIERRA/upload',json=json.loads(result), headers={'Authorization': event['headers']['authorization']})
        # Returns result of sending
        status = verify.status_code
        if status == 403:
            status = 401
        return {
            "statusCode": status,
            "body": str(verify.text),
            "headers": {
                "Content-Type": "application/json",
            },
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": '{"status":"Server error"}',
            "headers": {
                "Content-Type": "application/json",
            },
        }
