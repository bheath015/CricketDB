# -*- coding: utf-8 -*-

seasons = ["2007", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]

parentLink = "http://stats.espncricinfo.com/ci/engine/records/team/series_results.html?id=117;type=trophy"

import requests
#from BeautifulSoup import BeautifulSoup
from lxml import html
import time
from multiprocessing.dummy import Pool as ThreadPool

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse


## nick name and his data contents
playerMap = {}

def getHtmlFromLink(url):
	r = requests.get(url)
	return r.content

def getHostName(url):
	parsed_uri = urlparse(url)
	result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	return result

def getCompleteUrl(url, filePath):
	return url[:-1] + filePath

def cleanName(name):
	cleanedName =  name.replace('(c)', "").strip()
	t = '†'
	cleanedName =  cleanedName.replace(t.decode("utf-8"), "").strip()
	if cleanedName[-1] == ',':
		cleanedName = cleanedName[:-1]

	return cleanedName.strip()

def processURLAndExtactLinks(urlLink, xpath):
	html_page = getHtmlFromLink(urlLink)
	tree = html.fromstring(html_page)
	tableElements = tree.xpath(xpath)
	links = []
	hostName = getHostName(urlLink)
	for tableElement in tableElements:
		link = tableElement.attrib["href"]
		if(link[0]=='/'):
			completeLink = getCompleteUrl(hostName, link)
		else:
			completeLink = link
		links.append(completeLink)
	return links

def processUrlAndExtactPlayers(urlLink, xpath):
	html_page = getHtmlFromLink(urlLink)
	tree = html.fromstring(html_page)
	tableElements = tree.xpath(xpath)
	players = {}
	hostName = getHostName(urlLink)
	for tableElement in tableElements:
		link = tableElement.attrib["href"]
		if(link[0]=='/'):
			completeLink = getCompleteUrl(hostName, link)
		else:
			completeLink = link
		playername = cleanName(tableElement.text_content())
		players[playername] = {}
		players[playername]["link"] = link
	return players


def mergeDicts(dictList):

	finalAnswer = {}

	for pmap in dictList:
		for key in pmap.keys():
			finalAnswer[key] = pmap[key]

	return finalAnswer

def mergeLists(listList):

	finalAnswer = []
	for l in listList:
		finalAnswer += l
	return finalAnswer



def getSeasonMatchLinks(urlLink):
	time.sleep(0.5)
	return processURLAndExtactLinks(urlLink, '//table[@class="engineTable"]/tbody/tr[@class="data1"]/td[@class="left"][1]/a')
	

def getMatchLinkFromSeasonPage(urlLink):
	time.sleep(0.5)
	return processURLAndExtactLinks(urlLink, '//div[@class="news-list large-20 medium-20 small-20"]/ul/li/div/ul/li[1]/a');

def getScoreCardPlayers(urlLink):
	xpath1 = '//div[@class="scorecard-section batsmen"]//div[@class="cell batsmen"]/a'
	time.sleep(0.5)
	dict1 = processUrlAndExtactPlayers(urlLink, xpath1)
	xpath2 = '//div[@class="scorecard-section bowling"]/table/tbody/tr/td[1]/a'
	time.sleep(0.5)
	dict2 = processUrlAndExtactPlayers(urlLink, xpath2)
	xpath3 = '//span[contains(text(),"Did not bat")]/../a'
	time.sleep(0.5)
	dict3 = processUrlAndExtactPlayers(urlLink, xpath3)
	return mergeDicts([dict1, dict2, dict3])


def calculateParallel(function, computeList, threads=20):
    pool = ThreadPool(threads)
    results = pool.map(function, computeList)
    pool.close()
    pool.join()
    return results



# getMatchLinkFromSeasonPage("http://stats.espncricinfo.com/ci/engine/records/team/series_results.html?id=117;type=troph/ci/engine/series/313494.html")


seasonMatchLinks = getSeasonMatchLinks(parentLink)

for i in seasonMatchLinks:
	print i

matchLinks = []
matchLinksParallel = calculateParallel(getMatchLinkFromSeasonPage, seasonMatchLinks)
matchLinks = mergeLists(matchLinksParallel)
print len(matchLinks)

# for seasonLink in seasonMatchLinks:
#  	currentLinks = getMatchLinkFromSeasonPage(seasonLink)
#  	matchLinks = matchLinks + currentLinks
#  	print "Extracted match count", len(matchLinks)
	


playerDicts = {}
# playerDictsParallel = calculateParallel(getScoreCardPlayers,matchLinks)
# playerDicts = mergeDicts(playerDictsParallel)

for matchLink in matchLinks:
 	currentDict = getScoreCardPlayers(matchLink)
 	playerDicts = mergeDicts([playerDicts, currentDict])
 	print "Extracted player count", len(playerDicts.keys())
	time.sleep(0.5)

# import csv

# w = csv.writer(open("players.csv", "w"))
# for key, val in playerDicts.items():
# 	w.writerow([key, val])







