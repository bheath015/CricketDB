from flask import Flask
import mysql.connector
from datetime import date, datetime, timedelta
import json
from flask import jsonify
from flask import render_template
from flask import request
from flask import Flask, session, redirect, url_for, escape, request
from queries import *

import pymongo

myclient = pymongo.MongoClient("mongodb://ec2-52-205-35-60.compute-1.amazonaws.com:27017/")
mydb = myclient["cricket"]
mycol = mydb["player"]


cnx = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")



def getUserNameList():
	cursor = cnx.cursor()
	cursor.execute(USER_DATA_QUERY)
	userData = {}
	emailList = []
	for (username, password, email) in cursor:
		entry = {}
		entry["username"] = username
		entry["password"] = password
		entry["email"] = email
		userData[username] = entry
		emailList.append(email)

	return userData, emailList

def getRunsDashStats():
	cursor = cnx.cursor()
	runsJsonData = getRunsAvgPerTeam(cursor)
	return runsJsonData


def getWicketsDashStats():
	cursor = cnx.cursor()
	wicketsJsonData = getWicketsAvgPerTeam(cursor)
	return wicketsJsonData

def getTopBatPlayersStats():
	cursor = cnx.cursor()
	topBatPlayersStats = getTopBatPlayers(cursor)
	return topBatPlayersStats;

def getOverYearHistoryStats():
	cursor = cnx.cursor()
	totalData = getOverYearHistory(cursor);
	return totalData;



def addEntry(username, password, email):
	#addUserConnector = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")
	cursor = cnx.cursor()
	sql = "INSERT INTO user VALUES (%s, %s,%s)"
	cursor.execute(sql, (username, password, email))
	cnx.commit()



def getplayerInfoStats(playerid):
	cursor = cnx.cursor()
	playerDetails = getPlayerDetails(cursor, playerid)
	return playerDetails


def getPlayerListStats():
	cursor = cnx.cursor()
	playerInfo = getPlayerList(cursor)
	return playerInfo


def getPlayerAutoCompleteData():
	cursor = cnx.cursor()
	playerInfo = getPlayerList(cursor)
	playerData = []
	for key in playerInfo.keys():
		entry = {}
		entry["label"] = playerInfo[key]["name"]
		entry["category"] = ""
		entry["pid"] = key
		playerData.append(entry)

	return playerData


def getPlayerMongoDetails(fullName):
	query = {} 
	query["fullName"]= fullName
	data = []
	for entry in mycol.find(query):
		data.append(entry)
	data[0]["bowlingData"] = data[0]["bowlingData"].replace('<table class="engineTable">', '<table class = "table table-bordered">')
	data[0]["battingData"] = data[0]["battingData"].replace('<table class="engineTable">', '<table class = "table table-bordered">')

	
	return data[0];

def getAllMongoDetails():
	query = {} 
	data = {}
	project = {}
	project["_id"] = 0
	for entry in mycol.find(query, project):
		data[entry["fullName"]] = entry
	return data



def addFavPlayerInDb(username, playerid):
	#addFavPlayerConnector = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")
	cursor = cnx.cursor(buffered=True)
	insertFavPlayer(cursor, username, playerid)
	cnx.commit()

def getFavPlayer(username):
	cursor = cnx.cursor()
	cursor.execute('select * from favRecords where username="%s"'% username )
	rs = cursor.fetchall()
	print rs
	if(len(rs) == 0):
		return {"playerid": None}

	entry = {}
	entry["playerid"] = str(rs[0][1])
	return entry

def getTeamsList():
	cursor = cnx.cursor()
	return getTeamsQuery(cursor)

def getPlayersOnRoster(team):
	cursor = cnx.cursor()
	return getPlayersOnRosterQuery(cursor, team)

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/addFavPlayer")
def addFavPlayerApi():
	if 'username' not in session:
		return redirect("/loginpage")
	if(request.args.get('playerid') is None):
		return jsonify({})
	username = session["username"]
	playerId = int(request.args.get('playerid'))
	addFavPlayerInDb(username, playerId)
	return jsonify({})



@app.route("/getFavPlayer")
def getFavPlayerRoute():
	if 'username' not in session:
		return redirect("/loginpage")
	username = session["username"]
	data = getFavPlayer(username)
	return jsonify(data)


@app.route("/getPlayerList")
def playerListApi():
    playerData = getPlayerListStats();
    return jsonify(playerData)


@app.route("/loginpage")
def loginPage():
	return render_template('login.html', message="Please Enter Your Information")


