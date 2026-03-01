import requests
import datetime
import sys
import betfair_api.login as login
import config
import betfair_api.markets as markets

# --- Configuration ---
# It's recommended to load these from a secure config file or environment variables
# For example, you can create a 'config.py' file and add your details there.
# from config import BETFAIR_USERNAME, BETFAIR_PASSWORD, BETFAIR_API_KEY

try:
    from config_secrets import BETFAIR_USERNAME, BETFAIR_PASSWORD, BETFAIR_API_KEY
except ImportError:
    print("Error: A config_secrets.py file with your Betfair credentials is required.")
    print("Please create a 'config_secrets.py' file with the following variables:")
    print("BETFAIR_USERNAME = 'your_username'")
    print("BETFAIR_PASSWORD = 'your_password'")
    print("BETFAIR_API_KEY = 'your_api_key'")
    sys.exit(1)

if __name__ == "__main__":
    # 1. Login to get a session token
    session_token = login.login(BETFAIR_USERNAME, BETFAIR_PASSWORD, BETFAIR_API_KEY, config.CERT_PATH + "/client-2048.crt", config.CERT_PATH + "/client-2048.key")
    
    if session_token:
        # 2. Find the event
        event = markets.find_football_event(session_token, BETFAIR_API_KEY, "Eintracht Frankfurt", "SC Freiburg")
        
        if event:
            event_id = event['event']['id']
            event_name = event['event']['name']
            print(f"Found Event: {event_name} with ID: {event_id}")

            # 3. Get the market for the event (Match Odds)
            market = markets.get_market_catalogue(session_token, BETFAIR_API_KEY, event_id)

            if market:
                market_id = market['marketId']
                runners = {runner['runnerName']: runner['selectionId'] for runner in market['runners']}
                print(f"Found Market ID: {market_id}")
                print(f"Runners: {runners}")
                
                # 4. Get the odds for the market
                market_odds = markets.get_market_odds(session_token, BETFAIR_API_KEY, market_id)
                
                if market_odds:
                    print("\n--- Market Odds ---")
                    for book in market_odds:
                        for runner in book['runners']:
                            runner_name = [name for name, sel_id in runners.items() if sel_id == runner['selectionId']][0]
                            
                            # Available to back prices
                            back_prices = runner.get('ex', {}).get('availableToBack', [])
                            best_back_price = back_prices[0]['price'] if back_prices else "N/A"
                            
                            # Available to lay prices
                            lay_prices = runner.get('ex', {}).get('availableToLay', [])
                            best_lay_price = lay_prices[0]['price'] if lay_prices else "N/A"
                            
                            print(f"  Runner: {runner_name}")
                            print(f"    Best Available Back Price: {best_back_price}")
                            print(f"    Best Available Lay Price: {best_lay_price}\n")
                    print("-------------------\n")
