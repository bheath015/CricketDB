import time
import json

REDIS_KEY = "SCORES"

REDIS_KEY_BAT = "BAT_SCORES"
REDIS_KEY_BOWL = "BOWL_SCORES"

CACHE_REFRESH = 5000000*1000

import redis
r = redis.Redis(host='ec2-52-205-35-60.compute-1.amazonaws.com', port=6379, db=0)

def get_norm_scores(playerListNames):

    count = len(playerListNames)

    bowlList = []
    batList = []

    bowlObject = redis_cache_bowl_cost()
    batObject = redis_cache_bat_cost()

    for name in playerListNames:
        bowlList.append(bowlObject["data"][name])
        batList.append(batObject["data"][name])

    batScore = (sum(batList) * 11.0) / count
    bowlScore = (sum(bowlList) * 11.0) / count

    return batScore, bowlScore




def redis_cache_cost():
    entry = r.get(REDIS_KEY)
    if entry is None :
        entry = score_object()
        r.set(REDIS_KEY, json.dumps(entry))
        return entry
    else:
        print "From Cache 1"
        obj = json.loads(entry)
        millis = int(round(time.time() * 1000))
        if(millis - obj["time_stamp"] < CACHE_REFRESH):
            return obj
        entry = score_object()
        r.set(REDIS_KEY, json.dumps(entry))
        return entry



def redis_cache_bowl_cost():
    entry = r.get(REDIS_KEY_BOWL)
    if entry is None :
        entry = bowl_score_object()
        r.set(REDIS_KEY_BOWL, json.dumps(entry))
        return entry
    else:
        print "From Cache 2"
        obj = json.loads(entry)
        millis = int(round(time.time() * 1000))
        if(millis - obj["time_stamp"] < CACHE_REFRESH):
            return obj
        entry = bowl_score_object()
        r.set(REDIS_KEY_BOWL, json.dumps(entry))
        return entry

def redis_cache_bat_cost():
    entry = r.get(REDIS_KEY_BAT)
    if entry is None :
        entry = bat_score_object()
        r.set(REDIS_KEY_BAT, json.dumps(entry))
        return entry
    else:
        print "From Cache 3"
        obj = json.loads(entry)
        print "Done json stuffing"
        millis = int(round(time.time() * 1000))
        if(millis - obj["time_stamp"] < CACHE_REFRESH):
            return obj
        print "From Cache 3 computing again"
        entry = bat_score_object()
        r.set(REDIS_KEY_BAT, json.dumps(entry))
        return entry


def score_object():

    score_dict = score_func()
    entry = {}
    millis = int(round(time.time() * 1000))
    entry["time_stamp"] = millis
    entry["data"] = score_dict
    return entry

def bat_score_object():

    score_dict = score_func_batscore()
    entry = {}
    millis = int(round(time.time() * 1000))
    entry["time_stamp"] = millis
    entry["data"] = score_dict
    return entry

def bowl_score_object():

    score_dict = score_func_bowlscore()
    entry = {}
    millis = int(round(time.time() * 1000))
    entry["time_stamp"] = millis
    entry["data"] = score_dict
    return entry





