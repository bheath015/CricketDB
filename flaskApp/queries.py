import json

PLAYER_DATA_QUERY = "select * from player";
USER_DATA_QUERY = "select * from user";

RUNS_STAT_QUERY = "select `name`, score  from team join (SELECT inn.`battingTeam`, sum(btb.batsmanScore) as score from ballToBall btb join innings inn on btb.matchID = inn.matchID and btb.inningsNo = inn.inningsNo group by inn.`battingTeam`) scoreResult on team.`id` = scoreResult.`battingTeam`";
WICKETS_STAT_QUERY = "select `name`, score  from team join (SELECT inn.`bowlingTeam`, count(btb.outputType) as score from ballToBall btb join innings inn on btb.matchID = inn.matchID and btb.inningsNo = inn.inningsNo where btb.outputType <> 'Not Applicable'and btb.outputType <> 'retired hurt'   group by inn.`bowlingTeam`) scoreResult on team.`id` = scoreResult.`bowlingTeam`";
TOP_FIVE_BAT_PLAYERS = "select btb.strikerID, p.name, sum(btb.batsmanScore) as score  from ballToBall btb join player p on btb.`strikerID` = p.`id` group by btb.strikerID, p.name order by sum(btb.batsmanScore) desc limit 5;"
TEAM_HISTORY = "select playerId, `year`, `name` from playerToTeam  join team on id = teamId where playerId in ####LIST#### order by playerId asc, `year` desc, teamId asc;"
OVER_YEAR_STATS = "select overid, `year`, avg(score) as avScore from (select b.matchid, b.overid, b.inningsno, Sum(b.batsmanscore) + COALESCE(Sum(be.extraruns), 0) AS score from ballToBall b left join ballExtra be on be.matchid = b.matchid AND be.overid = b.overid AND be.ballid = b.ballid AND be.inningsno = b.inningsno GROUP BY b.matchid, b.overid, b.inningsno) matchStats join `match` m on m.`matchID` = matchStats.matchid group by overid, `year`";
PLAYER_LIST_QUERY = "select * from player"
HANDEDNESS_QUERY = "select `batHandedness`, `bowlSkill` from player where name = \"{}\";"

TEAM_NAMES_QUERY = "select `name` from team;";
TEAM_ROSTER_QUERY = "select p.name from player p left join playerToTeam pt on p.id = pt.playerId left join team t on t.`id` = pt.`teamId` where pt.year = {} and t.name = \"{}\" order by p.name;";

TEAM_NAME_TO_ID_QUERY = "select id from team where name = \"{}\";"
TEAM_RANDOM_QUERIES_A = [
	("This team's home win percentage is", "select (y.home_win/ x.home_tot)*100 as percentage from (select count(*) as home_tot  from `match` m  where  m.city in (select home from team where team.id = {})) x join(select count(*) as home_win  from `match` m  where  matchWinner = {} and m.city in (select home from team where team.id = {})) y on 1=1;"),
	("The proportion of right handed to left handed bowlers on this team is", "select count(distinct(T2.name)) / (count(distinct(T1.name)) + count(distinct(T2.name))) from (select p.name, YEAR(CURDATE())  - YEAR(dob) as Age, teamId from player p join playerToTeam ptt on p.id = ptt.playerId where ptt.teamId = {} and YEAR(CURDATE())  - YEAR(dob) >= 25) as T1, (select p.name, YEAR(CURDATE())  - YEAR(dob) as Age, teamId from player p join playerToTeam ptt on p.id = ptt.playerId) as T2 where T2.teamId = {} and T2.age < 25;"),
	("The number of ducks recorded on this team is", "SELECT COUNT(DISTINCT( T.NAME )) FROM (SELECT p.NAME, p.id, Sum(batsmanscore) AS runs FROM ballToBall b JOIN player p ON p.id = b.strikerid GROUP  BY strikerid HAVING runs ='0') T JOIN playerToTeam ptt ON T.id = ptt.playerid WHERE  ptt.teamid = {} ORDER  BY runs DESC;")
]

TEAM_RANDOM_QUERIES_B = [("The percentage of players under 30 on this team is", 
                          "select count(distinct(name)) from (select p.name, YEAR(CURDATE())  - YEAR(dob) as Age, teamId from player p join playerToTeam ptt on p.id = ptt.playerId) T where teamId = {} and age < 30;", 
                          "select count(distinct(name)) from (select p.name, YEAR(CURDATE())  - YEAR(dob) as Age, teamId from player p join playerToTeam ptt on p.id = ptt.playerId) T where teamId = {} and age >= 30;")]


COLOR_CODES = {}
COLOR_CODES["Royal Challengers Bangalore"] = "#760e26"
COLOR_CODES["Kolkata Knight Riders"] = "#f5d76e"	
COLOR_CODES["Rajasthan Royals"]	= "#284984"
COLOR_CODES["Rising Pune Supergiant"] = "#08072f"	
COLOR_CODES["Kochi Tuskers Kerala"]	= "#c77f9d"
COLOR_CODES["Kings XI Punjab"]	= "#e88f48"
COLOR_CODES["Delhi Daredevils"]	= "#bb0931"
COLOR_CODES["Gujarat Lions"] = "#f5d76e"
COLOR_CODES["Deccan Chargers"]	= "#9fac9b"
COLOR_CODES["Sunrisers Hyderabad"]	= "#d34c08"
COLOR_CODES["Rising Pune Supergiants"] = "#08072f"	
COLOR_CODES["Chennai Super Kings"]	= "#fbf130"
COLOR_CODES["Pune Warriors"] = "#08072f"
COLOR_CODES["Mumbai Indians"] = "#4117e7"

