"""
anitv.py - Clone of a Java module for PircBotx
Copyright 2015-2016, dgw
Licensed under the GPL v3.0 or later
"""

from sopel.module import commands, example
from sopel import formatting
from datetime import datetime
import re
import requests

arg_regexen = {
    'chan': '\-(?:ch(?:an|l)?|sta?)\s+(\w+)',
    'ep':   '\-ep\s+(\d+)',
    'num':  '\-(\d+)',
    'rev':  '\-(r)',
}


def setup(bot):
    global arg_regexen

    for regex in arg_regexen:
        arg_regexen[regex] = re.compile('(?:^|\s+)%s' % arg_regexen[regex])


@commands('ani', 'anitv')
@example(".ani love lab")
def anitv(bot, trigger):
    anime = trigger.group(2)
    if not anime:
        bot.say("No anime specified.")
        return
    args = parse_args(anime)
    try:
        r = requests.get(url='http://anitv.foolz.us/json.php?controller=search&query=' + args['title'],
                         timeout=(10.0, 4.0))
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
    queue = []
    for result in data['results']:
        if 'error' in result:
            bot.say(result['error'])
            return
        if args['chan']:
            if args['chan'].lower() not in result['station'].lower():
                continue
        if args['ep']:
            if args['ep'] != result['episode']:
                continue
        queue.append(format_result(result))
        if len(queue) >= args['num']:
            break
    if not len(queue):  # empty results
        bot.say("No results matching search criteria.")
        return
    if args['rev']:
        queue.reverse()
    for result in queue:
        bot.say("%s%s airs on %s in %s" % (result['title'], result['episode'], result['station'], result['countdown']))


def parse_args(args):
    parsed = {
        'chan': '',
        'ep':   None,
        'num':  1,
        'rev':  False,
    }
    argd = {}
    for regex in arg_regexen:
        match = arg_regexen[regex].search(args)
        if match:
            argd[regex] = match
            args = args[:match.start()] + args[match.end():]  # remove parsed args from input
    for arg in argd:
        parsed[arg] = argd[arg].group(1)
    parsed['title'] = args  # what's left of the input after parsing should be the title
    parsed['num'] = int(parsed['num'])  # I hate special cases, but how else to do this?
    if parsed['num'] > 5:
        parsed['num'] = 5  # clamp max
    return parsed


def format_result(result):
    fixed = {
        'title':   result['title'] or 'Unknown title',
        'episode': result['episode'] or "",
        'station': result['station'] or 'Unknown station'
    }
    for k in fixed:
        if fixed[k]:
            fixed[k] = formatting.color(fixed[k], 'red')
    fixed['station'] = fixed['station'].replace('I think something messed up when you tried to copy that',
                                                'Ultra! A&G+')
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