@app.route("/dash")
def showDash():
	if 'username' not in session:
		return redirect("/loginpage")
	username = session["username"]
	data = {}
	data["username"] = username
	data["runsJsonData"] = getRunsDashStats()
	data["wicketsJsonData"] = getWicketsDashStats()
	data["batPlayerStats"] = getTopBatPlayersStats()
	data["runRateChart"] = getOverYearHistoryStats()
	return render_template('dash.html', message=data)


@app.route("/login")
def loginRequest():
	username = request.args["username"]
	password = request.args["password"]
	userData, emailList = getUserNameList()
	if(username not in userData or password!=userData[username]["password"]):
		return render_template('login.html', message="Incorrect details")

	session['username'] = username
	return redirect('/dash')

@app.route("/logout")
def logout():
	session.pop('username', None)
	return redirect('/loginpage')


@app.route("/maketeam")
def maketeam():
	if 'username' not in session:
		return redirect("/loginpage")
	username = session["username"]
	data = {}
	data["username"] = username
	data['playerInfoList'] = getPlayerListStats()
	data['playerAutoComplete'] = getPlayerAutoCompleteData()
	data['allMongo'] = getAllMongoDetails()
	return render_template('team.html', message = data)




@app.route("/playerprofile")
def getPlayerProfilePage():
	if 'username' not in session:
		return redirect("/loginpage")
	username = session["username"]
	data = {}
	data["username"] = username
	data['playerInfoList'] = getPlayerListStats()
	data['playerAutoComplete'] = getPlayerAutoCompleteData()
	if(request.args.get('playerid') is None):
		return render_template("profile.html", message = data)
	playerId = int(request.args.get('playerid'))
	data['playerInfo'] = getplayerInfoStats(playerId)
	playerName = data['playerInfo']['name']
	data['mongoInfo'] = getPlayerMongoDetails(playerName)
	return render_template("profile.html", message = data)



@app.route("/register")
def registerPage():
	username = request.args["username"]
	password = request.args["password"]
	email = request.args["email"]

	userData, emailList = getUserNameList()
	if(username in userData or email in emailList):
		return render_template('login.html', message="Username/Email already exists")

	addEntry(username, password, email)

	return render_template('login.html', message="User created")

team_image_dict = {
	'Royal Challengers Bangalore': 'https://a.espncdn.com/i/teamlogos/cricket/500/335970.png',
	'Kolkata Knight Riders': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/800px-Kolkata_Knight_Riders_Logo.svg.png',
	'Rajasthan Royals': 'https://a.espncdn.com/i/teamlogos/cricket/500/335977.png',
	'Rising Pune Supergiant': 'https://upload.wikimedia.org/wikipedia/en/9/9a/Rising_Pune_Supergiant.png',
	'Kochi Tuskers Kerala': 'https://upload.wikimedia.org/wikipedia/en/thumb/9/96/Kochi_Tuskers_Kerala_Logo.svg/1024px-Kochi_Tuskers_Kerala_Logo.svg.png',
	'Kings XI Punjab': 'https://a.espncdn.com/i/teamlogos/cricket/500/335973.png',
	'Delhi Daredevils': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Delhi_Capitals_Logo.svg/800px-Delhi_Capitals_Logo.svg.png',
	'Gujarat Lions': 'https://upload.wikimedia.org/wikipedia/en/c/c4/Gujarat_Lions.png',
	'Deccan Chargers': 'https://upload.wikimedia.org/wikipedia/en/a/a6/HyderabadDeccanChargers.png',
	'Sunrisers Hyderabad': 'https://a.espncdn.com/i/teamlogos/cricket/500/628333.png',
	'Rising Pune Supergiants': 'https://upload.wikimedia.org/wikipedia/en/9/9a/Rising_Pune_Supergiant.png',
	'Chennai Super Kings': 'https://a.espncdn.com/i/teamlogos/cricket/500/335974.png',
	'Pune Warriors': 'https://a.espncdn.com/i/teamlogos/cricket/500/335978.png',
	'Mumbai Indians': 'https://a.espncdn.com/i/teamlogos/cricket/500/335978.png'
}

@app.route("/team")
def teamPage():
	teams_list = getTeamsList()
	team = "Gujarat Lions"
	roster = getPlayersOnRoster("Gujarat Lions")
	message = {}
	message['team_list'] = teams_list
	message['roster'] = roster
	message['team_name'] = team
	message['img_url'] = team_image_dict[team]
	return render_template('team.html', len=len(roster), message=message)



