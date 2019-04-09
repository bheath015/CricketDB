
import mysql.connector
from datetime import date, datetime, timedelta
import json


cnx = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")
cursor = cnx.cursor()

def month_converter(month):
	month = month.lower()
	months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
	return months.index(month) + 1

def processBorn(dateString):
	year = dateString.split(",")[1].strip()
	monthDate = dateString.split(",")[0].strip()
	month = monthDate.split(" ")[0].strip()
	dateNumString = monthDate.split(" ")[1].strip()
	monthNum = month_converter(month)
	bornDate = date(int(year), monthNum, int(dateNumString))
	return bornDate



def playerRecord(entry):
	name = entry["fullName"]
	shortName = entry["shortName"]
	dob = processBorn(entry["born"])
	batHandedness = entry["battingStyle"]
	bowlSkill = entry["bowlingStyle"]
	return name, shortName, dob, batHandedness, bowlSkill


def insertPlayerInfoToDb(cursor, jsonFile):
	sql = "INSERT INTO player (name, shortName, dob, batHandedness, bowlSkill) VALUES (%s, %s,%s,%s,%s)"
	fp = open(jsonFile)
	data = fp.read()
	dictData = json.loads(data)
	for key in dictData.keys():
		entry = dictData[key]
		rec =  playerRecord(entry)
		cursor.execute(sql, rec)


insertPlayerInfoToDb(cursor, "pDetails.json")
cnx.commit()


