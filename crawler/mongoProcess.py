import json
import pymongo

myclient = pymongo.MongoClient("mongodb://ec2-52-205-35-60.compute-1.amazonaws.com:27017/")
mydb = myclient["cricket"]
mycol = mydb["player"]


fp = open("pDetails_itr2.json", "r");
data = fp.read()
jsonData = json.loads(data);
entryKeys = jsonData.keys()

for key in entryKeys:
	value = jsonData[key]
	mycol.insert_one(value)
