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

all_tweets = []
all_users = []

while(True):
    try:
        print("SOURCE: Twitter Crawler\nSTATUS: Running\n")

        last_retrieved_id = utils.loadLastId("twitter")

        print("SOURCE: Twitter Crawler\nSTATUS: Running\nINFO: Last retrieved ID -> "+str(last_retrieved_id)+"\n")

        tweet_ids = []
        tweets = []
        users = []

        for item in utils.crawlTwitter(api, "servicenow -filter:retweets", "extended", last_retrieved_id): 
            tweet_ids.append(item.id)

            tweet = {}
            tweet["id"] = str(item.id)
            tweet["text"] = item.full_text
            tweet["lang"] = item.lang
            tweet["created_at"] = str(item.created_at)
            tweet["user"] = str(item.user.id)

            tweets.append(tweet)
            
            user = {}
            user["id"] = str(item.user.id)
            user["description"] = item.user.description
            user["followers"] = item.user.followers_count
            user["friends"] = item.user.friends_count
            user["location"] = item.user.location
            
            users.append(user)

        print("SOURCE: Crawler\nSTATUS: Writting Crawler Log\n")
        if (len(tweet_ids) > 0):
            last_retrieved_id = max(tweet_ids)
            utils.writeCrawlerLog("twitter", {"last_retrieved_id":last_retrieved_id})
            
            logText = "SOURCE: Crawler\nINFO: " + str(len(tweets)) + " Tweets Collected, " + str(len(users)) + " Users Collected. Last retrieved Tweet's ID: " + str(last_retrieved_id)+"\nDATE: "+str(datetime.datetime.now())+"\n"
            print(logText)

            all_tweets.extend(tweets)
            all_users.extend(users)

            response = requests.post(url=snowUrl+"/users", auth=(snowUser, snowPwd), headers=headers, json={"system": "RPI00001", "users":all_users})
            print(response)

            if ("hibernating" in response.text.lower() or response.status_code != 200):
                logText = "SOURCE: Crawler\nINFO: Instance is Hibernating. Tweets will be POSTED with the next Request"
            else:
                logText = "SOURCE: Crawler\nINFO: Users were POSTED correctly"
                print(logText)
                all_users = []

                response = requests.post(url=snowUrl+"/tweets", auth=(snowUser, snowPwd), headers=headers, json={"system": "RPI00001", "topic": "servicenow", "tweets":all_tweets})
                print(response)

                if ("hibernating" in response.text.lower() or response.status_code != 200):
                    logText = "SOURCE: Crawler\nINFO: Instance is Hibernating. Tweets will be POSTED with the next Request"
                    print(logText)
                else:
                    logText = "SOURCE: Crawler\nINFO: Tweets were POSTED correctly"
                    print(logText)
                    all_tweets = []
        else:
            logText = "SOURCE: Crawler\nINFO: No new Tweets were found\nDATE: "+str(datetime.datetime.now())+"\n"
            print(logText)

        print("SOURCE: Crawler\nSTATUS: Waiting 5 Minutes")
        time.sleep(300)
    except Exception as e:
        print("ERROR: "+e)
        continue
