"""Unit testing of log_operate.py functions"""


from log_operate import format_request
from log_operate import filtered
from log_operate import formatted


def test_format_request_output():
    assert format_request(['request1', 'request2']) == 'REQUESTS: request1 - request2'


def test_format_request_integer():
    assert format_request(00) == '0'


def test_format_request_string():
    assert format_request('string') == 'string'


def test_filtered_1():
    assert filtered([{'id': 11}, {'id': 'new_id'}], [{'id': 'new_id'}]) == [{'id': 11}]


def test_filtered_empty():
    assert filtered([{'id': 11}], [{'id': 'other_id'}, {'id': 11}]) == []


def test_format():
    assert formatted([{'content': 'Due: December 31, 2020 16:32'}]) == [{'content': '2020-12-31 16:32'}]
    assert formatted([{'content': 'Due: June 15, 2025 18:05'}]) == [{'content': '2025-06-15 18:05'}]

