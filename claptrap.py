#!/usr/bin/env python

import tweepy
import requests
import signal
import sys
import time
import re

#Twitter credentials
CONSUMER_KEY = None
CONSUMER_SECRET = None
ACCESS_TOKEN = None
ACCESS_SECRET = None

#Mailgun info and API key
SEND_FROM = None #'claptrap.py <postmaster@yourdomain.mailgun.org>'
SEND_TO = None #'you <you@somewhere.com>'
MAILGUN_API_KEY = None

#Other set up
peeps = ['16567106','8369072','846328884'] #@gearboxsoftware, @duvalmagic, @ECHOcasts
platform = 'PC' #Substitute other keywords as needed
pattern = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

def parse_tweet(tweet):
    shift_key = pattern.search(tweet.text)
    if (shift_key and platform in tweet.text and "RT" not in tweet.text
        and tweet.user.id_str in peeps):
        return True
    else:
        return False

def high_five(subject=None, body=None):
    return requests.post(
        "https://api.mailgun.net/v2/[YOURDOMAIN].mailgun.org/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": SEND_FROM,
              "to": SEND_TO,
              "subject": subject,
              "text": body})


#listener
class TW_Listner(tweepy.StreamListener):
    def on_status(self, tweet):
        if parse_tweet(tweet):
            subject = '[CLAPTRAP] ' + tweet.text
            body = ('Hi!\r\n\r\nClaptrap.py found a SHiFT key. High Five!\r\n\r\n'
                    +'@'+tweet.user.screen_name+'\r\n'
                    +tweet.text+'\r\n'
                    +'https://twitter.com/'
                    +tweet.user.screen_name
                    +'/status/'+tweet.id_str)
            for http_post in range(3):
                try:
                    high_five(subject,body)
                except (requests.ConnectionError, requests.HTTPError,
                        requests.RequestException):
                    time.sleep(30)
                    pass
                else:
                    break
            else:
                print "Nobody came to my birthday party.\n\n" + tweet.text
                return True #Keep going
        return True

    def on_error(self, status):
        print status
        if '420' in status: #Enhance Your Calm
            time.sleep(300)
        return True

    def on_timeout(self):
        print 'Connection timed out.\n'
        time.sleep(120) #time out, wait 2 minutes
        return True


if __name__ == '__main__':
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        print "Starting..."
        listener = TW_Listner()
        stream = tweepy.Stream(auth, listener)
        stream.filter(follow=peeps)
    except (KeyboardInterrupt, SystemExit, signal.SIGTERM):
        print 'Quit'
        sys.exit()
