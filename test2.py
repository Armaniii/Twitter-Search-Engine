import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
import json
#import lxml.html
import re
import sys
from flask import Flask, render_template, request
from textblob import TextBlob
from textwrap import TextWrapper
from datetime import datetime
from elasticsearch import Elasticsearch
import elasticsearch_dsl
from elasticsearch_dsl.query import MultiMatch, Match
from elasticsearch_dsl import MultiSearch, Q, Search
from mechanize import Browser
import requests
from lxml.html import fromstring
import threading
import time
from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import urlopen
from multiprocessing import Pool
import time
#br = Browser()
#br.open("https://www.caranddriver.com/news/a25809005/2019-bmw-x7-off-road-ces/")
#print(br.title())

es = Elasticsearch(maxsize = 50)
#es.indices.delete(index='idx_twp', ignore=[400, 404])
auth = tweepy.OAuthHandler('hLRByyFsNZxZYWDz0DjXBQOw8', 'YVsa29E7JIZPgF5rB64P381Rp16gJuLSdxGfTGNqytRetctaAX')
auth.set_access_token('597091744-ErxxSds15D31kZZOCNCoj16sbUCZmCBItY4ry3YK', 'nykIaNpJP5cILHHzX9nFkDc9ZaXyWtT9C3A8s4knwFXRi')

api = tweepy.API(auth,wait_on_rate_limit=False)
raiseFieldLimit = '''
{
  "index.mapping.total_fields.limit": 10000
}'''

access_token = "597091744-ErxxSds15D31kZZOCNCoj16sbUCZmCBItY4ry3YK"
access_token_secret = "nykIaNpJP5cILHHzX9nFkDc9ZaXyWtT9C3A8s4knwFXRi"
consumer_key = "hLRByyFsNZxZYWDz0DjXBQOw8"
consumer_secret = "YVsa29E7JIZPgF5rB64P381Rp16gJuLSdxGfTGNqytRetctaAX"

s = requests.Session()

# app = Flask(__name__)
# @app.route('/', methods = ['GET', 'POST'])
# def mymap():
#   print("camre herer")
#   if requests.method == 'POST':
#     #address = request.form['address']
#     userlat = '33.9746816'
#     userltd = '-117.3517819'
#   return render_template('mymap.html', userlat = userlat, userltd=userltd)
# def createIndex():
#   i = 0
#   with open ('tweets1.json', 'w', encoding ='utf8') as file:
#     for r in tweepy.Cursor(api.search,count=10,geocode="-33.602131,-70.576876,100km", lang = "en", tweet_mode='extended').items():
#         r1 = r._json
#         for url in r1["entities"]["urls"]:
#           url = url["expanded_url"]
#           #title = ["entities"]["urls"]["expanded_url"]
#           #print(url)
#           r = requests.get(url, verify = False)
#           tree = fromstring(r.content)
#           #title= br.open(url)
#           #title_name = br.title()
#           title = tree.findtext(".//title")
#           #print(title)
#           json_data = r1

#           a_dict = {'Title': title}

#           json_data.update(a_dict)
#           #test = es.index(index="idx_twp3",
#                               # doc_type="twitter_twp3",
#                               # id = json_data['id'],
#                               # body={'author': json_data['user']['screen_name'],
#                               #     'title':title,
#                               #     'date':json_data['created_at'],
#                               #     'message':json_data['text']}
#                               # )
#           string = '{"index":{"_index":"twp", "_type":"tweets", "_id":' + str(i) + '}}\n' 
#           file.write(string)
#           # file.write({"index":{"_index":"cp", "_type":"products", "_id": "3"}})
#           json.dump(json_data, file)
#           file.write('\n')
#           print(i)
#           i = i+ 1

