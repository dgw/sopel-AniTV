"""
anitv.py - Port of a Java module for PircBotx
Copyright 2015, dgw
Licensed under the GPL v3.0 or later
"""

from willie.module import commands, example
from willie import formatting
from willie.tools import Identifier
from datetime import datetime
import re, requests

argre = re.compile('\s*\-(\d)\s*')

@commands('ani', 'anitv')
@example('.ani love lab')
@example('.anitv love live')
def anitv(bot, trigger):
    num = 1
    anime = trigger.group(2)
    arg = argre.search(anime)
    if arg:
        num = int(arg.group(1))
        anime = anime[:arg.start()] + anime[arg.end():]
    try:
        r = requests.get(url='http://anitv.foolz.us/json.php?controller=search&query=' + anime, \
                         timeout=(10.0, 4.0))
    except requests.exceptions.ConnectionError:
        bot.say('Couldn\'t connect to server.')
    except requests.exceptions.ConnectTimeout:
        bot.say('Connection timed out.')
    except requests.exceptions.ReadTimeout:
        bot.say('Server took too long to send data.')
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        bot.say('HTTP error: ' + e.message)
    data = r.json()
    sent = 0
    for result in data['results']:
        if 'error' in result:
            bot.say(result['error'])
            return
        title = formatting.color(result['title'], 'red')
        episode = formatting.color(result['episode'], 'red')
        station = formatting.color(result['station'], 'red')
        station = station.replace('I think something messed up when you tried to copy that', 'Unknown station')
        timediff = datetime.fromtimestamp(result['unixtime']) - datetime.today()
        days = timediff.days
        hours, remainder = divmod(timediff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        g_days = 'day' if days == 1 else 'days'
        g_hours = 'hour' if hours == 1 else 'hours'
        g_minutes = 'minute' if minutes == 1 else 'minutes'
        g_seconds = 'second' if seconds == 1 else 'seconds'
        countdown = '%d %s ' % (days, g_days) if days else ''
        countdown += '%d %s ' % (hours, g_hours) if hours else ''
        countdown += '%d %s ' % (minutes, g_minutes) if minutes else ''
        countdown += '%d %s' % (seconds, g_seconds) if seconds else ''
        bot.say('%s episode %s airs on %s in %s' % (title, episode, station, countdown))
        sent += 1
        if sent >= num:
            break

