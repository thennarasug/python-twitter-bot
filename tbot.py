# TelegramBot
import time
# heroku env variables
from os import environ

import telepot
# Import a text processing library
from textblob import TextBlob
# Twython twitter api
from twython import Twython, TwythonError

'''
#no more command line or dynamic arguments, just kept it for reference.

keywords = input("twitter search keyword? ")
rt_fav_limit = input("max retweet_count or favorite_count? ")
'''

keywords_rt_fav_limits_all = [[50, ['signalapp', 'degoogle','pinebook','pine64','pinephone']],
                              [125, ['tutanota', 'protonmail', 'duckduckgo', 'protonvpn', 'tails OS', 'tor browser']],
                              [250, ['linux', 'manjaro', 'ubuntu']]]


# TelegramBot method
def sendtotelegram(TELEGRAM_TOKEN, TELEGRAM_TELEGRAM_CHAT_ID, tweetToTelegram):
    TelegramBot = telepot.Bot(TELEGRAM_TOKEN)
    # aboutme = TelegramBot.getMe()
    # print (TelegramBot.getMe())

    '''commented
    messages = TelegramBot.getUpdates()
    for message in messages:
        chat_id = message["message"]["from"]["id"]
    '''
    chat_id = TELEGRAM_TELEGRAM_CHAT_ID
    TelegramBot.sendMessage(chat_id, tweetToTelegram)
    print("****updated TelegramBot****")


# Analysis method
def analysis(sentence):
    # for sentence in sentences:
    # Instantiate TextBlob
    analysis = TextBlob(sentence)
    # Parts of speech
    # print("{}\n\nParts of speech:\n{}\n".format(sentence, analysis.tags))
    # Sentiment analysis
    sentiment = analysis.sentiment
    # print("Sentiment:\n{}\n\n".format(sentiment))
    return sentiment.polarity


APP_KEY = environ.get('APP_KEY')
APP_SECRET = environ.get('APP_SECRET')
OAUTH_TOKEN = environ.get('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = environ.get('OAUTH_TOKEN_SECRET')
TELEGRAM_TOKEN = environ.get('TELEGRAM_TOKEN')
TELEGRAM_TELEGRAM_CHAT_ID = environ.get('TELEGRAM_TELEGRAM_CHAT_ID')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# results = twitter.cursor(twitter.search, q='fiveperfectmovies')
# for result in results:
#    print(result['id_str'] + " : " + result['text'])

'''
#below section of code is to read the lines from a file and to tweet.
#not in use now, just kept for reference.

with open('tweets.txt', 'r+') as tweetfile:
	buff = tweetfile.readlines()

for line in buff[:]:
	line = line.strip(r'\n')
	if len(line)<=280 and len(line)>0:
		print ("Tweeting...")
		try:
			twitter.update_status(status=line)
		except TwythonError as e:
			print (e)
		with open ('tweets.txt','w') as tweetfile:
			buff.remove(line)
			tweetfile.writelines(buff)
		time.sleep(1)
	else:
		with open ('tweets.txt', 'w') as tweetfile:
			buff.remove(line)
			tweetfile.writelines(buff)
		print ("Skipped line - Too long for a tweet!")
		continue
'''

# indefinite while loop that runs every 1 hour. To remove the dependency on scheduler.
while True:
    for keywords_rt_fav_limits_entry in keywords_rt_fav_limits_all:
        rt_fav_limit = keywords_rt_fav_limits_entry[0]
        keywords = keywords_rt_fav_limits_entry[1]
        for keyword in keywords:
            for lang_list in ['en', 'ta']:
                try:
                    # count=100 max (default 15), result_type='mixed' or 'recent'
                    # count=15 max (default 15), result_type='popular'
                    print("search twitter......", keyword, " in ", lang_list, " with max_limit as ", rt_fav_limit)
                    search_results = twitter.search(q=keyword, count=1000, lang=lang_list, result_type='mixed')
                    # print (search_results)
                except TwythonError as e:
                    print(e)

                count = 0
                for tweet in search_results['statuses']:
                    if "RT @" not in tweet['text'] and (
                            tweet['favorite_count'] >= int(rt_fav_limit) or tweet['retweet_count'] >= int(
                            rt_fav_limit)) and tweet['retweeted'] == False and tweet[
                        'is_quote_status'] == False:  # and tweet['possibly_sensitive'] == False:
                        polarity_result = analysis(tweet['text'])
                        if polarity_result >= 0.25 or lang_list == 'ta':
                            try:
                                if len(tweet['text']) > 200 or "https" in tweet['text']:
                                    print(tweet['text'])
                                    twitter.retweet(id=int(tweet['id']))
                                    sendtotelegram(TELEGRAM_TOKEN, TELEGRAM_TELEGRAM_CHAT_ID, tweet['text'])
                                else:
                                    tempStatus = "RT @" + tweet['user']['screen_name'] + " : " + tweet[
                                        'text'] + " via #5k6mbot"
                                    print(tempStatus.encode('utf-8'))
                                    # this code is commented because of difficult in identifying the polls. #TODO
                                    # twitter.update_status(status=tempStatus.encode('utf-8'))
                                    twitter.retweet(id=int(tweet['id']))
                                    sendtotelegram(TELEGRAM_TOKEN, TELEGRAM_TELEGRAM_CHAT_ID, tweet['text'])
                                count = count + 1
                                print('Tweet from @%s Date: %s' % (
                                tweet['user']['screen_name'].encode('utf-8'), tweet['created_at']))
                                print(tweet['text'].encode('utf-8'), '\n', polarity_result)
                            except TwythonError as e:
                                print(e)
                print("total filtered and retweeted..." + str(count))
        print("end of search")
    print("sleeping for 12 hours")
    time.sleep(21600*2)
#else:
#    print("***terminated***")
