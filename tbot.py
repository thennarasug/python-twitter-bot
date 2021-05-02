import datetime as dt
# TelegramBot
# heroku env variables
from os import environ

import telepot
import logging
# Import a text processing library
from textblob import TextBlob
# Twython twitter api
from twython import Twython, TwythonError

import time
import traceback
import sqlite3
import Logger as log

log.basicconfig("tbot", level=logging.INFO)

'''
#no more command line or dynamic arguments, just kept it for reference.

keywords = input("twitter search keyword? ")
rt_fav_limit = input("max retweet_count or favorite_count? ")
'''

def create_table():
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tbot_tweet_id (id string primary key)")
    c.execute("CREATE TABLE IF NOT EXISTS tbot_followback_id (id string primary key)")
    c.execute("CREATE TABLE IF NOT EXISTS tbot_unfollow_id (id string primary key)")
    try:
        db.commit()
    except:
        db.rollback()


def insert_error_string(id):
    c = db.cursor()
    try:
        vals = [id]
        query = "INSERT INTO tbot_tweet_id (id) VALUES (?)"
        c.execute(query, vals)
        db.commit()
    except sqlite3.IntegrityError as i:
        pass
    except:
        error = traceback.print_exc()
        db.rollback()


def insert_followbackid(id):
    c = db.cursor()
    try:
        vals = [id]
        query = "INSERT INTO tbot_followback_id (id) VALUES (?)"
        c.execute(query, vals)
        db.commit()
    except sqlite3.IntegrityError as i:
        pass
    except:
        error = traceback.print_exc()
        db.rollback()


def insert_unfollowid(id):
    c = db.cursor()
    try:
        vals = [id]
        query = "INSERT INTO tbot_followback_id (id) VALUES (?)"
        c.execute(query, vals)
        db.commit()
    except sqlite3.IntegrityError as i:
        pass
    except:
        error = traceback.print_exc()
        db.rollback()


def select_error_string(id):
    try:
        query = "select count(*) from tbot_tweet_id where id = '{}'".format(id)
        cursor = db.execute(query)
        db.commit()
        return cursor
    except:
        error = traceback.print_exc()
        db.rollback()
        return None


def select_followbackid_string(id):
    try:
        query = "select count(*) from tbot_followback_id where id = '{}'".format(id)
        cursor = db.execute(query)
        db.commit()
        return cursor
    except:
        error = traceback.print_exc()
        db.rollback()
        return None


def select_followbackid_all():
    try:
        query = "select * from tbot_followback_id"
        cursor = db.execute(query)
        db.commit()
        return cursor
    except:
        error = traceback.print_exc()
        db.rollback()
        return None


def select_unfollowid_string(id):
    try:
        query = "select count(*) from tbot_unfollow_id where id = '{}'".format(id)
        cursor = db.execute(query)
        db.commit()
        return cursor
    except:
        error = traceback.print_exc()
        db.rollback()
        return None

# TelegramBot method
def sendtotelegram(TELEGRAM_TOKEN, TELEGRAM_TELEGRAM_CHAT_ID, tweetToTelegram):
    TelegramBot = telepot.Bot(TELEGRAM_TOKEN)
    chat_id = TELEGRAM_TELEGRAM_CHAT_ID
    # aboutme = TelegramBot.getMe()
    # print (TelegramBot.getMe())
    # messages = TelegramBot.getUpdates()
    # for message in messages:
    #    chat_id = message["message"]["from"]["id"]
    # print(chat_id)

    TelegramBot.sendMessage(chat_id, tweetToTelegram)
    log.loginfo("****updated TelegramBot****")
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


keywords_rt_fav_limits_all = [[50, ['signalapp', 'degoogle', 'f-droid', 'pinebook', 'pine64', 'pinephone', 'Yubico']], [50, ['algotrading']], [100, ['tutanota', 'protonmail', 'duckduckgo', 'protonvpn', 'tails OS', 'tor browser', 'manjarolinux', 'manjaro']], [150, ['linux', 'ubuntu']]]


# for database
dbfilewithpath = "./tbot.db"
db = sqlite3.connect(dbfilewithpath)

create_table()

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

def tweetfromfile():
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


def autofollowback():
    try:
        followers = twitter.get_followers_ids(screen_name = "5k6m")
        for followbackid in followers['ids']:
            try:
                cursor = select_followbackid_string(followbackid)
                for row in cursor:
                    if row[0] == 0:
                        twitter.create_friendship(user_id=followbackid)
                        insert_followbackid(followbackid)
                        print("followback -->", followbackid)
                        time.sleep(1.5)
            except TwythonError as e:
                print("error on followback", followbackid, e)
    except TwythonError as e:
        #insert_error_string(tweet['id'])
        print("error on get_followers_ids", e)
    except Exception as e:
        print("Exception", e)


def autounfollow():
    try:
        followers = twitter.get_followers_ids(screen_name = "5k6m")
        followersfromdb_cursor = select_followbackid_all()
        for id in followersfromdb_cursor:
            if id[0] not in followers['ids']:
                try:
                    twitter.destroy_friendship(user_id=id)
                    insert_followbackid(id)
                except TwythonError as e:
                    print("error on followback", id, e)
    except TwythonError as e:
        #insert_error_string(tweet['id'])
        print("error on get_followers_ids", e)
    except Exception as e:
        print("Exception", e)


