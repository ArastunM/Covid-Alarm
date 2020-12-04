"""Unit testing of side_funcs.py functions"""


from datetime import datetime
from side_funcs import gen_id
from side_funcs import readable_date
from side_funcs import date_difference
from side_funcs import find_alarm
from side_funcs import track_string


def test_gen_id_output():
    assert 'name' in gen_id('name')


def test_gen_id_len():
    assert len(gen_id('name')) >= 11


def test_date_difference_wrong():
    assert date_difference('wrong format') == 'wrong format'


def test_date_difference_today():
    assert date_difference(datetime.now().strftime("%Y-%m-%d %H:%M")) == 0


def test_readable_date():
    assert readable_date("2020-05-05 16:00") == "May 05, 2020 16:00"


def test_find_alarm_output():
    sample_event = ["Event(time=1609432320.2011623, priority=1, "
                    "action=<function alarm_to_notification at 0x046CF538>, "
                    "argument=({'title': 'Name', 'content': 'January 31, 2021 16:32', "
                    "'id': 'namemczrgcckyg', 'news': None, 'weather': None}, None, None), kwargs={})"]
    assert find_alarm(sample_event, 'Name') == [0, "{'title': 'Name', 'content': 'January 31, 2021 16:32', "
                                                   "'id': 'namemczrgcckyg', 'news': None, 'weather': None}"]

    assert not find_alarm(sample_event, 'Name2')


def test_find_alarm_wrong():
    assert not find_alarm(['wrong event sample'], 'Name')


def test_track_string_default():
    assert track_string('{hello}', '{', '}', False) == 'hello'


def test_track_string_reverse():
    assert track_string('/reverse/text/', '/', '/', True) == 'text'


def test_track_string_skip():
    assert track_string('m skip m yes mm', 'm', 'm', False, 1) == ' yes '
