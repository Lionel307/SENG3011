"""
A file containing the functionality of all of the possible mutations in the code
Written by Alex O'Neill (z5359415)
"""
import sys
import json
from datetime import datetime
from ariadne import convert_kwargs_to_snake_case
import requests
sys.path.insert(0, 'package/')


def import_from_bom(location):
    """ Imports data from the Bureau of Meteorology """

    # Finds the ID of a location from a JSON list of NSW location names and IDS
    with open('nsw_locations.json', 'r', encoding='utf8') as locations:
        all_locations = json.loads(locations.read())
        location_id = all_locations[location]

    # Using the ID, go to the Bureau of Meteorology and return the JSON and ID
    link = "http://reg.bom.gov.au/fwo/IDN60801/IDN60801."+str(location_id)+".json"
    return json.loads(requests.get(link, timeout=10).text)["observations"], location_id


def create_dictionary():
    """ Creates the dictionary for the data_model """

    # A preset heading and format in accordance with the ADAGE 3.0 Data Model
    dictionary = {
        "data_source": "Bureau of Meteorology", 
        "dataset_type": "Weather Measurements", 
        "dataset_id": "http://unsw-seng3011-23t1-shared-dev.ap-southeast-2.amazonaws.com", 
        "time_object": {
            "timezone": "GMT+11"
        },
        "events": [

        ]
    }
    # Sets the timestamp to the current time and returns the dictionary
    dictionary["time_object"]["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return dictionary


def is_float(num):
    """ A function which checks if a number is a float or not """
    try:
        float(num)
        return True
    except ValueError:
        return False



@convert_kwargs_to_snake_case
def create_weather_resolver(obj, info, location, hours): # pragma: no cover
    """ A GraphQL based resolver which imports weather from the Bureau of Meteorology
    and returns the specified contents in two optional formats (A list of
    weather dictionaries or an ADAGE 3.0 Data Model) """

    # Imports data from the Bureau of Meteorology or returns an error
    # if an invalid location is input
    try:
        observations, location_id = import_from_bom(location)
        print(obj)
        print(info)
    except KeyError:
        payload = {
            "success": False,
            "errors": ["Location does not exist"]
        }
        return payload

    # Selects the data dictionary from the JSON results
    datas = observations["data"]

    # Creates the format for the ADAGE 3.0 Data Model
    data_model = create_dictionary()

    # A list to store all of the attained weather information
    weathers = []

    # For each weather observation
    for data in datas:
        # If it is an hourly observation and within the past "hours"
        # number of hours
        if data["local_date_time_full"][10:12]=="00" and len(weathers) < hours:

            # Creates an event for storing in the Adage
            event = {
                "time_object": { 
                    "duration": 1, 
                    "duration_unit": "hour", 
                    "timezone": "GMT+11" 
                },
                "event_type": "Observations"            
            }
            # Creates an event timestamp using the date_time of the observation
            event["time_object"]["timestamp"] = data["local_date_time_full"][0:4] \
                + "-"+data["local_date_time_full"][4:6] + "-" \
                + data["local_date_time_full"][6:8] + " " \
                + data["local_date_time_full"][8:10] + ":" \
                + data["local_date_time_full"][10:12] + ":" \
                + data["local_date_time_full"][12:14] + ".0000000"

            # Creates a weather dictionary using parameters from the BOM import
            weather = {
                "id": str(location_id)+data["local_date_time_full"],
                "location": location,
                "date": data["local_date_time_full"][6:8] + "-" \
                        + data["local_date_time_full"][4:6] + "-" \
                        + data["local_date_time_full"][2:4],
                "time": data["local_date_time_full"][8:10] + ":" \
                        + data["local_date_time_full"][10:12] + ":" \
                        + data["local_date_time_full"][12:14],
                "temperature": data["air_temp"],
                "apparent_temp": data["apparent_t"],
                "dew_point": data["dewpt"],
                "relative_humidity": data["rel_hum"],
                "wind_direction": data["wind_dir"],
                "wind_speed": data["wind_spd_kmh"],
                "rain": float(data["rain_trace"]) if is_float(data["rain_trace"]) else 0.0
            }

            # Adds weather as an event attribute and appends the event to the
            # list of events
            event["attribute"] = weather
            data_model["events"].append(event)
        
            # Appends weather to the list of weathers
            weathers.append(weather)

    # Returns a payload with relevant data and showing success
    payload = {
        "success": True,
        "weathers": weathers,
        "data_model": json.dumps(data_model)
    }
    return payload


@convert_kwargs_to_snake_case
def create_wind_resolver(obj, info, location):
    """ Returns the approximated wind efficiency at a location """

    # Checks for past 24 hours
    hours = 24

    # Create a list of wind data
    wind_list = []

    # Imports data from the Bureau of Meteorology or returns an error
    # if an invalid location is input
    try:
        observations, location_id = import_from_bom(location)
        print(location_id)
        print(obj)
        print(info)
    except KeyError:
        payload = {
            "success": False,
            "errors": ["Location does not exist"]
        }
        return payload

    # Selects the data dictionary from the JSON results
    datas = observations["data"]

    # For each of the past 24 hourly data point in the data, add it to the list
    for data in datas:
        if data["local_date_time_full"][10:12]=="00" and len(wind_list) < hours:
            wind_list.append(data["wind_spd_kmh"])
    # Get current and max windspeed from the list
    current_windspeed = wind_list[0]
    max_windspeed = max(wind_list)

    # This error-checks in the rare scenario where max_windspeed = 0.
    # In this scenario, current windspeed would also be 0, and so setting
    # max_windspeed to 1.0 will result in a value of 0, which is correct.
    if max_windspeed == 0.0:
        max_windspeed = 1.0

    # Uses a formula to check what the wind efficiency is at the current time.
    actual_on_expected = (0.1785*current_windspeed)/(0.3024*max_windspeed)

    # Returns the wind efficiency
    payload = {
        "success": True,
        "wind_efficiency": str(actual_on_expected)
    }
    return payload
