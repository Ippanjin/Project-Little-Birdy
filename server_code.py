# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 07:17:05 2019

@author: Omar
"""
try:
    import os
    os.chdir("D:\(PC)\Desktop\Coding\Python\Twitter prototype\github\Twitter-prototype")
except:
    pass
import twitter
import json
from urllib.parse import unquote
from woeid import alphSorted_woeid_list as woeid_data
import copy
import webbrowser as browser
from time import time as time_now

init_data = {
'CONSUMER_KEY':'OmSLZHzlAonPshptklKq40PXu',
'CONSUMER_SECRET': 'FDDapXwQavn1hJjXVNfftqEPqmnh6ppOSyTt4ljfSGOH8IsFt9',
'OAUTH_TOKEN' : '1144962054475804672-1eRvXn1iWcEdOCZyq5mzhIn6L7echV',
'OAUTH_TOKEN_SECRET' : 'dapCBtw9xEbM5wHoPu0nuUB51CBho04ouac7a6IJ1AAer'
}

CONSUMER_KEY = 'OmSLZHzlAonPshptklKq40PXu'
CONSUMER_SECRET ='FDDapXwQavn1hJjXVNfftqEPqmnh6ppOSyTt4ljfSGOH8IsFt9'
OAUTH_TOKEN = '1144962054475804672-1eRvXn1iWcEdOCZyq5mzhIn6L7echV'
OAUTH_TOKEN_SECRET = 'dapCBtw9xEbM5wHoPu0nuUB51CBho04ouac7a6IJ1AAer'

data = [['Consumer key: ', 'OmSLZHzlAonPshptklKq40PXu'],
        ['Consumer secret: ', 'FDDapXwQavn1hJjXVNfftqEPqmnh6ppOSyTt4ljfSGOH8IsFt9'],
        ['OAUTH token: ', '1144962054475804672-1eRvXn1iWcEdOCZyq5mzhIn6L7echV'],
        ['OAUTH token secret: ', 'dapCBtw9xEbM5wHoPu0nuUB51CBho04ouac7a6IJ1AAer']]



WORLD_WOE_ID = 1
SENDAI_WOE_ID = woeid_data['Japan']['cities']['Sendai']['woeid']



def nonesorter(a):
    return a or 0


def get_preview_tweets(query, count):
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    # TODO: modify query to exclude retweets.
    search_results = twitter_api.search.tweets(q = query, count = count, result_type = "recent")
    statuses = search_results['statuses']
    while len(statuses) < count:
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError:
            break
        kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split("&") ])
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

    return statuses if len(statuses) <= 3 else statuses[:3]


def prepare_data(entries):
    woeids = []
    for entry in entries:
        woeids.append(entry[2])

    print(woeids)
    for i in range(0, len(woeids)):

        if entries[i][3] == "Loaded":
            continue

        else:
            temp_block, temp_hashtags, temp_keywords = [], [], []


            auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
            twitter_api = twitter.Twitter(auth=auth)

            temp_block = twitter_api.trends.place(_id=woeids[i])

            temp_block = sorted(temp_block[0]['trends'], reverse = True, key = lambda i: nonesorter(i['tweet_volume']))

            for temp in temp_block:
                if temp['name'][0] == '#':
                    temp_hashtags.append(temp)
                else:
                    temp_keywords.append(temp)

        entries[i].append([temp_hashtags, temp_keywords])
        entries[i][3] = "Loaded"



def prepare_one_data(entry):


    temp_block, temp_hashtags, temp_keywords = [], [], []


    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)

    temp_block = twitter_api.trends.place(_id=entry[2])

    temp_block = sorted(temp_block[0]['trends'], reverse = True, key = lambda i: nonesorter(i['tweet_volume']))

    for temp in temp_block:
        if temp['name'][0] == '#':
            temp_hashtags.append(temp)
        else:
            temp_keywords.append(temp)

    data_block = [temp_hashtags, temp_keywords]

    return data_block

def printHighlights(data):
    for tweet in data:
        print(tweet['name'], end ='\t')
        if tweet['tweet_volume'] != None or'tweet_volume' in tweet:
            print(tweet['tweet_volume'])
        else:
            print('No data')

def printHighlightsListbox(data, listbox):
    for tweet in data:
        entry = ""

        entry += tweet['name'] + '\t'
        if tweet['tweet_volume'] != None or'tweet_volume' in tweet:
            entry += tweet['tweet_volume']
        else:
            entry += 'No data'

        listbox.insert(tk.END, entry)


def get_common_data(data):

    common_sets, common_data = [], [[],[]]
    common_sets.append(set([item['name'] for item in data[0][0]]))
    common_sets.append(set([item['name'] for item in data[0][1]]))


    for i in range(1, len(data)):
        common_sets[0] &= set([item['name'] for item in data[i][0]])
        common_sets[1] &= set([item['name'] for item in data[i][1]])


    common_sets = [list(common_sets[0]), list(common_sets[1])]


    for tweet in data[0][0]:
        if tweet['name'] in common_sets[0]:
            common_data[0].append(tweet)

    for tweet in data[0][1]:
        if tweet['name'] in common_sets[1]:
            common_data[1].append(tweet)


    return common_data





def prepare_statuses(data_list):

    statuses = data_list['statuses']


    # Iterate through 5 more batches of results by following the cursor
    for _ in range(5):

        try:
            next_results = data_list['search_metadata']['next_results']
        except KeyError as e: # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=847960489447628799&q=%23RIPSelena&count=100&include_entities=1
        kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split("&") ])

        data_list = twitter_api.search.tweets(**kwargs)
        statuses += data_list['statuses']

    return statuses


def get_text_data(data_list):

    text_data = []

    for item in data_list:

        text_data.append({'status_text': item['text'].replace('\n', '\u000A'),
                          'screen_names': item['entities']['user_mentions'],
                          'hashtags': item['entities']['hashtags']})

    return text_data



"""
data = prepare_data([["","", 1118129],
                     ["","", 1118370],
                     ["","", 15015372]
                     ])

