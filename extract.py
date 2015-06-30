#!/usr/bin/python3

import os
import re
import sys

from urllib import request

if len(sys.argv) < 2:
    print("pass a subreddit as a command argument")
    exit(1)

sub = sys.argv[1]
text = request.urlopen("http://filmot.org/r/{}".format(sub)).read().decode('utf-8')
urlreg = re.compile(r'<a[\s\S]*?href="(?P<url>.*?)"[\s\S]*?>[\s\S]*?</a>')
imgreg = re.compile(r'<img[\s\S]*?src="(?P<url>.*?)"[\s\S]*?>')

def isvalid(url):
    return ("/r/" in url and
            url != "/r/{}/new".format(sub) and
            url != "/r/{}/top".format(sub))

def download(url):
    if os.path.isfile(url+".jpg") or os.path.isfile(url+".png"):
        return False
    url = "http://filmot.org" + url
    text = request.urlopen(url).read().decode('utf-8')
    for match in imgreg.finditer(text):
        url = match.group("url")
        if "//i.filmot.org" in url:
            url = "http:" + url
            name = url.split("/")[-1]
            # Don't download duplicates
            if os.path.isfile(name):
                return False
            
            print(name)
            with open(name, "w+b") as f:
                data = request.urlopen(url).read()
                f.write(data)
            return True

count = 0
print("downloading from {}".format(sub))
for match in urlreg.finditer(text):
    url = match.group("url")
    if isvalid(url):
        if download(url):
            count += 1

print("downloaded {} new lovely images from {}".format(count, sub))
