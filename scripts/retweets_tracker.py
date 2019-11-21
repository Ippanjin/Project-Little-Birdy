import twitter
from time import time as time_now

CONSUMER_KEY = 'OmSLZHzlAonPshptklKq40PXu'
CONSUMER_SECRET ='FDDapXwQavn1hJjXVNfftqEPqmnh6ppOSyTt4ljfSGOH8IsFt9'
OAUTH_TOKEN = '1144962054475804672-1eRvXn1iWcEdOCZyq5mzhIn6L7echV'
OAUTH_TOKEN_SECRET = 'dapCBtw9xEbM5wHoPu0nuUB51CBho04ouac7a6IJ1AAer'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

tracked_tweets = []
currently_untracked_tweets = []
period_adjustment_ratio = 3
per_hour_beta = 0.75
initial_exponentially_smoothed_per_hour_rate = 5

# A function that should be called very periodically, updates some retweets when enough time has passed.
def track_tweets():
    for tweet in tracked_tweets:
        if time_now() - tweet["last_updated"] >= tweet["update_every"]:
            update_retweets(tweet)
        if time_now() - tweet["last_hour_checkpoint"] >= 3600:
            update_retweets_per_hour(tweet)

# Add the given tweet id to the list of tracked tweets.
def add_tweet_for_tracking(tweet_id, update_every = 30, start_tracking_now = True, if_previously_paused == "resume"):
    for tweet in tracked_tweets:
        if tweet["id"] == tweet_id:
            return
    for tweet in currently_untracked_tweets:
        if tweet["id"] == tweet_id:
            if if_previously_paused == "resume":
                resume_tracking(tweet["id"], tweet)
            elif if_previously_resumed == "restart":
                delete_tracked_tweet_and_all_its_retweets(tweet["id"], tweet, currently_untracked_tweets)
            return
    tweet = {}
    tweet["id"] = tweet_id
    tweet["retweets"] = twitter_api.statuses.retweets(_id = tweet_id)
    tweet["object"] = twitter_api.statuses.show(_id = tweet_id)
    tweet["last_updated"] = time_now()
    tweet["update_every"] = update_every
    tweet["last_hour_checkpoint"] = time_now()
    tweet["retweets_per_hour_list"] = []
    tweet["retweet_count_an_hour_ago"] = 0
    tweet["exponentially_smoothed_per_hour_rate"] = initial_exponentially_smoothed_per_hour_rate
    if start_tracking_now:
        tracked_tweets.append(tweet)
    else:
        not_currently_tracked_tweets.append(tweet)

def delete_tracked_tweet_and_all_its_retweets(tweet_id, tweet = None, tweets_list = tracked_tweets):
    for index, _tweet in enumerate(tweets_list):
        if _tweet["id"] == tweet_id:
            tweet = _tweet
    try:
        tweets_list.remove(tweet)
    except:
        pass

# Changes the update period of the given tweet to the given value.
def change_update_period(tweet_id, new_update_period, tweet = None):
    if tweet:
        tweet["update_every"] = new_update_period
    else:
        for tweet in tracked_tweets:
            if tweet["id"] == tweet_id:
                tweet["update_every"] = new_update_period

# Adjust the update period of the given tweet to make it suitable.
def adjust_update_period(tweet, fetched_retweets, new_retweets):
    tweet["update_every"] += period_adjustment_ratio * (fetched_retweets - new_retweets - 5)

# Updates the retweets_per_hour metric for the supplied tweet along with related stuff.
# Must be run every hour for each tracked tweet.
# Usually this is handled by track_tweets.
def update_retweets_per_hour(tweet):
    # Append the number of new tweets this hour to the relevant list.
    tweet["retweets_per_hour_list"].append(
        tweet["object"].get("retweet_count") - tweet["retweet_count_an_hour_ago"])
    # Update info for next call.
    tweet["last_hour_checkpoint"] = time_now()
    tweet["retweet_count_an_hour_ago"] = tweet["object"].get("retweet_count")
    # Update the exponentially_smoothed_per_hour_rate and if becomes below 1 untrack for now.
    tweet["exponentially_smoothed_per_hour_rate"] *= per_hour_beta
    tweet["exponentially_smoothed_per_hour_rate"] += (1 - per_hour_beta) * tweet["retweets_per_hour_list"][-1]
    if tweet["exponentially_smoothed_per_hour_rate"] < 1:
        untrack_tweet_for_now(tweet["id"], tweet)

# Moves the tweet from the list of tracked ones to the list of temporarily untracked ones.
def untrack_tweet_for_now(tweet_id, tweet = None):
    if not tweet:
        for _tweet in tracked_tweets:
            if _tweet["id"] == tweet_id:
                tweet = _tweet
    try:
        currently_untracked_tweets.append(tweet)
        tracked_tweets.remove(tweet)
    except:
        pass

# Opposite of untrack_tweet_for_now.
def resume_tracking(tweet_id, tweet = None):
    if not tweet:
        for _tweet in currently_untracked_tweets:
            if _tweet["id"] == tweet_id:
                tweet = _tweet
    try:
        tracked_tweets.append(tweet)
        currently_untracked_tweets.remove(tweet)
    except:
        pass

# Updates the retweets and other properties of the supplied tweet.
# Note that this does update the original tweet variable as it is not being reassigned.
# Make sure never to reassign the tweet variable within the function.
def update_retweets(tweet):
    last_count = tweet["object"].get("retweet_count")
    tweet["object"] = twitter_api.statuses.show(_id = tweet["id"])
    num_new_retweets = tweet["object"].get("retweet_count") - last_count
    print(tweet["id"], 'New retweets:', num_new_retweets)
    new_retweets = twitter_api.statuses.retweets(_id = tweet["id"])
    print(tweet["id"], 'Number of fetched retweets:', len(new_retweets))
    last_retweet_id = tweet["retweets"][0].get("id")
    matching_index = 100
    for i, retweet in enumerate(new_retweets):
        if retweet.get("id") == last_retweet_id:
            matching_index = i
            break
    tweet["retweets"] = new_retweets[:matching_index] + tweet["retweets"]
    print(tweet["id"], 'Retweets collected by now:', len(tweet["retweets"]))
    adjust_update_period(tweet, len(new_retweets), num_new_retweets)
    tweet["last_updated"] = time_now()
