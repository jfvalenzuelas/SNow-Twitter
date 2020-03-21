import json
import os

def loadAccessData(platform):
    with open('config.json',) as json_data_file:
        data = json.load(json_data_file)[platform]
        if (platform == "twitter"):
            return data["consumer_key"], data["consumer_secret"], data["access_token"], data["access_token_secret"]
        if (platform == "ServiceNow"):
            return data["url"], data["user"], data["pwd"]
    
def loadLastId(platform):
    with open('crawler-log.json',) as json_data_file:
            data = json.load(json_data_file)[platform]
            return data["last_retrieved_id"]
        
def readCrawlerLog():
    if (os.path.exists('crawler-log.json')):
        with open('crawler-log.json', 'r+') as json_file:
            data = json.load(json_file)
            json_file.close()
        return data
    else:
        with open('crawler-log.json', 'a+') as json_file:
            return {}
        
def writeCrawlerLog(platform, newData):
    logData = readCrawlerLog()
    if (logData):
        tmp = logData[platform]
        logData[platform] = newData
        
        with open('crawler-log.json', 'w') as json_file:
            json.dump(logData, json_file)
            json_file.close()
    else:
        logData[platform] = newData
        with open('crawler-log.json', 'w') as json_file:
            json.dump(logData, json_file)
            json_file.close()
                        
def crawlTwitter(api, q, mode, since_id):
    #results = api.search(q=q, since_id=since_id,tweet_mode=mode, result_type="recent")
    results = api.search(q=q, since_id=since_id, tweet_mode=mode, result_type="recent", count=500)
    return results