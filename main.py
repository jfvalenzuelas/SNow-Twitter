import utils
import time
import datetime
import tweepy
import requests

# Twitter Credentials
consumer_key, consumer_secret, access_token, access_token_secret = utils.loadAccessData("twitter")
snowUrl, snowUser, snowPwd = utils.loadAccessData("ServiceNow")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


print("SOURCE: Twitter Crawler\nSTATUS: Initialized\n")

while(True):
    print("SOURCE: Twitter Crawler\nSTATUS: Running\n")

    last_retrieved_id = utils.loadLastId("twitter")

    print("SOURCE: Twitter Crawler\nSTATUS: Running\nINFO: Last retrieved ID -> "+str(last_retrieved_id)+"\n")

    tweet_ids = []
    tweets = []
    users = []

    for item in utils.crawlTwitter(api, "servicenow -filter:retweets", last_retrieved_id):

        tweet_ids.append(item.id)

        tweet = {}
        tweet["id"] = item.id
        tweet["text"] = item.text
        tweet["lang"] = item.lang
        tweet["created_at"] = str(item.created_at)
        tweet["user_location"] = item.user.location
        tweet["user"] = item.user.id
        tweet["processed"] = 0
        tweet["category"] = "UNDEFINED"

        tweets.append(tweet)
        
        user = {}
        user["id"] = item.user.id
        user["description"] = item.user.description
        user["followers"] = item.user.followers_count
        user["friends"] = item.user.friends_count
        user["tweets_count"] = 0
        
        users.append(user)

    print("SOURCE: Crawler\nSTATUS: Writting Crawler Log\n")
    if (len(tweet_ids) > 0):
        last_retrieved_id = max(tweet_ids)
        utils.writeCrawlerLog("twitter", {"last_retrieved_id":last_retrieved_id})
        
        logText = "SOURCE: Crawler\nINFO: " + str(len(tweets)) + " Tweets Collected, " + str(len(users)) + " Users Collected. Last retrieved Tweet's ID: " + str(last_retrieved_id)+"\nDATE: "+str(datetime.datetime.now())+"\n"
        print(logText)
    else:
        logText = "SOURCE: Crawler\nINFO: No new Tweets were found\nDATE: "+str(datetime.datetime.now())+"\n"
        print(logText)

    response = requests.post(url=snowUrl+"/tweets", auth=(snowUser, snowPwd), headers=headers, json={"tweets":tweets})

    print(response.text)

    print("SOURCE: Crawler\nSTATUS: Waiting")
    time.sleep(300)
    

































#failed_requests = []
#headers = {
#    "Content-Type": "application/json",
#    "Accept": "application/json",
#}

#Load Twitter API Tokens and Secrets
#Retrieve Tweets
#tweets = [{"tweet"}]
#Process each Tweet with spaCy
#for tweet in tweets:
#    data = {
#        "tweet_id": "",
#        "user_id": "",
#        "created_at": "",
#        "language": "",
#        "user_location": "",
#        "original_text": "",
#        "processed_text": ""
#    }

#    response = requests.post(url=url, auth=(user, pwd), headers=headers, json=data)
#    print(response.headers)
#    print(response)
#    if (response.status_code != 200):
#        failed_requests.append(data)

#Send Original Information and Processed Tweet to Instance

#Wait 5 Minutes
