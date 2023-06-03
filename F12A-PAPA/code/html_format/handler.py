"""
The service that allows for a user to save their data to the API
Written by Alex O'Neill (z5359415)
"""

import sys
sys.path.insert(0, 'package/')

from html_converter import html_converter
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
        link = "https://afzpve4n13.execute-api.ap-southeast-2.amazonaws.com/F12A_PAPA/weather"
        graphql = """\"mutation CreateWeather {\\n    createWeather(location: \\"Cape Byron\\", hours:5) {\\n   weathers{\\n    id\\n    location\\n    date\\n    time\\n    temperature\\n    apparent_temp\\n    dew_point\\n    relative_humidity\\n    wind_direction\\n    wind_speed\\n    rain}\\n    success\\n   errors\\n        }\\n}\"""".replace("Cape Byron", data["location"]).replace("5", str(data["hours"]))
        query = """{ "query" : """+graphql+"""}"""
        request = requests.post(link, json=json.loads(query), timeout=10)
        req = request.text
        status = request.status_code
        if status != 200:
            return {
                "statusCode": status,
                "body": str(req),
                "headers": {
                    "Content-Type": "application/json",
                },
            }
        # Extracts the data model from our weather API
        result = eval(req)["data"]["createWeather"]["weathers"][::-1]
        
        # Returns neatly formatted HTML to the results
        def_html = html_converter(result,data["location"],str(data["hours"]))
        
        return {
            "statusCode": 200,
            "body": def_html,
            "headers": {
                "Content-Type": "text/html;charset=UTF-8",
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