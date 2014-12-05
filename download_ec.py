#!/usr/bin/env python

'''
This downloads weather data from environment canada using the Atom
feed for a particular weather forecast.

It parses out the update-time, and the predicted high and low for the
next days (6 days it seems?) and outputs one row of CSV data with the
updated date, and then low, high, low, high etc for the next days.

Pretty messy...
'''

import re
import feedparser
import csv
from sys import stdout
from datetime import datetime

# grab from any environment canada local forecast
URI = 'http://weather.gc.ca/rss/city/ab-52_e.xml'

number_re = re.compile(r'([0-9]+)')

# download our feed
d = feedparser.parse(URI)

updated = d['feed']['updated']
# looks like: 2014-11-29T09:15:00Z
# ...but we only care about the day
updated = datetime.strptime(updated.split('T')[0], '%Y-%m-%d').date()

def search_temps(text):
    temps = dict(low=None, high=None)
    for phrase in text.lower().split('.'):
        for temptype in ['low', 'high']:
            temp = None
            if temptype in phrase:
                m = number_re.search(phrase)
                if m:
                    temp = int(m.group(1))
                    if 'minus' in phrase:
                        temp = -temp
                elif 'zero' in phrase:
                    temp = 0
            if temp is not None:
                temps[word] = temp
    return temps['low'], temps['high']

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
future = []
for entry in d['entries']:
    title = entry['title'].strip().lower()
    # there are entries like "current conditions:" or "friday night:"
    # which we want to ignore, and just take e.g. "saturday:"
    day = title.split(':')[0].rstrip(':')
    if day not in days:
        continue

    # note that low or high could be None still here, if we couldn't
    # parse them out (or, sometimes they're missing from the
    # forecast). In that case they'll be blank in the CSV-line
    low, high = search_temps(title)
    future.append(low)
    future.append(high)

out = csv.writer(stdout)
out.writerow([updated] + future)
