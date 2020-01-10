from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

#Variables that contains the user credentials to access Twitter API 
access_token = "597091744-ErxxSds15D31kZZOCNCoj16sbUCZmCBItY4ry3YK"
access_token_secret = "nykIaNpJP5cILHHzX9nFkDc9ZaXyWtT9C3A8s4knwFXRi"
consumer_key = "hLRByyFsNZxZYWDz0DjXBQOw8"
consumer_secret = "YVsa29E7JIZPgF5rB64P381Rp16gJuLSdxGfTGNqytRetctaAX"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        r = json.loads(data)
        print (r["entities"])
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])