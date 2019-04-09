import mysql.connector

cnx = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")
cursor = cnx.cursor()
from os import listdir
from os.path import isfile, join
import yaml
from multiprocessing.dummy import Pool as ThreadPool
import pickle
from datetime import date, datetime, timedelta


teamsData = set([])

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


sql = "INSERT INTO `match` (team1, team2, date, year, venue, city, country, tossWinner, matchWinner, tossDecision, winType, outcomeType, margin, playerOfTheMatch, tempKey) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

import csv
csv_reader = None
csv_file =  open('Match.csv')
csv_reader = csv.reader(csv_file, delimiter=',')



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


def getDateObject(dateString):

	de = dateString.split("/")
	return date(int(de[2]), int(de[0]), int(de[1]))




def getMatchRecord(matchEntry, matchId):

	tempKey = matchId
	team1 = teamNametoId[matchEntry["info"]["teams"][0]]
	team2 = teamNametoId[matchEntry["info"]["teams"][1]]
	dateObject = matchEntry["info"]["dates"][0]
	year = dateObject.year
	venue = matchEntry["info"]["venue"]
	city = None
	try:
		city = matchEntry["info"]["city"]
	except:
		city = None

	country = "India"

	tossWinner = None
	try:
		tossWinner = teamNametoId.get(matchEntry["info"]["toss"]["winner"])
	except:
		tossWinner = None

	matchWinner = None
	try:
		matchWinner = teamNametoId.get(matchEntry["info"]["outcome"]["winner"])
	except:
		matchWinner = None
	
	tossDecision = None
	try:
		tossDecision = matchEntry["info"]["toss"]["decision"]
	except:
		tossDecision = None
	
	winType = None
	try:
		winType = matchEntry["info"]["outcome"]["by"].keys()[0]
	except:
		print matchEntry["info"]["outcome"]

	outcomeType = None
	try:
		outcomeType = matchEntry["info"]["result"]
	except:
		outcomeType = "Result"


	playerOfTheMatch = None
	try:
		playerOfTheMatch = playerSnameToID.get(matchEntry["info"]["player_of_match"][0])
	except:
		playerOfTheMatch = None

	margin = None
	try:
		margin = matchEntry["info"]["outcome"]["by"].values()[0]
		margin = int(margin)
	except:
		margin = None

	return team1, team2, dateObject, year, venue, city, country, tossWinner, matchWinner, tossDecision, winType, outcomeType, margin, playerOfTheMatch, tempKey




count = 0;
for entry in allData:
	rec = getMatchRecord(entry, onlyfiles[count])
	cursor.execute(sql, rec)
	count += 1

cnx.commit()
csv_file.close()


# def getMatchRecord(matchEntry):

# 	tempKey = matchEntry[1]
# 	team1 = teamNametoId[matchEntry[2].strip()]
# 	team2 = teamNametoId[matchEntry[3].strip()]
# 	dateObject = getDateObject(matchEntry[4])
# 	year = matchEntry[5]
# 	venue = matchEntry[6]
# 	city = matchEntry[7]
# 	country = matchEntry[8]
# 	tossWinner = teamNametoId.get(matchEntry[9].strip())		
# 	matchWinner = teamNametoId.get(matchEntry[10].strip())
# 	tossDecision = matchEntry[11]
# 	winType = matchEntry[12]
# 	outcomeType = matchEntry[13]
# 	playerOfTheMatch = playerSnameToID.get(matchEntry[14].strip())
# 	margin = None
# 	try:
# 		margin = int(matchEntry[15])
# 	except:
# 		margin = None


# 	return team1, team2, dateObject, year, venue, city, country, tossWinner, matchWinner, tossDecision, winType, outcomeType, margin, playerOfTheMatch, tempKey




# count =0
# for matchEntry in csv_reader:
# 	if(count == 0):
# 		count += 1
# 		continue
# 	rec = getMatchRecord(matchEntry)
# 	#print sql% rec
# 	cursor.execute(sql, rec)
# 	count += 1
















