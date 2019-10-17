# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 07:17:05 2019

@author: Omar
"""
import twitter
import json
from woeid import alphSorted_woeid_list as woeid_data
import copy

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
    if not a:
        return 0
    return a


def prepare_data(entries):
    woeids = []
    for i in range(0, len(entries)):
        woeids.append(entries[i][2])

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

            for j in range(0, len(temp_block)):
                if temp_block[j]['name'][0] == '#':
                    temp_hashtags.append(temp_block[j])
                else:
                    temp_keywords.append(temp_block[j])

        entries[i].append([temp_hashtags, temp_keywords])
        entries[i][3] = "Loaded"



def prepare_one_data(entry):


    temp_block, temp_hashtags, temp_keywords = [], [], []


    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)

    temp_block = twitter_api.trends.place(_id=entry[2])

    temp_block = sorted(temp_block[0]['trends'], reverse = True, key = lambda i: nonesorter(i['tweet_volume']))

    for i in range(0, len(temp_block)):
        if temp_block[i]['name'][0] == '#':
            temp_hashtags.append(temp_block[i])
        else:
            temp_keywords.append(temp_block[i])

    data_block = [temp_hashtags, temp_keywords]

    return data_block

def printHighlights(data):
    for i in range(0, len(data)):
        print(data[i]['name'], end ='\t')
        if data[i]['tweet_volume'] != None or'tweet_volume' in data[i]:
            print(data[i]['tweet_volume'])
        else:
            print('No data')

def printHighlightsListbox(data, listbox):
    for i in range(0, len(data)):
        entry = ""

        entry += data[i]['name'] + '\t'
        if data[i]['tweet_volume'] != None or'tweet_volume' in data[i]:
            entry += data[i]['tweet_volume']
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


    for i in range(0, len(data[0][0])):
        if data[0][0][i]['name'] in common_sets[0]:
            common_data[0].append(data[0][0][i])

    for i in range(0, len(data[0][1])):
        if data[0][1][i]['name'] in common_sets[1]:
            common_data[1].append(data[0][1][i])


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

    for i in range(0, len(data_list)):

        text_data.append({'status_text': data_list[i]['text'].replace('\n', '\u000A'),
                          'screen_names': data_list[i]['entities']['user_mentions'],
                          'hashtags': data_list[i]['entities']['hashtags']})

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
