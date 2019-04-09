import mysql.connector

cnx = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")
cursor = cnx.cursor()
from os import listdir
from os.path import isfile, join
import yaml
from multiprocessing.dummy import Pool as ThreadPool
import pickle

teamsData = set([])

cursor.execute("SELECT * FROM player")

myresult = cursor.fetchall()

playerSnameToID = {}
playerIdToSname = {}

for x in myresult:
	playerSnameToID[x[2]] = x[0]
	playerIdToSname[x[0]] = x[2]


def loadYamlData(fileName):
	f = open(fileName, "r")
	io = yaml.load(f)
	f.close()
	print "done"
	return io

def loadAllCricSheets(folderPath):
	onlyfiles = [join(folderPath, f) for f in listdir(folderPath) if isfile(join(folderPath, f))]
	fileData = []
	count = 1
	for f in onlyfiles:
		print count
		fileData.append(loadYamlData(f))
		count += 1
	#fileData = calculateParallel(loadYamlData, onlyfiles)
	return fileData

def getAllTeams(matchDataList):
	teams = set([])
	for info in matchDataList:
		tt = info["info"]["teams"]
		for t in tt:
			teams.add(t)
	return teams

def calculateParallel(function, computeList, threads=40):
    pool = ThreadPool(threads)
    results = pool.map(function, computeList)
    pool.close()
    pool.join()
    return results

def loadCricSheetsBinary(filePath):
	data = None
	with open(filePath, "rb") as fp:
		data = pickle.load(fp)
	return data


# 

# allData = loadAllCricSheets("/Users/nikhilt/Desktop/tmp/ipl")
# f = open("allData.pkl","wb")
# pickle.dump(allData, f)
# f.close()

data = loadCricSheetsBinary("allData.pkl")

# def processMatch(matchData):

# 	venue = matchData["venue"]
# 	city = matchData["city"]
# 	teams = 





