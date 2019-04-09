

import csv
import json
from lxml import html

import requests
#from BeautifulSoup import BeautifulSoup
from lxml import html
import time
from multiprocessing.dummy import Pool as ThreadPool

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

completeDetails = {}
playerDetails = {}


def getCompleteUrl(url, filePath):
	return url[:-1] + filePath

def getHostName(url):
	parsed_uri = urlparse(url)
	result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	return result


def getPlayerName(tree):
	xpath = '//p[@class="ciPlayerinformationtxt"]/b[contains(text(),"Full name")]/../span'
	spanElement = tree.xpath(xpath)
	return spanElement[0].text

def getCountry(tree):
	xpath = '//div[@class="ciPlayernametxt"]//h3/b'
	spanElement = tree.xpath(xpath)
	return spanElement[0].text

def getPlayerImage(tree, fullName, url):
	xpath = '//div[@id="ciHomeContentlhs"]//img'
	imageElement = tree.xpath(xpath)
	imageElement = imageElement[0]
	link = imageElement.attrib["src"]
	completeLink = None
	hostName = getHostName(url)
	if(link[0]=='/'):
		completeLink = getCompleteUrl(hostName, link)
	else:
		completeLink = link

	return completeLink

def getPlayerPlayingRole(tree):
	xpath = '//p[@class="ciPlayerinformationtxt"]/b[contains(text(),"Playing role")]/../span'
	spanElement = tree.xpath(xpath)
	return spanElement[0].text

def getPlayerBattingStyle(tree):
	xpath = '//p[@class="ciPlayerinformationtxt"]/b[contains(text(),"Batting style")]/../span'
	spanElement = tree.xpath(xpath)
	return spanElement[0].text

def getPlayerBowlingStyle(tree):
	xpath = '//p[@class="ciPlayerinformationtxt"]/b[contains(text(),"Bowling style")]/../span'
	spanElement = tree.xpath(xpath)
	return spanElement[0].text

def getPlayerBorn(tree):
	xpath = '//p[@class="ciPlayerinformationtxt"]/b[contains(text(),"Born")]/../span'
	spanElement = tree.xpath(xpath)
	return spanElement[0].text

def getPlayerAge(tree):
	xpath = '//p[@class="ciPlayerinformationtxt"]/b[contains(text(),"Current age")]/../span'
	spanElement = tree.xpath(xpath)
	return spanElement[0].text

def getHtmlFromLink(url):
	r = requests.get(url)
	return r.content

def loadPlayerData(name):
	urlLink = playerDetails[name]
	html_page = getHtmlFromLink(urlLink)
	time.sleep(0.5)
	tree = html.fromstring(html_page)


	fullName = None
	imageLink = None
	playingrole = None
	battingStyle = None
	bowlingStyle = None
	born = None
	age = None
	country = None

	try:
		fullName = getPlayerName(tree).strip()
	except:
		fullName = ""

	try:
		country = getCountry(tree).strip()
	except:
		country = ""

	try:
		imageLink = getPlayerImage(tree, fullName, urlLink).strip()
	except:
		imageLink = ""

	try:
		playingrole = getPlayerPlayingRole(tree).strip()
	except:
		playingrole = ""

	try:
		battingStyle = getPlayerBattingStyle(tree).strip()
	except:
		battingStyle = ""

	try:
		bowlingStyle = getPlayerBowlingStyle(tree).strip()
	except:
		bowlingStyle = ""

	try:
		born = getPlayerBorn(tree).strip()
	except:
		born = ""

	try:
		age = getPlayerAge(tree).strip()
	except:
		age = ""

	dataDetails = {}
	dataDetails["fullName"] = fullName
	dataDetails["imageLink"] = imageLink
	dataDetails["playingrole"] = playingrole
	dataDetails["battingStyle"] = battingStyle
	dataDetails["bowlingStyle"] = bowlingStyle
	dataDetails["born"] = born
	dataDetails["age"] = age
	dataDetails["link"] = urlLink

	return dataDetails

def calculateParallel(function, computeList, threads=20):
    pool = ThreadPool(threads)
    results = pool.map(function, computeList)
    pool.close()
    pool.join()
    return results



with open('players.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		data = json.loads(row[1].replace("'",'"'))
		link = data["link"]
		playerDetails[row[0]] = link


shortNames = playerDetails.keys()

# details = calculateParallel(loadPlayerData, shortNames)


for i in range(len(shortNames)):
	print playerDetails[shortNames[i]]
	details = loadPlayerData(shortNames[i])
	details["shortName"] = shortNames[i]
	completeDetails[shortNames[i]] = details


stringData = json.dumps(completeDetails)

jsonFile = open("pDetails.json", "w")
jsonFile.write(stringData)
jsonFile.close()



