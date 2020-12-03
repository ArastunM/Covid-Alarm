"""This module is used to apply logging related functions"""

import ast
from datetime import datetime
from side_funcs import date_difference


def format_request(requested: list):
    """Applying log format for requests"""
    if isinstance(requested, list):
        log_info = 'REQUESTS: '
        for index, item in enumerate(requested):
            log_info += f"{item}"
            if index != len(requested) - 1:
                log_info += " - "
        return log_info


def restore_briefings(log_file):
    """Used to restore hourly briefings"""
    with open(log_file) as logfile:
        brief_time = ''
        for line in logfile.readlines():
            if '__main__ - INFO' in line[:15]:
                # searching for the called briefings in log lines
                if line[46:59] == 'BRIEF CALLED:':
                    brief_time = line[60:].strip()
        open(log_file, 'w').close()

        try:
            # formatting the date
            brief_time = datetime.strptime(brief_time, '%B %d, %H:%M')
            last_time = brief_time.strftime('%B %d, %H:%M')
            brief_time = brief_time.strftime(f"{datetime.today().strftime('%Y')}-%m-%d %H:%M")
            return date_difference(brief_time), last_time
        except ValueError:
            # past hour is reported in case no 'BRIEF CALLED:' was found
            return -3600, brief_time


def restore_alarms(log_file):
    """Used to restore previous alarms"""
    with open(log_file) as logfile:
        added_alarms = []
        removed_alarms = []
        for line in logfile.readlines():
            if '__main__ - INFO' in line[:15]:
                # searching for alarm / notification related log lines
                if line[46:56] == 'NEW ALARM:':
                    added_alarms.append(ast.literal_eval(line[57:].strip()))
                elif line[46:60] == 'REMOVED ALARM:':
                    removed_alarms.append(ast.literal_eval(line[61:].strip()))
                elif line[46:57] == 'NEW NOTIFY:':
                    removed_alarms.append(ast.literal_eval(line[58:].strip()))

        added_alarms = filtered(added_alarms, removed_alarms)
        return formatted(added_alarms)


def filtered(alarms: list, removed: list):
    """Filtering removed out of alarms"""
    filtered_alarms = []
    for alarm in alarms:
        for remove in removed:
            if alarm['id'] == remove['id']:
                filtered_alarms.append(alarm)
                break
    return [i for i in alarms if i not in filtered_alarms]


def formatted(alarms: list):
    """Applying date format to retrieved alarms"""
    for alarm in alarms:
        alarm['content'] = alarm['content'][5:]
        alarm['content'] = datetime.strptime(alarm['content'], '%B %d, %Y %H:%M')
        alarm['content'] = alarm['content'].strftime("%Y-%m-%d %H:%M")
    return alarms
