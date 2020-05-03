# Import a text processing library
from textblob import TextBlob

#Twython twitter api
from twython import Twython, TwythonError

import time

keyword = input("twitter search keyword? ")
max_limit = input("max retweet_count or favorite_count? ")

# Analysis method
def analysis(sentence):
   # for sentence in sentences:
        # Instantiate TextBlob
        analysis = TextBlob(sentence)
        # Parts of speech
        #print("{}\n\nParts of speech:\n{}\n".format(sentence, analysis.tags))
        # Sentiment analysis
        sentiment=analysis.sentiment
        #print("Sentiment:\n{}\n\n".format(sentiment))
        return sentiment.polarity

#add your details here
APP_KEY = 'xxxxxxx'
APP_SECRET = 'yyyyyy'
OAUTH_TOKEN = 'zzzzzz'
OAUTH_TOKEN_SECRET = 'xyzxyz'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#results = twitter.cursor(twitter.search, q='fiveperfectmovies')
#for result in results:
#    print(result['id_str'] + " : " + result['text'])

#print (twitter.search(q='fiveperfectmovies'))

with open('/storage/emulated/0/Download/pythontwitterbot/tweetthis.txt', 'r+') as tweetfile:
	buff = tweetfile.readlines()

for line in buff[:]:
	line = line.strip(r'\n')
	if len(line)<=280 and len(line)>0:
		print ("Tweeting...")
		try:
			twitter.update_status(status=line)
		except TwythonError as e:
			print (e)
		with open ('liners.txt','w') as tweetfile:
			buff.remove(line)
			tweetfile.writelines(buff)
		time.sleep(1)
	else:
		with open ('liners.txt', 'w') as tweetfile:
			buff.remove(line)
			tweetfile.writelines(buff)
		print ("Skipped line - Too long for a tweet!")
		continue

for lang_list in ['en','ta']:
    try:
        #count=100 max (default 15), result_type='mixed' or 'recent'
        #count=15 max (default 15), result_type='popular'
        print ("search twitter......", keyword, " in ", lang_list, " with max_limit as ", max_limit)
        search_results = twitter.search(q=keyword,count=100, lang=lang_list, result_type='popular')
    except TwythonError as e:
        print (e)

    count=0
    #print(search_results)
    for tweet in search_results['statuses']:
        if  "RT @" not in tweet['text'] and (tweet['favorite_count'] >= int(max_limit) or tweet['retweet_count'] >= int(max_limit)) and tweet['retweeted'] == False and tweet['is_quote_status'] == False :#and tweet['possibly_sensitive'] == False:
            polarity_result = analysis(tweet['text'])
            #print (tweet['retweeted'],tweet['is_quote_status'])
            if  polarity_result >= 0.25 :
                try:
                    #twitter.update_status(status=tweet['text'].encode('utf-8'))
                    twitter.retweet(id=int(tweet['id']))
                    count = count +1
                    print ('Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'),tweet['created_at']))
                    print (tweet['text'].encode('utf-8'), '\n', polarity_result)
                    #print (tweet['text'], '\n')
                    #print(tweet)
                except TwythonError as e:
                    print (e)
    print ("total filtered and retweeted..." + str(count))
print ("end of search")