def getOverYearHistory(cursor):
	cursor.execute(OVER_YEAR_STATS);
	yearData = {}
	totalData = []
	for(overid, year, avScore) in cursor:
		if year not in yearData:
			yearData[year] = [[i+1, 0] for i in range(20)]

		yearData[year][overid][1] = float(avScore);

	year = sorted(yearData.keys(), reverse=True)

	for y in year:
		entry = {}
		entry["label"] = str(y);
		entry["data"] = yearData[y]
		totalData.append(entry)

	return totalData[:5];


def getTopBatPlayers(cursor):
	cursor.execute(TOP_FIVE_BAT_PLAYERS)
	playerInfo = []
	enrtryMap = {}
	idList = []
	for (strikerID, name, score) in cursor:
		entry = {}
		entry['name'] = name;
		entry['score'] = score;
		entry['id'] = strikerID;
		entry['teams'] = []
		entry['teamNames'] = set([])
		playerInfo.append(entry)
		enrtryMap[strikerID] = entry; 
		idList.append(strikerID)


	st = '('
	i = 0;
	while i < len(idList):
		st += str(idList[i]);
		if(i!=len(idList) - 1):
			st += ","
		i+=1 
	st += ')';
	print st

	cursor.execute(TEAM_HISTORY.replace("####LIST####", st));
	for (playerId, year, teamName) in cursor:
		playerEntry = enrtryMap[playerId];
		if (teamName not in playerEntry['teamNames']):
			entry = {}
			entry['name'] = teamName
			entry['color'] = COLOR_CODES[teamName]
			playerEntry['teams'].append(entry)
			playerEntry['teamNames'].add(teamName)


	return playerInfo



def getRunsAvgPerTeam(cursor):
	cursor.execute(RUNS_STAT_QUERY)
	teamWiseData = {}
	for (name, runs) in cursor:
		teamWiseData[name] = runs;

	total = sum(teamWiseData.values())

	teamWiseAvgData = []

	for key in teamWiseData.keys():
		entry = {}
		entry["label"] = key
		entry["data"] = float(teamWiseData[key]/total) * 100
		entry["color"] = COLOR_CODES[key]

		teamWiseAvgData.append(entry)

	return teamWiseAvgData


def getWicketsAvgPerTeam(cursor):
	cursor.execute(WICKETS_STAT_QUERY)
	teamWiseData = {}
	for (name, runs) in cursor:
		teamWiseData[name] = float(runs);

	total = sum(teamWiseData.values())

	teamWiseAvgData = []

	for key in teamWiseData.keys():
		entry = {}
		entry["label"] = key
		entry["data"] = float(teamWiseData[key]/total) * 100
		entry["color"] = COLOR_CODES[key]

		teamWiseAvgData.append(entry)

	return teamWiseAvgData



def getPlayerDetails(cursor, pid):
	## do mongo stuff
	playerInfo = getPlayerList(cursor)
	playerDetails = playerInfo[pid]
	return playerDetails


def getPlayerList(cursor):
	cursor.execute(PLAYER_LIST_QUERY)
	playerInfo = {}
	for (pid, name, shortName, dob, batHand, bowlSkill) in cursor:
		entry = {}
		entry["pid"] = pid
		entry["name"] = name
		entry["shortName"] = shortName
		entry["dob"] = dob
		entry["batHand"] = batHand
		entry["bowlSkill"] = bowlSkill
		playerInfo[pid] = entry

	return playerInfo



def insertFavPlayer(cursor, username, player):
	print username
	rows_count = cursor.execute('select * from favRecords where username="%s";' % username)
	rs = cursor.fetchall()
	if(len(rs) > 0):
		entry = rs[0]
		cursor.execute('update favRecords set playerId=%s where username="%s"' % (player, username))
	else:
		cursor.execute("insert into favRecords (username, playerId) values (%s,%s)", (username, player))
	return



def getTeamsQuery(cursor):
	cursor.execute(TEAM_NAMES_QUERY)
	return [team[0] for team in cursor]

def getPlayersOnRosterQuery(cursor, year, team):
	# print(TEAM_ROSTER_QUERY.format(year, team))
	cursor.execute(TEAM_ROSTER_QUERY.format(year, team))
	# print([player[0] for player in cursor])
	return [player[0] for player in cursor]

def getPlayerHandedness(cursor, player):
	cursor.execute(HANDEDNESS_QUERY.format(player))
	out = [skill for skill in cursor]
	return out[0][0], out[0][1]

def getTeamRandomQuery(cursor, team, index):
	cursor.execute(TEAM_NAME_TO_ID_QUERY.format(team))
	ret = [x for x in cursor]
	team_id = ret[0][0]
	if index != 3:
		cursor.execute(TEAM_RANDOM_QUERIES_A[index][1].format(team_id, team_id, team_id))
		out = [x for x in cursor]
		out = out[0][0]
		prompt = TEAM_RANDOM_QUERIES_A[index][0]
	else:
		index = index - len(TEAM_RANDOM_QUERIES_A)
		cursor.execute(TEAM_RANDOM_QUERIES_B[index][1].format(team_id))
		under = [x for x in cursor]
		under = under[0][0]
		cursor.execute(TEAM_RANDOM_QUERIES_B[index][2].format(team_id))
		over = [x for x in cursor]
		over = over[0][0]
		out = float(under) / (float(over) + float(under)) * 100
		prompt = TEAM_RANDOM_QUERIES_B[index][0]
	return (prompt, "{}%".format(out))