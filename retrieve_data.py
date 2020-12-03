"""This module is used to retrieve external data"""


import requests
import json
import uk_covid19
from uk_covid19 import Cov19API, exceptions
import logging


def from_config(*args):
    """Used to retrieve values form configuration file"""
    with open('config.json') as json_file:
        data = json.load(json_file)
        for arg in args:
            try:
                data = data[arg]
            except KeyError:
                return
        return data


# defining logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(from_config('log_file', 'format'))
file_handler = logging.FileHandler(from_config('log_file', 'file_name'))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_covid():
    """Formatting requested covid data"""
    data_list, keys = request_covid()
    if data_list:
        # assigning variable values from requested data
        location = data_list[0][keys[0]]
        today_cases = data_list[0][keys[1]]
        total_cases = data_list[0][keys[2]]
        total_deaths = data_list[1][keys[3]]
        death_rate = int(data_list[1][keys[4]])
        per_change = int((int(today_cases) / int(data_list[1][keys[1]])) * 100)
        daily_report = ''
        if death_rate >= 50:
            daily_report = f'A notable change detected as rate of deaths within a month ' \
                           f'of positive tests reached {death_rate / 100.000}%. \n'
        daily_report += f'Today in {location}, {today_cases} new cases were recorded, ' \
                        f'a {per_change}% of yesterday\'s cases. \n'
        daily_report += f'A total of {total_cases} cases and ' \
                        f'{total_deaths} deaths have been recorded'
        return daily_report
    else:
        # logging the error if the request was not successful
        logger.error('COVID REPORT NOT RETRIEVED')


def get_news():
    """Formatting requested news data"""
    data_list = request_news()
    if data_list:
        articles = data_list['articles']
        return articles[0]['title']
    else:
        # logging the error if the request was not successful
        logger.error('NEWS REPORT NOT RETRIEVED')


def get_weather():
    """Formatting requested weather data"""
    data_list = request_weather()
    if data_list:
        # assigning variable values from requested data
        location = data_list['name']
        temp_list = data_list['main']
        weather_type = data_list['weather'][0]['description'].lower()
        visibility = int(data_list['visibility']) / 1000
        temp = []
        for temps in temp_list.values():
            temp.append(int(temps) - 273)
        return f'Today in {location} its {temp[0]}°C, ranging from {temp[1]} to {temp[2]}. ' \
               f'Weather type is {weather_type} and visibility is {visibility}km'
    else:
        # logging the error if the request was not successful
        logger.error('WEATHER REPORT NOT RETRIEVED')


def request_covid():
    """Requesting covid data"""
    location = from_config('retrieve', 'covid', 'location')
    data = from_config('retrieve', 'covid', 'data_type')
    api = Cov19API(filters=location, structure=data)
    try:  # checking if the request was successful
        retrieved = api.get_json()
        return retrieved['data'], list(data.keys())
    except uk_covid19.exceptions.FailedRequestError:
        return


def request_news():
    """Requesting news data"""
    base_url = from_config('retrieve', 'news', 'path')
    api_key = from_config('retrieve', 'news', 'key')
    country = from_config('retrieve', 'news', 'country')
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    try:  # checking if the request was successful
        response = requests.get(complete_url).json()
        if response['status'] == 'ok' and response['totalResults'] != 0:
            return response
    except json.decoder.JSONDecodeError:
        return


def request_weather():
    """Requesting weather data"""
    base_url = from_config('retrieve', 'weather', 'path')
    api_key = from_config('retrieve', 'weather', 'key')
    city_name = from_config('retrieve', 'weather', 'city')
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url).json()
    if response['cod'] == 200:  # checking if the request was successful
        return response
