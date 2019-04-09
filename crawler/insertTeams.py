import mysql.connector
from datetime import date, datetime, timedelta
import json
import pickle


cnx = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")
cursor = cnx.cursor()

allData = None
with open("allData.pkl") as fp:
	allData = pickle.load(fp)
allData = [entry for entry in allData if isinstance(entry, dict)]
print(len(allData))
teams = set([])
for matchEntry in allData:
	pteams = matchEntry["info"]["teams"]
	for p in pteams:
		teams.add(p)

sql = "INSERT INTO team (name, country) VALUES (%s, %s)"
for team in teams:
	rec = (team, "India")
	cursor.execute(sql, rec)

cnx.commit()