#no db flow
def autofollowandunfollow():

    followcount = 0
    followerrorcount = 0
    unfollowcount = 0
    unfollowerrorcount = 0


    # follow
    try:
        followers = twitter.get_followers_ids(screen_name = "5k6m")
        following = twitter.get_friends_ids(screen_name = "5k6m")
        for followbackid in followers['ids']:
            try:
                if followbackid not in following['ids']:
                    twitter.create_friendship(user_id=followbackid)
                    print("followback -->", followbackid)
                    time.sleep(1.5)
                followcount = followcount+1
            except TwythonError as e:
                #print("error on followback", followbackid, e)
                followerrorcount = followerrorcount+1
    except TwythonError as e:
        print(e)
    except Exception as e:
        print("Exception", e)

    log.loginfo("followcount " + str(followcount) + " | followerrorcount " + str(followerrorcount) + " --> sleeping for 10sec")
    print(dt.datetime.now(), "followcount " + str(followcount) + " | followerrorcount " + str(followerrorcount) + " --> sleeping for 10sec")
    time.sleep(10)

    '''
    # unfollow
    # lookup_friendships
    try:
        followers = twitter.get_followers_ids(screen_name = "5k6m")
        following = twitter.get_friends_ids(screen_name = "5k6m")
        for unfollowid in following['ids']:
            try:
                lookup_friendships = twitter.lookup_friendships(user_id=unfollowid)
                if (unfollowid not in followers['ids']) and (lookup_friendships['relationship']['target']['following_received'] == False):
                    twitter.destroy_friendship(user_id=unfollowid)
                    print("unfollow -->", unfollowid)
                    time.sleep(1.5)
                    unfollowcount = unfollowcount+1
            except TwythonError as e:
                #print("error on unfollow", unfollowid, e)
                unfollowerrorcount = unfollowerrorcount+1
    except TwythonError as e:
        print(e)
    except Exception as e:
        print("Exception", e)

    log.loginfo("unfollowcount " + str(unfollowcount) + " | unfollowerrorcount " + str(unfollowerrorcount) + " --> sleeping for 5min")
    print(dt.datetime.now(), "unfollowcount " + str(unfollowcount) + " | unfollowerrorcount " + str(unfollowerrorcount) + " --> sleeping for 5min")
    '''

# indefinite while loop that runs every 1 hour. To remove the dependency on scheduler.
while True:
    log.loginfo("*****************************triggered*****************************")
    print(dt.datetime.now(), "*****************************triggered*****************************")
    try:
        #autofollowback()
        #autounfollow()
        autofollowandunfollow()
    except:
        pass
    for keywords_rt_fav_limits_entry in keywords_rt_fav_limits_all:
        rt_fav_limit = keywords_rt_fav_limits_entry[0]
        keywords = keywords_rt_fav_limits_entry[1]
        search_results = ""
        for keyword in keywords:
            for lang_list in ['en', 'ta']:
                for result_type in ['popular', 'recent']:
                    try:
                        # count=100 max (default 15), result_type='mixed' or 'recent'
                        # count=15 max (default 15), result_type='popular'
                        # print ("search twitter......", keyword, " in ", lang_list, " with max_limit as ", rt_fav_limit)
                        search_results = twitter.search(q=keyword, count=100, lang=lang_list, result_type=result_type)
                        # print (search_results)

                        if len(search_results) > 0:
                            count = 0
                            for tweet in search_results['statuses']:
                                if "RT @" not in tweet['text'] and (tweet['favorite_count'] >= int(rt_fav_limit) or tweet['retweet_count'] >= int(rt_fav_limit)) and tweet['retweeted'] == False and tweet['is_quote_status'] == False:  # and tweet['possibly_sensitive'] == False:
                                    polarity_result = analysis(tweet['text'])
                                    if polarity_result >= 0.15 or lang_list == 'ta':
                                        try:
                                            cursor = select_error_string(tweet['id'])
                                            for row in cursor:
                                                if row[0] == 0:
                                                    if len(tweet['text']) > 200 or "https" in tweet['text']:
                                                        twitter.retweet(id=int(tweet['id']))
                                                        log.loginfo(tweet['text'])
                                                        print(tweet['text'])
                                                        sendtotelegram(TELEGRAM_TOKEN, TELEGRAM_TELEGRAM_CHAT_ID, tweet['text'])
                                                        time.sleep(5)
                                                    else:
                                                        tempStatus = "RT @" + tweet['user']['screen_name'] + " : " + tweet['text'] + " via #5k6mbot"
                                                        # this code is commented because of difficult in identifying the polls. #TODO
                                                        # twitter.update_status(status=tempStatus.encode('utf-8'))
                                                        twitter.retweet(id=int(tweet['id']))
                                                        sendtotelegram(TELEGRAM_TOKEN, TELEGRAM_TELEGRAM_CHAT_ID, tweet['text'])
                                                        log.loginfo(tempStatus.encode('utf-8'))
                                                        print(tempStatus.encode('utf-8'))
                                                        time.sleep(5)
                                                    count = count + 1
                                                    # print ('Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'),tweet['created_at']))
                                                    # print (tweet['text'].encode('utf-8'), '\n', polarity_result)
                                        except TwythonError as e:
                                            if "You have already retweeted this Tweet" in str(e):
                                                insert_error_string(tweet['id'])
                                                #print("error on action", tweet['id'], e)
                                            else:
                                                log.logcritical("error on action ", e)
                                                print("error on action ", e)
                            # print ("total filtered and retweeted..." + str(count))
                    # added this to avoid "Twitter API returned a 429 (Too Many Requests), Rate limit exceeded"
                    except TwythonError as e:
                        print("error on search ", e)
                time.sleep(10)
        # print ("end of search")
    log.loginfo("*****************************sleeping for 30min*****************************")
    print(dt.datetime.now(), "*****************************sleeping for 30min*****************************")
    time.sleep(1800)

