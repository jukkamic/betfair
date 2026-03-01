from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import main
import betfair_api.markets as markets
from betfair_api.resources.event_types import EVENT_TYPES

main_bp = Blueprint('main', __name__)

# Process event types for the template
PROCESSED_EVENT_TYPES = []
if EVENT_TYPES and 'result' in EVENT_TYPES[0]:
    raw_types = EVENT_TYPES[0]['result']
    # Sort by name for better UX, though user might prefer Soccer/Tennis first
    # Let's keep the order but maybe ensure Soccer is selected by default
    for item in raw_types:
        PROCESSED_EVENT_TYPES.append({
            'id': item['eventType']['id'],
            'name': item['eventType']['name']
        })
    PROCESSED_EVENT_TYPES.sort(key=lambda x: x['name']) # Optional: Sort alphabetically

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    search_results = []
    
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        event_type_id = request.form.get('event_type_id', "1") # Default to Soccer (1)
        
        if search_term:
            session_token = main.get_session()
            if session_token:
                try:
                    search_results = markets.find_events(session_token, main.BETFAIR_API_KEY, search_term, event_type_id)
                except Exception as e:
                    print(f"Error searching events: {e}")
                    
    return render_template('index.html', name=current_user.name, results=search_results, event_types=PROCESSED_EVENT_TYPES)

@main_bp.route('/event/<event_id>')
@login_required
def event_details(event_id):
    session_token = main.get_session()
    market_data = {}
    
    if session_token:
        catalogue = markets.get_market_catalogue(session_token, main.BETFAIR_API_KEY, event_id)
        if catalogue:
            market_id = catalogue['marketId']
            runners = {runner['selectionId']: runner['runnerName'] for runner in catalogue['runners']}
            
            odds = markets.get_market_odds(session_token, main.BETFAIR_API_KEY, market_id)
            
            total_implied_probability = 0
            runner_probabilities = {}
            
            if odds:
                for book in odds:
                    for runner in book.get('runners', []):
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
