import json

PLAYER_DATA_QUERY = "select * from player";
USER_DATA_QUERY = "select * from user";

RUNS_STAT_QUERY = "select `name`, score  from team join (SELECT inn.`battingTeam`, sum(btb.batsmanScore) as score from ballToBall btb join innings inn on btb.matchID = inn.matchID and btb.inningsNo = inn.inningsNo group by inn.`battingTeam`) scoreResult on team.`id` = scoreResult.`battingTeam`";
WICKETS_STAT_QUERY = "select `name`, score  from team join (SELECT inn.`bowlingTeam`, count(btb.outputType) as score from ballToBall btb join innings inn on btb.matchID = inn.matchID and btb.inningsNo = inn.inningsNo where btb.outputType <> 'Not Applicable'and btb.outputType <> 'retired hurt'   group by inn.`bowlingTeam`) scoreResult on team.`id` = scoreResult.`bowlingTeam`";
TOP_FIVE_BAT_PLAYERS = "select btb.strikerID, p.name, sum(btb.batsmanScore) as score  from ballToBall btb join player p on btb.`strikerID` = p.`id` group by btb.strikerID, p.name order by sum(btb.batsmanScore) desc limit 5;"
TEAM_HISTORY = "select playerId, `year`, `name` from playerToTeam  join team on id = teamId where playerId in ####LIST#### order by playerId asc, `year` desc, teamId asc;"
OVER_YEAR_STATS = "select overid, `year`, avg(score) as avScore from (select b.matchid, b.overid, b.inningsno, Sum(b.batsmanscore) + COALESCE(Sum(be.extraruns), 0) AS score from ballToBall b left join ballExtra be on be.matchid = b.matchid AND be.overid = b.overid AND be.ballid = b.ballid AND be.inningsno = b.inningsno GROUP BY b.matchid, b.overid, b.inningsno) matchStats join `match` m on m.`matchID` = matchStats.matchid group by overid, `year`";


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

