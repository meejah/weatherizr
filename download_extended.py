#!/usr/bin/env python

'''
This downloads the southern alberta extended forecast, parses the
<pre> tag out of the HTML and dumps that in a file named by the
current date.

Hopefully they don't add more <pre> tags ;)
'''

# requests is way nicer, but since this is so simple I'm going to do
# it with no external dependencies...

import urllib2
from HTMLParser import HTMLParser
from datetime import datetime
from os.path import join

class Parser(HTMLParser):
    recording = False

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.recording = True
            self.text = ''
    def handle_data(self, data):
        if self.recording:
            self.text += data
    def handle_endtag(self, tag):
        if tag == 'pre':
            self.recording = False

data = urllib2.urlopen('http://weather.gc.ca/forecast/public_bulletins_e.html?Bulletin=fpcn53.cwwg').read()
print len(data)
parser = Parser()
parser.feed(data)

fname = datetime.now().strftime('extended/%Y-%m-%d.txt')
join(__file__, '..', fname)
with open(fname, 'w') as f:
    f.write(parser.text)