class TweetStreamListener(StreamListener):
  #print("Came here")
  def on_data(self, data):
    #print("camer here ")
    data1= json.loads(data)
    #print(data1["entities"])
    
    with open ('tweets4.json', 'a', encoding ='utf8') as file:
      for url in data1["entities"]["urls"]:
          url = url["expanded_url"]
          #title = ["entities"]["urls"]["expanded_url"]
          #print(url)
          try:
            r = s.get(url)
          except:
            time.sleep(5)
            continue
          #time.sleep(5)
          
          #tree = fromstring(r.content)
          #title= br.open(url)
          #title_name = br.title()
          #title = tree.findtext(".//title")
          #print(title)
          #print(r)
          parse_only = SoupStrainer("title")
          soup = BeautifulSoup(r.text, 'html.parser', parse_only = parse_only)
          #print(soup)
          if(r is None):
            title1 = ""
          else:
            title1 = getattr(soup, "title").text

          json_data = data1
          a_dict = {'Title': title1}

          json_data.update(a_dict)
          #test = es.index(index="idx_twp3",
                              # doc_type="twitter_twp3",
                              # id = json_data['id'],
                              # body={'author': json_data['user']['screen_name'],
                              #     'title':title,
                              #     'date':json_data['created_at'],
                              #     'message':json_data['text']}
                              # )
          string = '{"index":{"_index":"twp", "_type":"tweets", "_id":' + str(data1["id"]) + '}}\n' 
          file.write(string)
          #print("came here")
          # file.write({"index":{"_index":"cp", "_type":"products", "_id": "3"}})
          json.dump(json_data, file)
          file.write('\n')
         
  

def searchIndex(query):
  response = es.search(index='twp', body={
    'query': {
      'bool':{
        'should':[{
          'match': {
            'full_text': ".*" + query + "*."
            }
          }, {
            'match': {
              'Title': ".*" + query + "*."
            }
          }]
      }
    }
  })

  results = []
  for hit in response['hits']['hits']:
      #print("@" + hit["_source"]["user"]["screen_name"] + " posted at: " + hit["_source"]["created_at"] )
      #print("                   "+ hit["_source"]["text"])
      #print("        Title:                " + hit["_source"]["Title"])
      if(hit["_source"]["geo"] is not None):
        #print("         Latitude:  " + str(hit["_source"]["geo"]["coordinates"][0]) + "Longitude " + str(hit["_source"]["geo"]["coordinates"][1]))
        results.append({"lat":str(hit["_source"]["geo"]["coordinates"][0]), "lon": str(hit["_source"]["geo"]["coordinates"][1]), "message":hit["_source"]["text"]})

  print(results)
    


# class StreamListener(tweepy.StreamListener):
#     status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
#     def on_status(self, status):

#         #print 'n%s %s' % (status.author.screen_name, status.created_at)
#         try:
#             json_data = status._json


#             es.bulk(index="idx_twp1",
#                         doc_type="twitter_twp1",
#                         id = json_data['id'],
#                         body='tweets.json'
#                         )
#             #print(json_data['message'])
#         except Exception as e:
#             print(e)
#             pass
#{'author': json_data['user']['screen_name'],
                    #'date':json_data['created_at'],
                    #'message':json_data['text']}


if __name__ == '__main__':
  #createIndex()
  #app.run(debug=True)
  #es = Elasticsearch()
  listener = TweetStreamListener()
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  stream = Stream(auth, listener)
 
  # procs = 12
  # jobs =[]
  # l = 10
  # for x in range(10):
  #   try:
  #     stream = Stream(auth, listener)
  #     process = multiprocessing.Process(target=stream.filter(locations=[-125,25,-65,48],stall_warnings=False), async = True)
  #     process.start()
  #     jobs.append(process)
  #   except:
  #     continue

  # for j in jobs:
  #   j.join()

  p = Pool(12)
  while True:
    try:
      p.map(stream.filter(locations=[-125,25,-65,48]), async = True)
    except:
      continue


  # stream = Stream(auth, listener)
  # pool = multiprocessing.Pool(processes = multiprocessing.cpu_count()-1)
  # while True:
  #   #try:
  #   stream = Stream(auth, listener)  
  #   pool_outputs = pool.apply(stream.filter(locations=[-125,25,-65,48], async = True))
  #   #except:
  #     #continue
  #   pool.close()
  #   pool.join()
  # while True:
  #     stream = Stream(auth, listener)

  #     dat = StreamListener
  #     dat1 = dat.on_data
  #     p = Pool(processes =5)
  #     try:
  #       records = p.map(stream.filter(locations=[-125,25,-65,48], async = True))
  #     except:
  #       continue
  #     p.terminate()
  #     p.join()

  #stream.filter(locations=[-125,25,-65,48])
  #api = tweepy.API(auth,wait_on_rate_limit=True)
  #streamer.filter(None)


  # query = input("Enter your Query: ")

  # test = ""
  # searchIndex(query)