def score_func():
    from bs4 import BeautifulSoup
    from pymongo import MongoClient

    mongoClient = MongoClient ('ec2-52-205-35-60.compute-1.amazonaws.com:27017')

    db = mongoClient.cricket

    collection = db.player
    batTots = {}

    tot = []
    for doc in collection.find():
        soup = BeautifulSoup(doc['battingData'])
        My_table = soup.find('table',{'class':'engineTable'})
        lists = My_table.findAll('tr')
        avg = []
        sr = []
        for row in lists:
            cols=row.find_all('td')
            cols=[x.text.strip() for x in cols]
        try:
            avg = float(cols[6])
            sr = float(cols[8])
        except:
            avg = 0
            sr = 0
        batTots[doc['fullName']] = avg+sr

    from collections import OrderedDict
    d_descending = sorted(batTots, key=batTots.get, reverse=True)


    batRank = {}
    count = 1
    for i in range(len(d_descending)):
        batRank[d_descending[i]] = count
        count+=1
    batRank





    bowlTots = {}

    tot = []
    for doc in collection.find():
        soup = BeautifulSoup(doc['bowlingData'])
        My_table = soup.find('table',{'class':'engineTable'})
        lists = My_table.findAll('tr')
        avg = []
        sr = []

        for row in lists:
            cols=row.find_all('td')
            cols=[x.text.strip() for x in cols]
            if(cols==[]):
                None
            else:
                if(cols[0]=='T20s'):
                    try:
                        eco = float(cols[5])
                        srb = float(cols[10])
                    except:
                        eco = 0
                        srb = 0
        if(eco==0):
            bowlTots[doc['fullName']] = 0
        else:
            bowlTots[doc['fullName']] = eco/srb


    from collections import OrderedDict
    bowl_descending = sorted(bowlTots, key=bowlTots.get, reverse=True)

    for i in bowlTots.keys():
        if (bowlTots[i] == 0):
            bowlTots[i] = 11111


    bowlRank = {}
    count = 1
    for i in range(len(bowl_descending)):
        bowlRank[bowl_descending[i]] = count
        count+=1


    for key, values in bowlRank.items():
        if (bowlRank[key] > 422):
            bowlRank[key] = 423
    from collections import Counter
    d = Counter(batRank) + Counter(bowlRank)
    final = sorted(d, key=d.get, reverse=False)

    total = 321
    score = {}
    for i in range(len(final)):
        total = total - 0.5
        score[final[i]] = total
    return score







def score_func_batscore():
    from bs4 import BeautifulSoup
    from pymongo import MongoClient
    import math

    mongoClient = MongoClient ('ec2-52-205-35-60.compute-1.amazonaws.com:27017')

    db = mongoClient.cricket

    collection = db.player
    batTots = {}

    tot = []
    for doc in collection.find():
        soup = BeautifulSoup(doc['battingData'])
        My_table = soup.find('table',{'class':'engineTable'})
        lists = My_table.findAll('tr')
        avg = []
        sr = []
        for row in lists:
            cols=row.find_all('td')
            cols=[x.text.strip() for x in cols]
        try:
            avg = float(cols[6])
            sr = float(cols[8])
        except:
            avg = 0
            sr = 0
        batTots[doc['fullName']] = avg+sr

    max_value = max(batTots.values())
    for key, value in batTots.items():
        batTots[key] = math.ceil(value*100/(max_value))
        if(batTots[key] > 100):
            batTots[key] = 100
        batTots[key] = math.ceil(batTots[key])

    return batTots



    # Final Function


def score_func_bowlscore():
    from bs4 import BeautifulSoup
    from pymongo import MongoClient
    import math

    mongoClient = MongoClient ('ec2-52-205-35-60.compute-1.amazonaws.com:27017')

    db = mongoClient.cricket

    collection = db.player

    bowlTots = {}

    tot = []
    for doc in collection.find():
        soup = BeautifulSoup(doc['bowlingData'])
        My_table = soup.find('table',{'class':'engineTable'})
        lists = My_table.findAll('tr')
        avg = []
        sr = []

        for row in lists:
            cols=row.find_all('td')
            cols=[x.text.strip() for x in cols]
            if(cols==[]):
                None
            else:
                if(cols[0]=='T20s'):
                    try:
                        eco = float(cols[5])
                        srb = float(cols[10])
                    except:
                        eco = 0
                        srb = 0
        if(eco==0):
            bowlTots[doc['fullName']] = 0
        else:
            bowlTots[doc['fullName']] = eco/srb


    from collections import OrderedDict
    bowl_descending = sorted(bowlTots, key=bowlTots.get, reverse=True)
    max_value = max(bowlTots.values())
    for key, value in bowlTots.items():
        bowlTots[key] = math.sqrt(math.ceil(value*100/(max_value*0.8)))*10
        if(bowlTots[key] > 100):
            bowlTots[key] = 100
        bowlTots[key] = math.ceil(bowlTots[key])

    return bowlTots
