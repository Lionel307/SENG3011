"""
A file containing the functionality of all of the possible queries in the code
Written by Alex O'Neill (z5359415)
"""

import sys
sys.path.insert(0, 'package/')

from ariadne import convert_kwargs_to_snake_case
import json

@convert_kwargs_to_snake_case
def list_locations_resolver(obj, info, name):
    """ A query to check all possible locations """
    try:
        # Finds all location names in NSW
        with open('nsw_locations.json', 'r', encoding='utf8') as locations:
            data = json.loads(locations.read())
        locations = [key for key, value in data.items()]
        locations.sort()
        print(obj)
        print(info)

        # Finds all locations starting with the string "name"
        new_locations = []
        for location in locations:
            if location.startswith(name.title()):
                new_locations.append(location)

        #  Returns a list of locations
        payload = {
            "success": True,
            "locations": new_locations
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload