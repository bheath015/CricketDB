from flask import Flask
import mysql.connector
from datetime import date, datetime, timedelta
import json
from flask import jsonify
from flask import render_template
from flask import request
from flask import Flask, session, redirect, url_for, escape, request
from queries import *
import numpy as np
np.random.seed(0)
import pymongo
from score import *
import time

myclient = pymongo.MongoClient("mongodb://ec2-52-205-35-60.compute-1.amazonaws.com:27017/")
mydb = myclient["cricket"]
mycol = mydb["player"]


cnx = mysql.connector.connect(user='root', database='cricketdb', host="cricketdb.cpemtivwfnzb.us-east-1.rds.amazonaws.com", passwd="Cricket1234!")

REDIS_TEAM_SCORE = "ALL_TEAM_SCORE"

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


    return data[0]

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

def getPlayersOnRoster(year, team):
    cursor = cnx.cursor(buffered=True)
    roster = (getPlayersOnRosterQuery(cursor, year, team))

    output = []
    for player in roster:
        output.append((player, getPlayerMongoDetails(player)['imageLink'], getPlayerHandedness(cursor, player)))
    return output

def getRandomQueries(team):
    cursor = cnx.cursor(buffered=True)
    choices = np.random.choice([0, 1, 2, 3], 2, replace=False)
    query1 = getTeamRandomQuery(cursor, team, choices[0])
    # query1 = getTeamRandomQuery(cursor, team, 0)
    query2 = getTeamRandomQuery(cursor, team, choices[1])
    # query2 = getTeamRandomQuery(cursor, team, 3)
    return (query1, query2)

def getAllTeamsScoresFromCache():
    entry = r.get(REDIS_TEAM_SCORE)
    if entry is None :
        entry = getAllTeamsScores()
        r.set(REDIS_TEAM_SCORE, json.dumps(entry))
        return entry
    else:
        print "From Cache #####################################"
        obj = json.loads(entry)
        millis = int(round(time.time() * 1000))
        if(millis - obj["time_stamp"] < CACHE_REFRESH):
            return obj
        entry = getAllTeamsScores()
        r.set(REDIS_TEAM_SCORE, json.dumps(entry))
        return entry


def getAllTeamsScores():
    teamData = {}
    for teamName in team_year_dict:
        playersData = getPlayersOnRoster(team_year_dict[teamName], teamName)
        teamData[teamName] = []
        for tup in playersData:
            teamData[teamName].append(tup[0])

    teamScores = {}

    for teamName in teamData:
        teamScores[teamName] = get_norm_scores(teamData[teamName])

    millis = int(round(time.time() * 1000))
    entry = {}
    entry["data"] = teamScores
    entry["time_stamp"] = millis
    return entry
def getTrivia2():
    cursor = cnx.cursor()
    return getTrivia2Query(cursor)

def getTrivia3():
    cursor = cnx.cursor()
    return getTrivia3Query(cursor)

def getTrivia4():
    cursor = cnx.cursor()
    return getTrivia4Query(cursor)

def getTrivia5():
    cursor = cnx.cursor()
    return getTrivia5Query(cursor)

def getTrivia6():
    cursor = cnx.cursor()
    return getTrivia6Query(cursor)

def getTrivia8():
    cursor = cnx.cursor()
    return getTrivia8Query(cursor)

def getTrivia9():
    cursor = cnx.cursor()
    return getTrivia9Query(cursor)

def getTrivia10():
    cursor = cnx.cursor()
    return getTrivia10Query(cursor)

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
    data['playerCost'] = redis_cache_cost()
    data['batScore'] = redis_cache_bat_cost()
    data['bowlScore'] = redis_cache_bowl_cost()
    data['team_list'] = getTeamsList()
    return render_template('team_build.html', message = data)


@app.route("/battle", methods=['POST'])
def showBattle():
    jsonData = request.form["jsondata"]
    print jsonData
    obj = json.loads(jsonData)
    playerNames = obj["nameList"]
    scoreTuple = get_norm_scores(playerNames)
    scoreTemp = getAllTeamsScoresFromCache()
    scoreTemp = scoreTemp["data"]
    scoreTemp["user"] = scoreTuple
    values = []

    del scoreTemp["Rising Pune Supergiants"]
    del scoreTemp["Rising Pune Supergiant"]
    del scoreTemp["Kochi Tuskers Kerala"]
    del scoreTemp["Gujarat Lions"]
    del scoreTemp["Deccan Chargers"]
    del scoreTemp["Pune Warriors"]
    del scoreTemp["Rajasthan Royals"]

    for teamName in scoreTemp:
        if teamName!= "user":
            values.append((teamName, scoreTemp[teamName], team_image_dict[teamName]))
        else:
            values.append((teamName, scoreTemp[teamName], "/static/ace-master/assets/images/avatars/user.jpg"))



    from random import shuffle
    shuffle(values)
    print values
    print len(values)
    data = {}
    makeMatch(values, 1, data)
    print(data)

    message = {}
    message["match"] = data

    return render_template('battle_view.html', message = message)



def winner(T1BA, T1BO, T2BA, T2BO):
    import random
    t=[0,1]
    if(T1BA>T2BA and T1BO>T2BO):
        return 0
    elif (T1BA+T1BO > T2BA+T2BO):
        return 0
    elif (T1BA+T1BO < T2BA+T2BO):
        return 1
    else:
        return random.choice(t)




def makeMatch(values, roundIndex, data):

    data[roundIndex] = {}
    data[roundIndex]["teams"] = values

    winners = []
    looser = []

    i = 0;
    while(i < len(values)):
        print values, i
        teamA = values[i]
        teamB = values[i+1]

        win = winner(teamA[1][0], teamA[1][1], teamB[1][0], teamB[1][1])

        if(win == 0):
            winners.append(teamA)
            looser.append(teamB)
        else:
            winners.append(teamB)
            looser.append(teamA)

        i = i +2

    data[roundIndex]["winners"] = winners


    if(len(values) == 4):
        makeMatch(winners, roundIndex + 2 , data)
        makeMatch(looser, roundIndex + 1, data)
        return

    if(len(winners) > 1):
        makeMatch(winners, roundIndex + 1, data)

    return



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
    data['facts'] = getRandomPlayerQueries(cnx.cursor(), playerId)
    print data['facts']
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
    'Pune Warriors': 'https://upload.wikimedia.org/wikipedia/en/4/4a/Pune_Warriors_India_IPL_Logo.png',
    'Mumbai Indians': 'https://a.espncdn.com/i/teamlogos/cricket/500/335978.png'
}

team_year_dict = {
    'Royal Challengers Bangalore': '2017',
    'Kolkata Knight Riders': '2017',
    'Rajasthan Royals': '2015',
    'Rising Pune Supergiant': '2017',
    'Kochi Tuskers Kerala': '2011',
    'Kings XI Punjab': '2017',
    'Delhi Daredevils': '2017',
    'Gujarat Lions': '2017',
    'Deccan Chargers': '2012',
    'Sunrisers Hyderabad': '2017',
    'Rising Pune Supergiants': '2016',
    'Chennai Super Kings': '2015',
    'Pune Warriors': '2013',
    'Mumbai Indians': '2017'
}

@app.route("/team")
def teamPage():
    if 'username' not in session:
        return redirect("/loginpage")
    username = session["username"]
    
    teams_list = getTeamsList()
    team = "Gujarat Lions"
    roster = getPlayersOnRoster(team_year_dict[team], team)
    randoms = getRandomQueries(team)
    message = {}
    message['team_list'] = teams_list
    message['roster'] = roster
    message['team_name'] = team
    message['img_url'] = team_image_dict[team]
    message['query 1'] = randoms[0][0]
    message['response 1'] = randoms[0][1]
    message['query 2'] = randoms[1][0]
    message['response 2'] = randoms[1][1]
    message["username"] = username
    if roster:
        message['roster_header'] = 'Roster'
    else:
        message['roster_header'] = 'No Roster Available'
    return render_template('team.html', len=len(roster), message=message)

@app.route('/team', methods=['POST'])
def teamPage2():
    if 'username' not in session:
        return redirect("/loginpage")
    username = session["username"]
    
    teams_list = getTeamsList()
    team = "Gujarat Lions"
    if not request.form['team_search']:
        team = "Gujarat Lions"
    else:
        team = request.form['team_search']
    roster = getPlayersOnRoster(team_year_dict[team], team)
    randoms = getRandomQueries(team)
    message = {}
    message['team_list'] = teams_list
    message['roster'] = roster
    message['team_name'] = team
    message['img_url'] = team_image_dict[team]
    message['query 1'] = randoms[0][0]
    message['response 1'] = randoms[0][1]
    message['query 2'] = randoms[1][0]
    message['response 2'] = randoms[1][1]
    message["username"] = username
    if roster:
        message['roster_header'] = 'Roster'
    else:
        message['roster_header'] = 'No Roster Available'
    return render_template('team.html', len=len(roster), message=message)


@app.route("/trivia")
def triviaPage():
    if 'username' not in session:
        return redirect("/loginpage")
    username = session["username"]
    message = {}
    message["username"] = username

    q2 = getTrivia2()
    message['query 2'] = q2[0]
    message['response 2'] = "{}%".format(q2[1][0])

    q3 = getTrivia3()
    message['query 3'] = q3[0]
    print(len(q3[1]))
    q3[1].append(("", ""))
    print(len(q3[1]))
    message['response 3'] = q3[1]

    q4 = getTrivia4()
    message['query 4'] = q4[0]
    q4[1].append(("", ""))
    message['response 4'] = q4[1]

    q5 = getTrivia5()
    message['query 5'] = q5[0]
    message['response 5'] = "{}".format(q5[1][0])

    q6 = getTrivia6()
    message['query 6'] = q6[0]
    message['response 6'] = "{}".format(q6[1][0])

    q8 = getTrivia8()
    message['query 8'] = q8[0]
    message['response 8'] = q8[1][0]

    q9 = getTrivia9()
    message['query 9'] = q9[0]
    message['response 9'] = "{}".format(q9[1][0])

    q10 = getTrivia10()
    message['query 10'] = q10[0]
    message['response 10'] = "{}".format(q10[1][0])

    message['team_list'] = getTeamsList()
    return render_template('trivia.html', message=message, len=len(q3[1]))


