PLAYER_RANDOM_QUERIES = {}

entry = {}
entry["query"] = "select Sum(batsmanscore) from ballToBall b join player p on p.id = b.strikerid where p.id = %s;"
entry["fact"] = "Total Runs  Scored:  ####"
PLAYER_RANDOM_QUERIES["1"] = entry


entry = {}
entry["query"] = "select count(distinct(teamId)) from playerToTeam t join player p on p.id = t.playerId where p.id = %s;"
entry["fact"] = "Total teams played for:  ####"
PLAYER_RANDOM_QUERIES["2"] = entry


entry = {}
entry["query"] = "select count(distinct(teamId)) from playerToTeam t join player p on p.id = t.playerId where p.id = %s;"
entry["fact"] = "Total Man of Match awards:  ####"
PLAYER_RANDOM_QUERIES["3"] = entry


entry = {}
entry["query"] = "select count(distinct(year)) from playerToTeam p where p.playerId = %s;"
entry["fact"] = "No of seasons played : ####"
PLAYER_RANDOM_QUERIES["4"] = entry


entry = {}
entry["query"] = "SELECT Count(outputtype) AS wickets FROM ballToBall b JOIN player p ON p.id = b.bowlerid WHERE outputtype IN ( 'caught', 'bowled', 'lbw', 'stumped','caught and bowled','hit wicket' ) and p.id = %s;"
entry["fact"] = "No of Wickets: ####"
PLAYER_RANDOM_QUERIES["5"] = entry

entry = {}
entry["query"] = "select count(batsmanScore) from ballToBall b where batsmanScore = 6 and b.strikerID = %s ;"
entry["fact"] = "No of Sixes: ####"
PLAYER_RANDOM_QUERIES["6"] = entry

entry = {}
entry["query"] = "select count(batsmanScore) from ballToBall b where batsmanScore = 4 and b.strikerID = %s ;"
entry["fact"] = "No of fours: ####"
PLAYER_RANDOM_QUERIES["7"] = entry

entry = {}
entry["query"] = "SELECT  (Sum(batsmanscore) / Count(DISTINCT matchID, overID, ballID))*100 AS SR FROM ballToBall	 where strikerid = %s GROUP BY strikerid"
entry["fact"] = "IPL Strike Rate: ####"
PLAYER_RANDOM_QUERIES["8"] = entry
