"""
A file containing the functionality of all of the possible mutations in the code
Written by Alex O'Neill (z5359415) and Dylan Ngo (z5308205)
"""

import sys
import mutations
import queries
sys.path.insert(0, 'package/')
import pytest



@pytest.fixture
def test_basic_weather():
    dictionary = mutations.create_weather_resolver(1, 1, "Newcastle Nobbys", 2)
    assert dictionary['success'] == True
    assert dictionary['weathers'][0]['id'].startswith('94774')
    assert dictionary['weathers'][0]['location'] == 'Newcastle Nobbys'

def test_basic_weather_error():
    dictionary = mutations.create_weather_resolver(1, 1, "Fake Location", 2)
    assert dictionary['success'] == False
    assert dictionary['errors'] ==  ["Location does not exist"]

def test_basic_wind():
    dictionary = mutations.create_wind_resolver(1, 1, "Newcastle Nobbys")
    assert dictionary['success'] == True
    assert float(dictionary['wind_efficiency']) >= 0

def test_basic_wind_error():
    dictionary = mutations.create_wind_resolver(1, 1, "Fake Location")
    assert dictionary['success'] == False
    assert dictionary['errors'] ==  ["Location does not exist"]

def test_create_dictionary():
    dictionary = mutations.create_dictionary()
    assert "Bureau of Meteorology" in str(dictionary)

def test_is_float():
    float_check = mutations.is_float("1.0")
    assert float_check == True

def test_is_float_error():
    float_check = mutations.is_float("A")
    assert float_check == False

def test_import():
    data, loc_id = mutations.import_from_bom("Newcastle Nobbys")
    assert loc_id == '94774'
    assert str(data).startswith("{")

def test_queries():
    data = queries.list_locations_resolver(1,1,"A")
    assert "Albury" in str(data["locations"])

def test_queries_errors():
    data = queries.list_locations_resolver(1,1,1)
    assert data['success'] == False

'''This test file tests the pipeline'''
def test_pipe():
    '''Test that pytest and pylint are working'''
    assert 1 + 1 == 2