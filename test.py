import tweepy
import json
import lxml.html
import re
import sys
import lucene
from flask import Flask, render_template

from textwrap import TextWrapper
from datetime import datetime
from elasticsearch import Elasticsearch

import urllib2
from BeautifulSoup import BeautifulSoup

# soup = BeautifulSoup(urllib2.urlopen("https://www.google.com"))
# print (soup.title.string)

auth = tweepy.OAuthHandler('hLRByyFsNZxZYWDz0DjXBQOw8', 'YVsa29E7JIZPgF5rB64P381Rp16gJuLSdxGfTGNqytRetctaAX')
auth.set_access_token('597091744-ErxxSds15D31kZZOCNCoj16sbUCZmCBItY4ry3YK', 'nykIaNpJP5cILHHzX9nFkDc9ZaXyWtT9C3A8s4knwFXRi')

api = tweepy.API(auth,wait_on_rate_limit=True)
# public_tweets = api.home_timeline()
# api.search(count=1,geocode="-33.602131,-70.576876,100km",json=True, parser=tweepy.parsers.JSONParser())

f = open("t.txt","a")
stopWords = ['a','about','an','and','are','as','at','be','but','by','for','from','has','have','he','his','in','is','it','its','more','new','of','on','one','or','said','say','that','the','their','they','this','to','was','which','who','will','with','you']
   
counter = 0

res = api.search(count=50,geocode="-33.602131,-70.576876,100km",lang="en",tweet_mode='extended')

print(len(res))

for r in tweepy.Cursor(api.search,count=3,geocode="-33.602131,-70.576876,100km",lang="en",tweet_mode='extended').items():
    r = r._json

    print('index: ',counter)
   
    counter += 1
    r = r['full_text']
    r = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', r)
    r = re.sub('[!?/@#:;"{},-.()\^\'_`%$]', '', r)
    
    # f.write(r)
    
libxml_disable_entity_loader(false)
t = lxml.html.parse("https://t.co/6vNCJXxIC4")
print( t.find(".//title").text)


# import lxml.html
# t = lxml.html.parse(url)
# print t.find(".//title").text


    