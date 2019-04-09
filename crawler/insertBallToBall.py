import mysql.connector

cnx = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")
cursor = cnx.cursor()
from os import listdir
from os.path import isfile, join
import yaml
from multiprocessing.dummy import Pool as ThreadPool
import pickle
from datetime import date, datetime, timedelta



cursor.execute("SELECT * FROM player")

myresult = cursor.fetchall()

playerSnameToID = {}
playerIdToSname = {}

for x in myresult:
	playerSnameToID[x[2]] = x[0]
	playerIdToSname[x[0]] = x[2]

cursor.execute("SELECT * FROM team")

myresult = cursor.fetchall()


teamNametoId = {}
teamIdtoName = {}

for x in myresult:
	teamNametoId[x[1]] = x[0]
	teamIdtoName[x[0]] = x[1]

cursor.execute("SELECT * FROM `match`")
myresult = cursor.fetchall()

matchIdToInt = {}
matchIntToId = {}

for x in myresult:
	matchIdToInt[x[-1]] = x[0]
	matchIntToId[x[0]] = x[-1]



import csv
csv_reader = None
csv_file =  open('Ball_By_Ball.csv')
csv_reader = csv.reader(csv_file, delimiter=',')


sql1 = "INSERT INTO ballToBall values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

sql2 = "INSERT INTO ballExtra values (%s, %s, %s, %s, %s, %s)"

folderPath = "/Users/nikhilt/Desktop/tmp/ipl"
onlyfiles = [f.split(".")[0] for f in listdir(folderPath) if isfile(join(folderPath, f))]
allfiles = []

allData = None
with open("allData.pkl") as fp:
	allData = pickle.load(fp)

allDatTemp = [] 

count = 0
for entry in allData:
	if isinstance(entry, dict):
		allDatTemp.append(entry)
		allfiles.append(onlyfiles[count])
	count += 1

allData = allDatTemp
onlyfiles = allfiles



def getplayerSnameToID(string):
	if(string == "Niraj Patel"):
		string = "NK Patel"
	elif(string == "Harmeet Singh (2)"):
		string = "Harmeet Singh"
	return playerSnameToID[string]

def getOverAndBallId(floatNumber):
	s = str(floatNumber)
	over = s.split(".")[0]
	ballId = s.split(".")[1]
	return over, ballId

def getRecordsForInnings(inningsEntry, inningsNumber, matchId):

	deliveries = inningsEntry["deliveries"]
	records = []
	extrasEntries = []
	recordMap = {}
	for ball in deliveries:
		key = ball.keys()[0]
		over, ballId = getOverAndBallId(key)
		temp_key = over + "_" + ballId
		if(temp_key not in recordMap):
			recordMap[temp_key] = 1
		else:
			ballId = ballId + "0"
			temp_key = over + "_" + ballId
			recordMap[temp_key] = 1



		entry = ball[key]
		striker = getplayerSnameToID(entry["batsman"])
		non_striker = getplayerSnameToID(entry["non_striker"])
		bowler = getplayerSnameToID(entry["bowler"])
		batsmanScore = entry["runs"]["batsman"]
		outputType = None
		try:
			outputType = entry["wicket"]["kind"]
		except:
			outputType = "Not Applicable"


		tmpEntry = (matchId, over, ballId, inningsNumber, striker, non_striker, bowler, batsmanScore, outputType)

		try:
			extraKeys = entry["extras"].keys()
			for key in extraKeys:
				extraEntry = (matchId, over, ballId, inningsNumber, key, entry["extras"][key])
				extrasEntries.append(extraEntry)
		except:
			a = 1


		records.append(tmpEntry)

	return records, extrasEntries




def getBallRecord(matchEntry, matchIdString):
	matchId = matchIdToInt[matchIdString]
	count = 1
	allRecords = []
	for innings in matchEntry["innings"]:
		inningsEntry = matchEntry["innings"][count-1].values()[0]
		print matchIdString
		aa, bb = getRecordsForInnings(inningsEntry, count, matchId)
		for a in aa:
			cursor.execute(sql1, a)

		for b in bb:
			cursor.execute(sql2, b)

		count += 1
		if(count > 2):
			break

count = 0;
for entry in allData:
	#print onlyfiles[count] 
	getBallRecord(entry, onlyfiles[count])
	count += 1

# count =0
# for ballEntry in csv_reader:
# 	if(count == 0):
# 		count += 1
# 		continue
# 	rec = getBallRecord(ballEntry)
# 	#print sql% rec
# 	#cursor.execute(sql, rec)
# 	count += 1

cnx.commit()
# csv_file.close()





