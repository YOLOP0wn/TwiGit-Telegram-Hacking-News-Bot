#!usr/bin/python2
# encoding=utf8

consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""
telegram_token = ""
chat_id = ""

import telegram
from TwitterAPI import TwitterAPI, __version__
from TwitterAPI.TwitterOAuth import TwitterOAuth
import codecs
import json
import sys
import time
from datetime import date
import requests
import re


def send(msg, chat_id, token=telegram_token):
	bot = telegram.Bot(token=telegram_token)
	bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')


def _search(name, obj):
    """Breadth-first search for name in the JSON response and return value."""
    q = []
    q.append(obj)
    while q:
        obj = q.pop(0)
        if hasattr(obj, '__iter__') and type(obj) is not str:
            isdict = isinstance(obj, dict)
            if isdict and name in obj:
                return obj[name]
            for k in obj:
                q.append(obj[k] if isdict else k)
    else:
        return None


def get_id():
        file = open('id.txt', 'r')
        id = file.read()
        file.close()
        return id

def new_id(id):
        file = open("id.txt","w")
        file.write(id)
        file.close()



search = ['id','full_text','screen_name','created_at','expanded_url'] #Twitter
word = ["poc+cve", "0day", "exploit+cve"] #Github

since_id = get_id() #Get last Tweet id

temp_id = 0
git = ""
tweets = ""
today = str(date.today()) #Today date YYYY-MM-DD

if __name__ == '__main__':
    try:

	######## PULL TWITTER NEWS ############

        api = TwitterAPI(consumer_key,
                         consumer_secret,
                         access_token_key,
                         access_token_secret)
        response = api.request('search/tweets', {'q':"(poc cve) OR (exploit cve) OR (#0day) -filter:retweets -filter:replies", 'tweet_mode':'extended', 'since_id':int(since_id)})

        for item in response.get_iterator():
		link = ''
                for name in search:
                    value = _search(name, item)
                    if value:
			if name == "screen_name":
				username = value
			elif name == "id":
				tweet_id = value
				if int(tweet_id) > int(temp_id):
					temp_id = tweet_id
			elif name == "full_text":
				text = value
				c = re.search("CVE-\d{4}-\d{4,7}", text)
                                cve = c.group(0) if c else ""
			elif name == "created_at":
				dt = value
			elif name == "expanded_url":
                                link = value

			#print('%s' % (value))


	##### DO NOT ADD TWEET IF THE SAME CVE-ID OR URL ALREADY EXIST #####	
		if cve:
                        if cve not in tweets:
                                tweets += username + "\n" + text + "\n" + link + "\n\n"
                elif link:
                        if link not in tweets:
                                tweets += username + "\n" + text + "\n" + link + "\n\n"
                else:
                        tweets += username + "\n" + text + "\n" + link + "\n\n"


	if temp_id  != 0:
                new_id(str(temp_id))



	######## PULL GITHUB NEWS ###########
	for w in word:
        	response = requests.get("https://api.github.com/search/repositories?q="+ w +"&sort=updated")
	        data = sorted(response.json()['items'], key=lambda x: x['created_at'], reverse = True)


        	for u in data:
                	if today == u['created_at'].split('T')[0]:
                        	git += u['full_name'] + "\n" + u['description'] + "\n" + u['html_url'] + "\n\n"




	####### SEND TWITTER AND GITHUB NEWS TO TELEGRAM ##########
	if len(tweets) > 0:
		tmsg = "\xE2\x9A\xA0 \xE2\x9A\xA0 TWITTER NEWS \xE2\x9A\xA0 \xE2\x9A\xA0 \n\n".decode('utf-8') + tweets
                send(tmsg, chat_id, token=telegram_token)

	if len(git) > 0:
		gmsg = "\xE2\x9A\xA0 \xE2\x9A\xA0 GITHUB NEWS \xE2\x9A\xA0 \xE2\x9A\xA0 \n\n".decode('utf-8') + git
		send(gmsg, chat_id, token=telegram_token)


    except KeyboardInterrupt:
        print('Terminated by user')

    except Exception as e:
        print('STOPPED: %s' % e)
	send('Error: %s' % e, chat_id, token=telegram_token)
