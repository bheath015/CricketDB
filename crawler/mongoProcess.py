import json

fp = open("players.csv");

playersData = {}
for line in fp:
	entries = line.split(",")
	playername = entries[0].strip()
	jsonString = entries[1].strip()
	jsonString = jsonString.replace("'", '"')
	struct = json.loads(jsonString)
	playersData[playername] = struct





print playersData

