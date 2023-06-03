"""
A user friendly way of accessing the wind efficiency command
Written by Alex O'Neill (z5359415)
"""
import sys
sys.path.insert(0, 'package/')

import json
import requests
import logging
import newrelic.agent
from flagbase import FlagbaseClient, Config, Identity

logger = logging.getLogger()
logger.setLevel(logging.INFO)
newrelic.agent.initialize()
@newrelic.agent.lambda_handler()
def handler(event, context):
    """ Allows users to access the wind efficiency API without knowledge of GraphQL """
    print("Wind Handler Called")
    try:
        # Loads data from JSON input
        data = json.loads((event)['body'])

        # If you want to check wind efficiency at a location
        if "location" in data:
            # Sends properly formatted GraphQL to our weather API
            link = "https://5qmp4gs3ud.execute-api.ap-southeast-2.amazonaws.com/F12A_PAPA/weather"
            graphql = """\"mutation CreateWind {\\n    createWind(location: \\"Cape Byron\\") {\\n        wind_efficiency\\n        success\\n        errors\\n    }\\n}\"""".replace("Cape Byron", data["location"])
            query = """{ "query" : """+graphql+"""}"""
            
            # Extracts the wind results from our weather API
            request = requests.post(link, json=json.loads(query))
            req = request.text
            status = request.status_code
            
            # Returns result of the request
            result = eval(req)["data"]["createWind"]
            
        # Otherwise, if you want to manually add in windspeed,
        # then calculate wind efficiency
        elif "current_windspeed" in data and "max_windspeed" in data:
            actual_on_expected = (0.1785*float(data["current_windspeed"]))/(0.3024*float(data["max_windspeed"]))
            result = {
                'wind_efficiency': str(actual_on_expected),
                'success': True,
                'errors': None,
            }
            status = 200
        logger.info("Successful Wind efficiency")
        flagbase = FlagbaseClient(
        config=Config(
            server_key="sdk-server_ffad6de2-2312-42b4-b979-4974acdccd69",
            )
        )
        
        # user details might be pulled from your database
        user = Identity(
            "some-user-id",
            {"some-trait-key": "blue"}
        )

        # Implementing flagbase with new efficiency percentage feature
        show_feature = flagbase.variation("example-flag", user, "treatment")
        print(flagbase.context.get_raw_flags().get_flags())
        print(show_feature)
        if show_feature == "treatment":
            newrelic.agent.record_custom_event('CreateWindSuccess', {'WindResult': result})
            if result['wind_efficiency'] != None:
                result["efficiency_percentage"] = str(float(result['wind_efficiency'])*100)+"%"
            return {
                "statusCode": status,
                "body": json.dumps(result),
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json',
                },
            }
        else:
            newrelic.agent.record_custom_event('CreateWindDisabled', {'WindResult': result})
            return {
                "statusCode": status,
                "body": json.dumps(result),
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json',
                },
            }
    except Exception as e:
        newrelic.agent.record_custom_event('CreateWindError', {'Error': "Server error"})
        return {
            "statusCode": 500,
            "body": '{"status":"Server error"}',
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                'Access-Control-Allow-Origin':'*',
                'Content-Type':'application/json',
            },
        }