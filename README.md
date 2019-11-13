# Rock, Paper, Scissors, Lizard, Spock


## Description
This is a back-end server which is used to play the game Rock, Paper, Scissors, Lizard, Spock.

<img src="https://github.com/savanaconda/RockPaperScissorsLizardSpock/blob/master/rockpaperscissorslizardspock.png" width="400">

The rules for this game can be found at:
http://www.samkass.com/theories/RPSSL.html

The game is played when the user picks one of the five choices, using the front-end interface. The computer randomly selects an option, a winner is chosen, and the user is told what the computer selected and if the user won, lost, or tied the computer.

The front-end interface is located at:
https://codechallenge.boohma.com/ 


## Implementation
Back-end code is written in Python, utilizing the Python web framework Flask. Three main functions are implement: choices, choice, and play.

### Choices
Choices returns the 5 game choices (rock, paper, scissors, lizard, and spock) via an HTTP GET. The data format is application/json, with pairs of "id" and "name". An example of the format of a single choice is shown here:
```
{"id": 1, "name": "rock"}
```

### Choice
Choice returns a randomly selected choice, which is used as the computer's choice in the game play. This is also done via an HTTP GET. A random number is received from https://codechallenge.boohma.com/random and one of the five choices is selected based on this random number. The output is the same format as that shown above in Choices.

### Play
The play command takes the user choice from the front-end server, compares that to the randomly generated computer choice, and returns the results to the user. The data format is as such:
```
{"results": "win", "player": 1, "computer": 4}
```
In the above example, the user (player) selected choice 1, rock, and the computer selected choice 4, lizard. Rock crushes lizard, so the user wins and thus the result is win.

Play is implemented as a HTTP POST where the user choice is posted from the front-end to the server.


## Instructions

### Setup
Test machine should have Python 3.7.2 installed, as well as the following python libraries:
 * flask
 * flask-cors
 * requests
 * math
 * collections
 * os

The back-end server __RSPLS_game.py__ can be downloaded from this Github repo. The front-end application will be accessed via https://codechallenge.boohma.com/.

### Loading the Game
Start the server by navigating to the folder which it is located and typing
```
python RPSLS_game.py
```
Once the server starts, you should see the following output in the console:
```
 * Serving Flask app "RPSLS_game" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 880-025-376
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
To use the front-end interface, navigate to https://codechallenge.boohma.com/ and paste the address http://127.0.0.1:5000 into the root URL field. Step through the game by following the instructions on the front-end page. As HTTP requests are made, status codes can be monitored in the output in the console.


## Scoreboard
Once the server has been started, a scoreboard of the 10 most recent runs can be accessed at http://127.0.0.1:5000/scoreboard.


## Resources
1. http://flask.palletsprojects.com/en/1.1.x/
2. https://flask-cors.readthedocs.io/en/latest/
3. https://www.w3schools.com/tags/tag_table.asp
