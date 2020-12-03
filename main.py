"""This is the central module for Covid-aware alarm clock"""

import sched
import time
import logging
from datetime import datetime
from flask import Flask, request, render_template, redirect
from retrieve_data import from_config, get_covid, get_news, get_weather
from side_funcs import gen_id, date_difference, readable_date, find_alarm
from log_operate import format_request, restore_alarms, restore_briefings
from announcement import announce_join

# defining variables
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
alarm_list = []
notify_list = []
image = from_config('image')
log_file = from_config('log_file', 'file_name')

# defining logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(from_config('log_file', 'format'))
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def initiate():
    """Used to restore alarms and briefings"""
    restored_alarms = restore_alarms(log_file)  # restoring alarms
    for alarm in restored_alarms:
        add_alarm(alarm['title'], alarm['content'], alarm['news'], alarm['weather'], True)

    delay, brief_time = restore_briefings(log_file)  # restoring briefings
    if delay > -3600:
        # log the briefing time so its not lost
        logger.info('BRIEF CALLED: ' + str(brief_time))
    s.enter(3600 + delay, 1, hourly_briefings, (datetime.now().strftime("%B %d, %H:%M"),))


s.enter(0, 1, initiate)


@app.route('/')
def start_page():
    """Start page, redirects to /index"""
    return redirect('/index')


@app.route('/index')
def main_page():
    """Main function loop"""
    s.run(blocking=False)
    alarm_name = request.args.get('two')
    alarm_time = request.args.get('alarm')
    alarm_close = request.args.get('alarm_item')
    notify_close = request.args.get('notif')
    news = request.args.get('news')
    weather = request.args.get('weather')

    # logging requests
    logger.info(format_request([alarm_name, alarm_time, alarm_close,
                                notify_close, news, weather]))

    # closing alarms and notifications
    if alarm_close:
        return close_alarm(alarm_close)
    elif notify_close:
        return close_notification(notify_close)

    # adding new alarms
    if alarm_name and alarm_time:
        return add_alarm(alarm_name, alarm_time, news, weather)
    return render_template('index.html', alarms=alarm_list, notifications=notify_list, image=image)


def add_alarm(title, content, news, weather, from_log=False):
    """Used to add new alarms"""
    # working on time format
    alarm_time = content.replace('T', ' ')
    delay = date_difference(alarm_time)
    alarm_time = readable_date(alarm_time)
    if delay >= 0 or from_log:
        # call function / logging / assign alarm values / refresh
        alarm_list.append({'title': title, 'content': "Due: " + alarm_time,
                           'id': gen_id(title), 'news': news, 'weather': weather})
        # logging new alarm
        logger.info('NEW ALARM: ' + str(alarm_list[len(alarm_list) - 1]))
        s.enter(delay, 1, alarm_to_notification, (alarm_list[len(alarm_list) - 1], news, weather,))
    else:
        logger.warning('ALARM NOT ADDED - PAST DATE')
    if not from_log:  # only refresh the page if alarms were submitted manually
        return redirect('/index')


def hourly_briefings(due_time):
    """Calling hourly briefings"""
    # removing previous briefings
    logger.info('BRIEF CALLED: ' + str(due_time))
    remove = []
    for item in notify_list:
        if item['id'] == 'brf':
            remove.append(item)
    for item in remove:
        notify_list.remove(item)

    temp_list = assign_briefings(due_time)
    retrieved_count = len([i for i in temp_list if i is not None])
    # logging retrieved briefings
    logger.info('BRIEFINGS RETRIEVED: ' + str(retrieved_count))

    # announcing added briefings
    size = len(notify_list)
    temp_list = [size - i for i in range(retrieved_count)][::-1]
    if retrieved_count > 0:
        announce_join(notify_list[-retrieved_count::], notify_list[-retrieved_count::], temp_list, True)
    s.enter(3600, 1, hourly_briefings, (datetime.now().strftime("%B %d, %H:%M"),))


def assign_briefings(due_time):
    # retrieving and assigning to briefings
    news_report = get_news()
    weather_report = get_weather()
    covid_report = get_covid()
    if news_report:
        notify_list.append({'title': 'News report at ' + due_time, 'content': news_report,
                            'id': 'brf'})
    if weather_report:
        notify_list.append({'title': 'Weather report at ' + due_time, 'content': weather_report,
                            'id': 'brf'})
    if covid_report:
        notify_list.append({'title': 'COVID report at ' + due_time, 'content': covid_report,
                            'id': 'brf'})
    return [news_report, weather_report, covid_report]


def alarm_to_notification(event, news, weather):
    """Used during Alarm timeout"""
    if news or weather:
        event['content'] = ''
        if news:  # if news should be retrieved
            news_report = get_news()
            if news_report:
                event['title'] += " / news report"
                event['content'] += news_report + '\n'
        if weather:  # if weather should be retrieved
            weather_report = get_weather()
            if weather_report:
                event['title'] += " / weather report"
                event['content'] += weather_report
    assign_notifications(event, news, weather)


def assign_notifications(event, news, weather):
    new_notify = alarm_list.pop(alarm_list.index(event))
    if event['content'] != '':
        notify_list.append(new_notify)
        # logging new notification
        logger.info('NEW NOTIFY: ' + str(notify_list[len(notify_list) - 1]))
        # announcing current notification
        announce_join([event], [event], [len(notify_list)], news or weather)


def close_alarm(tar_alarm):
    """Used to remove/dismiss alarms"""
    rm_index, part = find_alarm(s.queue, tar_alarm)
    s.cancel(s.queue[rm_index])
    for item in alarm_list:
        if item['id'] == part['id']:
            alarm_list.remove(item)
            # logging removal of an alarm
            logger.info('REMOVED ALARM: ' + str(item))
    return redirect('/index')


def close_notification(tar_notify):
    """Used to remove/dismiss notifications"""
    for item in notify_list:
        if item['title'] == tar_notify:
            notify_list.remove(item)
            # logging removal of notification
            logger.info('REMOVED NOTIFY: ' + str(item))
            break
    return redirect('/index')


if __name__ == '__main__':
    app.run(debug=True)
