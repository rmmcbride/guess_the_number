from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import random

app = Flask(__name__)

class Game:
	"""
	Create an instance of a game.
	
	Game properties:
		winning number
		number of guesses
		ability to check if an user's guess was correct
		feedback for the user on their guess
	"""
	
	def __init__(self, bottom=1, top=10):
		self.bottom = bottom
		self.top = top
		
	def new_game(self):
		self.winning_number = random.sample(range(self.bottom, self.top + 1), 1)[0]
		self.num_guesses = 0
		
	def play(self, guess):
		"""
		Compare the user's guess to the winning number and provide
		feedback to the user on their guess
		"""
		self.num_guesses += 1  # Update the number of turns counter
		# Compare the user's guess to the winning number
		if guess < self.winning_number:
			return 'Too low', -1
		elif guess > self.winning_number:
			return 'Too high', -1
		else:
			return 'Congratulations! You guessed correctly', 1

g = Game()

@app.route("/")
def welcome():
    return render_template("index.html")
    
@app.route("/play", methods=["GET", "POST"])
def playtime():
	guess = request.form.get('guess')
	feedback = None  # Default value
	success = -1  # Default value
	if guess:
		# The guess arrives as a string via the form. Need to convert
		# it to an integer
		feedback , success = g.play(int(guess))
	return render_template("play.html", guess=guess, feedback=feedback, success=success)

@app.route("/new_game", methods=["GET", "POST"])
def start_game():
	g.new_game()
	return redirect(url_for('playtime'))
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
