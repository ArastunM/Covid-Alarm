"""Module for applied side functions"""

from datetime import datetime
import random
import ast


def gen_id(base: str) -> str:
    """Generating a random ID"""
    alphabet = list(map(chr, range(97, 123)))
    code = ''.join(random.choice(alphabet) for i in range(random.randint(7, 10)))
    return base.lower() + code


def date_difference(scheduled):
    """Used to find date difference"""
    current = datetime.now().strftime("%Y-%m-%d %H:%M")
    d1, d2 = current + ':00', scheduled + ':00'

    try:
        d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
        d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # if date format was not appropriate the argument is returned
        return scheduled
    # time difference found in seconds
    time_delta = (d2 - d1)
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
        try:
            part.append(ast.literal_eval(track_string(str(event), ',', '(', True, 2)))
        except SyntaxError:
            pass
    for i in range(len(part)):
        if part[i]['title'] == remove:
            return [i, part[i]]


def track_string(string: str, start, end, from_end, skip=0):
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
