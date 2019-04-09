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

sql = "INSERT INTO innings (matchID, inningsNo, battingTeam, bowlingTeam) values (%s, %s, %s, %s) "

for x in myresult:
	matchIdToInt[x[-1]] = x[0]
	matchIntToId[x[0]] = x[-1]

for match in myresult:
	tossWinner = match[8]
	tossDecision = match[10]
	team1 = match[1]
	team2 = match[2]
	if(tossDecision == "field"):
		tossLooser = team1 + team2 - tossWinner
		rec1 = (match[0], 1, tossLooser, tossWinner)
		rec2 = (match[0], 2, tossWinner, tossLooser)
		cursor.execute(sql, rec1)
		cursor.execute(sql, rec2)

	elif(tossDecision == "bat"):
		##
		tossLooser = team1 + team2 - tossWinner
		rec1 = (match[0], 1, tossWinner, tossLooser)
		rec2 = (match[0], 2, tossLooser, tossWinner)
		cursor.execute(sql, rec1)
		cursor.execute(sql, rec2)

cnx.commit()

		##













