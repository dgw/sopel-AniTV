"""
anitv.py - Port of a Java module for PircBotx
Copyright 2015, dgw
Licensed under the GPL v3.0 or later
"""

from willie.module import commands, example
from willie import formatting
from willie.tools import Identifier
from datetime import datetime
import requests

@commands('ani', 'anitv')
@example('.ani love lab')
@example('.anitv love live')
def anitv(bot, trigger):
    anime = trigger.group(2)
    r = requests.get('http://anitv.foolz.us/json.php?controller=search&query=' + anime)
    data = r.json()
    for result in data['results']:
        title = formatting.color(result['title'], 'red')
        episode = formatting.color(result['episode'], 'red')
        station = formatting.color(result['station'], 'red')
        station = station.replace('I think something messed up when you tried to copy that', 'Unknown station')
        timediff = datetime.fromtimestamp(result['unixtime']) - datetime.today()
        countdown = formatting.color(str(timediff), 'red')
        bot.say('%s episode %s airs on %s in %s' % (title, episode, station, countdown))