printHighlights(data[0][0])
print("************")
printHighlights(data[1][0])
print("************")
printHighlights(data[2][0])



common_data = get_common_data(data)
print("************")
print("************")
printHighlights(common_data[0])
print("************")
printHighlights(common_data[1])


world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
sendai_trends = twitter_api.trends.place(_id=SENDAI_WOE_ID)

sorted_all = sorted(sendai_trends[0]['trends'], reverse = True, key = lambda i: nonesorter(i['tweet_volume']))

sorted_hashtags, sorted_keywords = [], []


for i in range(0, len(sorted_all)):
    if sorted_all[i]['name'][0] == '#':
        sorted_hashtags.append(sorted_all[i])
    else:
        sorted_keywords.append(sorted_all[i])


for i in range(0, len(sorted_hashtags)):
    print(sorted_hashtags[i]['name'], end ='\t')
    if 'tweet_volume' in sorted_hashtags[i]:
        print(sorted_hashtags[i]['tweet_volume'])
    else:
        print('No data')


for i in range(0, len(sorted_keywords)):
    print(sorted_keywords[i]['name'], end ='\t')
    if 'tweet_volume' in sorted_all[i]:
        print(sorted_keywords[i]['tweet_volume'])
    else:
        print('No data')


#get the nth rank hashtag or tweet keyword
hashtag = sorted_hashtags[0]['name']
keyword = sorted_keywords[0]['name']

count = 100



hashtag_search_results = twitter_api.search.tweets(q=hashtag, count=count)
keyword_search_results = twitter_api.search.tweets(q=keyword, count=count)


hashtag_statuses = prepare_statuses(hashtag_search_results)
keyword_statuses = prepare_statuses(keyword_search_results)



hashtag_text_data = get_text_data(hashtag_statuses)

for i in range(0, len(hashtag_text_data)):
    if hashtag_text_data[i]['screen_names']:
        print("Status %d" % i)
        print(hashtag_text_data[i]['screen_names'][0]['screen_name'])
    else:
        continue
    print()
"""

tracked_tweets = []

def track_tweets():
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    for tweet in tracked_tweets:
        if time_now() - tweet["last_updated"] >= tweet["update_every"]:
            update_retweets(tweet)

def add_tweet_for_tracking(tweet_id, update_every = 5):
    tweet = {}
    tweet["id"] = tweet_id
    tweet["retweets"] = twitter_api.statuses.retweets(_id = tweet_id)
    tweet["object"] = tweet_api.statuses.show(_id = _id)
    tweet["last_updated"] = time_now()
    tweet["update_every"] = update_every
    tracked_tweets.append(tweet)

def update_retweets(tweet):
    last count = tweet["object"].get("retweet_count")
    tweet["object"] = tweet_api.statuses.show(_id = tweet["id"])
    print('New retweets:', tweet["object"].get("retweet_count") - last_count)
    new_retweets = twitter_api.statuses.retweets(_id = tweet["id"])
    print('Number of fetched retweets:', len(new_retweets))
    last_retweet_id = tweet["retweets"][0].get("id")
    matching_index = 100
    for i, retweet in enumerate(new_retweets):
        if retweet.get("id") == last_retweet_id:
            matching_index = i
    tweet["retweets"] = new_retweets[:matching_index] + tweet["retweets"]

def main():
    pass

if __name__ == "__main__":
    main()
