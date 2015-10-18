"""
anitv.py - Port of a Java module for PircBotx
Copyright 2015, dgw
Licensed under the GPL v3.0 or later
"""

from willie.module import commands, example
from willie import formatting
from datetime import datetime
import re
import requests

argre = re.compile('\s*\-(\d)\s*')


@commands('ani', 'anitv')
@example(".ani love lab")
def anitv(bot, trigger):
    num = 1
    anime = trigger.group(2)
    if not anime:
        bot.say("No anime specified.")
        return
    arg = argre.search(anime)
    if arg:
        num = int(arg.group(1))
        anime = anime[:arg.start()] + anime[arg.end():]
    try:
        r = requests.get(url='http://anitv.foolz.us/json.php?controller=search&query=' + anime, timeout=(10.0, 4.0))
    except requests.exceptions.ConnectTimeout:
        bot.say("Connection timed out.")
        return
    except requests.exceptions.ConnectionError:
        bot.say("Couldn't connect to server.")
        return
    except requests.exceptions.ReadTimeout:
        bot.say("Server took too long to send data.")
        return
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        bot.say("HTTP error: " + e.message)
        return
    data = r.json()
    sent = 0
    for result in data['results']:
        if 'error' in result:
            bot.say(result['error'])
            return
        result = format_result(result)
        bot.say("%s%s airs on %s in %s" % (result['title'], result['episode'], result['station'], result['countdown']))
        sent += 1
        if sent >= num:
            break


def format_result(result):
    fixed = {
        'title':   result['title'] or 'Unknown title',
        'episode': result['episode'] or "",
        'station': result['station'] or 'Unknown station'
    }
    for k in fixed:
        if fixed[k]:
            fixed[k] = formatting.color(fixed[k], 'red')
    fixed['station'].replace('I think something messed up when you tried to copy that', 'Unknown station')
    if fixed['episode']:
        fixed['episode'] = " episode %s" % formatting.color(fixed['episode'], 'red')
    fixed['countdown'] = format_countdown(datetime.fromtimestamp(result['unixtime']) - datetime.today())
    return fixed


def format_countdown(timediff):
    days = timediff.days
    hours, remainder = divmod(timediff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    g_days = "day" if days == 1 else "days"
    g_hours = "hour" if hours == 1 else "hours"
    g_minutes = "minute" if minutes == 1 else "minutes"
    g_seconds = "second" if seconds == 1 else "seconds"
    countdown = "%d %s " % (days, g_days) if days else ""
    countdown += "%d %s " % (hours, g_hours) if hours else ""
    countdown += "%d %s " % (minutes, g_minutes) if minutes else ""
    countdown += "%d %s" % (seconds, g_seconds) if seconds else ""
    return countdown
