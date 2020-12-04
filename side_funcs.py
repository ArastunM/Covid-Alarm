"""Module for applied side functions"""

from datetime import datetime
import random


def gen_id(base: str) -> str:
    """Generating a random ID"""
    alphabet = list(map(chr, range(97, 123)))  # generating english alphabet
    code = ''.join(random.choice(alphabet) for i in range(random.randint(7, 10)))  # choosing random letters
    return base.lower() + code


def date_difference(scheduled):
    """Used to find date difference"""
    current = datetime.now().strftime("%Y-%m-%d %H:%M")
    date1, date2 = current + ':00', scheduled + ':00'

    try:
        date1 = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
        date2 = datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return scheduled  # if date format was not appropriate the argument is returned
    # time difference calculated in seconds
    time_delta = (date2 - date1)
    total_seconds = int(time_delta.total_seconds())
    if total_seconds > 0:
        total_seconds -= int(datetime.now().strftime("%S"))
    return total_seconds


def readable_date(date):
    """Formatting the date into a more human readable form"""
    try:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        return date.strftime("%B %d, %Y %H:%M")
    except ValueError:
        return date


def find_alarm(events, remove):
    """Find the selected alarm from queue"""
    # getting name and time of events from queue using track_string
    part = []
    for event in events:
        part.append(track_string(str(event), ',', '(', True, 2))
    for index, item in enumerate(part):
        if remove in item:
            return [index, item]  # returning queue index and item itself


def track_string(string: str, start: str, end: str, from_end: bool, skip=0) -> str:
    """Tracking parts of the given string with different configurations"""
    recorded = ''
    read = False
    if from_end:  # if tracking should be in reversed order
        string = string[::-1]

    for letters in string:
        if letters == end and read:
            break
        if read:
            recorded += letters
        if letters == start:
            if skip > 0:  # applying skips
                skip -= 1
            else:
                read = True

    if from_end:  # reversing string back
        recorded = recorded[::-1]
    return recorded
