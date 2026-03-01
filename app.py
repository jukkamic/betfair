from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Dummy user credentials (replace with a real user store)
users = {
    "admin": "password"
}

import main
import betfair_api.markets as markets

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    search_results = []
    
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        if search_term:
            session_token = main.get_session()
            if session_token:
                # Use the market finding logic from main/markets
                try:
                    search_results = markets.find_football_events(session_token, main.BETFAIR_API_KEY, search_term)
                except Exception as e:
                    print(f"Error searching events: {e}")
                    
    return render_template('index.html', username=session['username'], results=search_results)

@app.route('/event/<event_id>')
def event_details(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))
        
    session_token = main.get_session()
    market_data = {}
    
    if session_token:
        # Get market catalogue for the event
        catalogue = markets.get_market_catalogue(session_token, main.BETFAIR_API_KEY, event_id)
        if catalogue:
            market_id = catalogue['marketId']
            runners = {runner['selectionId']: runner['runnerName'] for runner in catalogue['runners']}
            
                        # Get odds
            odds = markets.get_market_odds(session_token, main.BETFAIR_API_KEY, market_id)
            
            # Calculate implied percentages
            total_implied_probability = 0
            runner_probabilities = {}
            
            if odds:
                for book in odds:
                    for runner in book.get('runners', []):
                        # Use the best available back price
                        back_prices = runner.get('ex', {}).get('availableToBack', [])
                        if back_prices:
                            best_back_price = back_prices[0]['price']
                            implied_prob = (1 / best_back_price) * 100
                            runner_probabilities[runner['selectionId']] = round(implied_prob, 2)
                            total_implied_probability += implied_prob
                        else:
                            runner_probabilities[runner['selectionId']] = 0

            market_data = {
                'market_name': catalogue['marketName'],
                'runners': runners,
                'odds': odds,
                'runner_probabilities': runner_probabilities,
                'total_implied_probability': round(total_implied_probability, 2)
            }
            
    return render_template('event_details.html', event_id=event_id, market=market_data)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
