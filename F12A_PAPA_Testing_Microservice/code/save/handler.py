"""
The service that allows for a user to save their data to the API
Written by Alex O'Neill (z5359415)
"""

import sys
sys.path.insert(0, 'package/')
import json
import requests

def handler(event, context):
    """ Allows users to save data by reusing the CreateWeather schema """
    try:
        # Loads data from JSON input
        data = json.loads((event)['body'])

        # Sends properly formatted GraphQL to our weather API 
        link = "https://afzpve4n13.execute-api.ap-southeast-2.amazonaws.com/F12A_PAPA/weather"
        graphql = """\"mutation CreateWeather {\\n    createWeather(location: \\"Cape Byron\\", hours:5) {\\n        data_model\\n        }\\n}\"""".replace("Cape Byron", data["location"]).replace("5", str(data["hours"]))
        query = """{ "query" : """+graphql+"""}"""
        req = requests.post(link, json=json.loads(query), timeout=10).text

        # Extracts the data model from our weather API
        result = eval(req)["data"]["createWeather"]["data_model"]

        # Uses F14A_SIERRA's lovely upload service to upload our data to the S3 Bucket
        verify = requests.post('https://afzpve4n13.execute-api.ap-southeast-2.amazonaws.com/F14A_SIERRA/upload',json=json.loads(result), headers={'Authorization': event['headers']['authorization']}).text

        # Returns result of sending
        return {
            "statusCode": 200,
            "body": str(verify),
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