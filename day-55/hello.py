from flask import Flask, session, render_template, request
import random

app = Flask(__name__)

def generate_random_number():
    return random.randint(0, 9)

@app.route('/')
def home():
    if 'random_number' not in session:
        session['random_number'] = generate_random_number()
    return render_template('home.html')

@app.route("/guess", methods=['POST'])
def guess_number():
    guess = int(request.form['guess'])
    random_number = session.get('random_number')
    
    if guess > random_number:
        message = "Too high, try again!"
        color = "purple"
        gif = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"
    elif guess < random_number:
        message = "Too low, try again!"
        color = "red"
        gif = "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"
    else:
        message = "You found me!"
        color = "green"
        gif = "https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"
        session.pop('random_number')
    
    return render_template('result.html', message=message, color=color, gif=gif)

if __name__ == "__main__":
    app.run(debug=True)
