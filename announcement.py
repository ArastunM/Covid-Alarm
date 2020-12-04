"""This module is used to apply announcements"""


import threading
import pyttsx3
from playsound import playsound
from retrieve_data import from_config

QUEUE = []
notification_sound = from_config('notify_sound')


def announce_join(title: list, content: list, number: list, announcement: bool):
    """Threading announce functions"""
    thread = threading.Thread(target=type_check, args=(title, content, number, announcement))
    thread.start()  # starting the type_check thread


def type_check(title: list, content: list, number: list, announcement: bool):
    """Plays notification sound / checks notification type"""
    playsound(notification_sound)
    if announcement:  # only announce if type is announcement
        announce(title, content, number)


def announce(title: list, content: list, number: list, item='notification'):
    """Takes a list of notifications and announces them"""
    # if multiple announce functions are threaded, a queue is formed
    engine = pyttsx3.init()
    speak = ''
    for i, obj in enumerate(title):  # formatting values to be announced
        speak += f'{item} number {number[i]}: {obj["title"]} \n {content[i]["content"]} \n\n'
    engine.say(speak)
    try:
        engine.runAndWait()
        engine.stop()
        if QUEUE:  # if queue is not empty
            temp_list = QUEUE.pop(0)
            announce(temp_list[0], temp_list[1], temp_list[2])
    except RuntimeError or KeyError:
        # when engine is busy add to the queue
        QUEUE.append([title, content, number])
