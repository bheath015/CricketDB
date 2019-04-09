import pickle
from os import listdir
from os.path import isfile, join

# allData = None
# with open("allData.pkl") as fp:
# 	allData = pickle.load(fp)
# allData = [entry for entry in allData if isinstance(entry, dict)]
# print allData[0]["innings"]

folderPath = "/Users/nikhilt/Desktop/tmp/ipl"
onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
allfiles = []
for i in onlyfiles:
	print i
