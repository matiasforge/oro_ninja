from flask import Flask, render_template, redirect, request, session
import random
import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'

WINNING_GOLD = 500
MAX_MOVES = 15

def process_money(location):
    places = {
        'farm': (10, 20),
        'cave': (5, 10),
        'house': (2, 5),
        'casino': (-50, 50)
    }

    gold_range = places[location]
    earned_gold = random.randint(gold_range[0], gold_range[1])

    if location == 'casino' and earned_gold < 0:
        activity = f"Entered a casino and lost {-earned_gold} gold... Ouch! ({datetime.datetime.now()})"
    else:
        activity = f"Earned {earned_gold} gold from the {location}! ({datetime.datetime.now()})"

    session['gold'] += earned_gold
    session['activities'].insert(0, (activity, earned_gold >= 0))  # Insertar actividad al inicio de la lista

@app.route('/')
def index():
    if 'gold' not in session:
        session['gold'] = 0
    if 'activities' not in session:
        session['activities'] = []
    session['moves'] = session.get('moves', 0)
    won = session['gold'] >= WINNING_GOLD
    lost = session['moves'] >= MAX_MOVES
    show_reset = won or lost
    return render_template('index.html', won=won, lost=lost, show_reset=show_reset)

@app.route('/process_money', methods=['POST'])
def process_money_route():
    location = request.form['building']
    process_money(location)

    session['moves'] += 1
    return redirect('/')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        session.pop('gold', None)
        session.pop('activities', None)
        session.pop('moves', None)
        return redirect('/')
    return render_template('reset_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
