# CricketDB

##############################
#####    Introduction    #####
##############################

Welcome to our Cricket Database! The purpose of this website is to learn more about the players and teams of the Indian Premier League, which is a professional Twenty20 cricket league contested from March-May of each year by eight teams representing eight different cities.

We invite new and veteran fans to explore our web application and learn more about their favorite teams and players. 

##############################
#####      Features      #####
##############################

#####    Welcome Page    #####

On our welcome page, you are invited to log into the web app. This will allow us to store your personal username and password into a database where we can also store you favorite team and player. 

#####    Player Page     #####

#####     Team Page      #####

Our team page presents a profile of your favorite team. Simply enter you favorite team into the search bar (if you don't have one, type in a random letter and select one from the dropdown of available teams) and click enter. This will direct you to your team's profile page. On this page, we query:
-The Roster from the SQL Database (if one is available for the team)
-An image associated with each player from the Mongo Database
-The bowling and batting handedness of each player from the SQL Database
-Rotating queries about each team which include:
--
--
--
--

We also show the crest of your favorite team.

##### Team-Builder Page  #####

##############################
#####   Getting Started  #####
##############################

#####    Requirements    #####

Our web app is a Flask Application (Flask is a web framework written in Python). Therefore, you will need to download Flask and run it within a Python2 environment. 

Because our application relies on robust databases with Cricket team and player information, you will need to also download MySQL-Connector and PyMongo. We use a MySQL instance to hold our basic player and team information, and a Mongo database to hold our more in-depth player data.
