from flask import Flask, render_template, jsonify, Response, request, abort
from flask_cors import CORS
import requests
import math
import collections
import os

RANDOM_MAX = 100
RANDOM_URL = "https://codechallenge.boohma.com/random"
SCOREBOARDFILE = "./scoreboard.txt"
SCOREBOARD = collections.deque([""], 10)

# Note: If ID assignments are reassigned in front end, they must
# also be fixed here to preserve functionality
choiceTable =  {1: "rock",
				2: "paper",
				3: "scissors",
				4: "lizard",
				5: "spock"}

# Rows are user selection, cols are computer selection
winsTable = [ # rock    paper   scissors  lizard   spock
			  ["tie",  "lose",   "win",   "win",  "lose"], # rock
			  ["win",   "tie",  "lose",  "lose",   "win"], # paper
			  ["lose",  "win",   "tie",   "win",  "lose"], # scissors
			  ["lose",  "win",  "lose",   "tie",   "win"], # lizard
			  ["win",  "lose",   "win",  "lose",   "tie"]] # spock


def formatChoice(ID, name):
	return {"id": ID, "name": name}


def formatResults(result, playerChoice, compChoice):
	return {"results": result, "player": playerChoice["id"], 
			"computer": compChoice["id"]}

def getChoices():
	return [formatChoice(ID, name) for ID, name in choiceTable.items()]

def getRandChoice():
	data = requests.get(RANDOM_URL).json()
	if ( (type(data) != dict) or ("random_number" not in data)):
		raise ValueError("Random number request not processed successfully")
	randNum = data["random_number"]
	# Convert random number from 1 to RANDOM_MAX to
	# random number from 1 to 5
	randChoice = math.ceil(randNum/RANDOM_MAX*5)
	choiceName = choiceTable[randChoice]
	return formatChoice(randChoice, choiceName)

def getGameResult(userChoice, compChoice):
	# input format: {"id":<int>, "name":<String>}
	userIdx = userChoice["id"] - 1
	compIdx = compChoice["id"] - 1
	return winsTable[userIdx][compIdx]

def playRPSLS(choiceID):
	if choiceID not in choiceTable:
		raise ValueError("Invalid choice: %s" % choiceID)

	userChoice = formatChoice(choiceID, choiceTable[choiceID])

	compChoice = getRandChoice()

	result = getGameResult(userChoice, compChoice)

	updateScoreboard(userChoice, compChoice, result)

	return formatResults(result, userChoice, compChoice)

def updateScoreboard(userChoice, compChoice, result):
	# Converts datat to html format and scores in file
	# to be read and posted

	SCOREBOARD.appendleft([userChoice["name"], compChoice["name"], result])

	with open(SCOREBOARDFILE, 'w') as sb:
		sb.write("<h3>Most Recent Games</h3>\n")
		scoresList = list(SCOREBOARD)
		html = '<table>'
		html += '<tr><th>User</th><th>Computer</th><th>Result</th></tr>\n'
		for entry in scoresList:
			html += '<tr>'
			for val in entry:
				html += '<td>%s</td>' % val
			html += '</tr>\n'
		html += '<table>'
		sb.write(html)


app = Flask(__name__)
# CORS allows proper access control for default server location
# Further research into proper access control should be done if
# this project is extended
CORS(app)

@app.route("/choices", methods = ["GET"])
def choices():
	return jsonify(getChoices())

@app.route("/choice", methods = ["GET"])
def choice():
	return jsonify(getRandChoice())

@app.route("/play", methods = ["POST"])
def play():
	# Had to use force=True because
	# request.is_json returned False
	data = request.get_json(force=True)

	if( (type(data) != dict) or ("player" not in data) ):
		abort(400)

	choiceID = data["player"]

	result = playRPSLS(choiceID)

	return jsonify(result)

@app.route("/scoreboard", methods = ["GET"])
def getScoreboard():
	if(os.path.exists(SCOREBOARDFILE)):
		scoreBFile = open(SCOREBOARDFILE,"r")
		scores = scoreBFile.read()
		return scores
	return "No Scores Yet"




if __name__ == "__main__":
	app.run(debug=True)