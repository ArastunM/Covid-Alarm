"""Unit testing of retrieve.py functions"""


from retrieve_data import from_config
from retrieve_data import get_covid
from retrieve_data import get_news
from retrieve_data import get_weather


def test_location_covid():
    assert isinstance(from_config('retrieve', 'covid', 'location'), list)


def test_location_news():
    assert isinstance(from_config('retrieve', 'news', 'country'), str)


def test_location_weather():
    assert isinstance(from_config('retrieve', 'weather', 'city'), str)


def test_local_resources_log_file():
    assert isinstance(from_config('log_file', 'file_name'), str)
    assert from_config('log_file', 'file_name')[-4:] == '.log'


def test_local_resources_image():
    accept = ['.png', '.jpg', '.jpeg', '/png', '/jpeg']
    assert isinstance(from_config('image'), str)
    assert from_config('image')[-4:] in accept


def test_external_services_covid_type():
    assert isinstance(get_covid(), str)


def test_external_services_covid_return():
    assert get_covid()


def test_external_services_news():
    assert isinstance(get_news(), str)


def test_external_services_news_return():
    assert get_news()


def test_external_services_weather():
    assert isinstance(get_weather(), str)


def test_external_services_weather_return():
    assert get_weather()
