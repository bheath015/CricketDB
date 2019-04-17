from flask import Flask
import mysql.connector
from datetime import date, datetime, timedelta
import json
from flask import jsonify
from flask import render_template
from flask import request
from flask import Flask, session, redirect, url_for, escape, request
from queries import *




cnx = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")


def getPlayerList():
	cursor = cnx.cursor()
	cursor.execute(PLAYER_DATA_QUERY)
	playerData = {}
	for (playerId, playerName, playerShortName, playerDob, playerBat, playerBowl) in cursor:
		entry = {}
		entry["playerId"] = playerId
		entry["playerName"] = playerName
		entry["playerShortName"] = playerShortName
		entry["playerDob"] = playerDob
		entry["playerBat"] = playerBat
		entry["playerBowl"] = playerBowl
		playerData[playerId] = entry

	return playerData

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
	addUserConnector = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")
	cursor = addUserConnector.cursor()
	sql = "INSERT INTO user VALUES (%s, %s,%s)"
	cursor.execute(sql, (username, password, email))
	addUserConnector.commit()



app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/getPlayerList")
def playerListApi():
    playerData = getPlayerList();
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












