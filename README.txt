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

Our player page includes a profile of any player from the IPL. Simply type a name into the search bar and click enter. On each profile, you can designate the player as your favorite! We have the following information from both of our sources:
-Bio information from the Mongo Database and the MySQL Database
-A player image from the Mongo Database
-Both batting and bowling statistics in a grid from the MySQL Database
-Rotating queries about players including (Not all implemented):
--Who is the best batsman against each bowler by strike rate?
--Most wickets by a specific player.

#####     Team Page      #####

Our team page presents a profile of your favorite team. Simply enter you favorite team into the search bar (if you don't have one, type in a random letter and select one from the dropdown of available teams) and click enter. This will direct you to your team's profile page. On this page, we query:
-The Roster from the SQL Database (if one is available for the team)
-An image associated with each player from the Mongo Database
-The bowling and batting handedness of each player from the SQL Database
-Rotating queries about each team which include (Not all implemented):
--The proportion of right vs left handed bowlers by team
--The proportion of old vs. young players by team (>= or < 25)
--The number of Ducks on a team
--The home win percentage of a team

We also show the crest of your favorite team.

##### Team-Builder Page  #####

Our team player page allows users to manage a budget and create their very own cricket team. We use our patented algorithm to rank players and assign them a cost. Players are added to a user's roster, and then evaluated as a group. May the best team win!

#####    Trivia Page     #####
#####       TODO         #####

This page presents many fun Cricket trivia facts that you can use to impress your friends. These include:
-How has winning the toss affected winning the match?
-Which out of town team has won the most matches in all cities where matches are played?
-Which player has the most player-of-the-match awards in each city where matches are played?
-Which player has scored the greatest difference of away runs minus home runs?
-Who bowler allows the highest rate of extras in the league?
-Who’s whose bunny? (Highest number of times a batsman got out for the same bowler)
-What is the highest score of runs in an over?
-Who took more than 100 wickets in IPL?
-Who scored the most centuries in IPL?


##############################
#####   Getting Started  #####
##############################

#####    Requirements    #####

Our web app is a Flask Application (Flask is a web framework written in Python). Therefore, you will need to download Flask and run it within a Python2 environment. 

Because our application relies on robust databases with Cricket team and player information, you will need to also download MySQL-Connector and PyMongo. We use a MySQL instance to hold our basic player and team information, and a Mongo database to hold our more in-depth player data.

##### Running the Program #####

In the flaskApp directory, run the command `FLASK_APP=index.py flask run` and you are good to go!
Our repo can be found at: https://github.com/bheath015/CricketDB
