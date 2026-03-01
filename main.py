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
    # Handle missing secrets gracefully for the web app context if possible, 
    # or just let it fail if credentials are strictly required at startup.
    # For now, we will print a warning but not exit immediately to allow app.py to import this file if needed,
    # though actual API calls will fail.
    print("Warning: config_secrets.py not found. API calls will fail.")
    BETFAIR_USERNAME = None
    BETFAIR_PASSWORD = None
    BETFAIR_API_KEY = None

# Global session cache
_current_session_token = None
_last_session_time = None
SESSION_TIMEOUT_MINUTES = 15  # Keep-alive interval

def get_session():
    """
    Returns a valid session token.
    Uses cached token if available and fresh (or refreshed via keep-alive).
    Otherwise performs full login.
    """
    global _current_session_token, _last_session_time

    if not BETFAIR_USERNAME:
        return None

    now = datetime.datetime.now()

    # Case 1: No token cached -> Full Login
    if _current_session_token is None:
        token = login.login(BETFAIR_USERNAME, BETFAIR_PASSWORD, BETFAIR_API_KEY, config.CERT_PATH + "/client-2048.crt", config.CERT_PATH + "/client-2048.key")
        if token:
            _current_session_token = token
            _last_session_time = now
        return _current_session_token

    # Case 2: Token cached, check if refresh needed
    if _last_session_time and (now - _last_session_time).total_seconds() > (SESSION_TIMEOUT_MINUTES * 60):
        print(f"Session older than {SESSION_TIMEOUT_MINUTES} minutes. Attempting keep-alive...")
        new_token = login.keep_alive(_current_session_token, BETFAIR_API_KEY)
        
        if new_token:
            _current_session_token = new_token
            _last_session_time = now
            return _current_session_token
        else:
            print("Keep-alive failed. Re-logging in...")
            # Keep-alive failed (session expired?), try full login
            token = login.login(BETFAIR_USERNAME, BETFAIR_PASSWORD, BETFAIR_API_KEY, config.CERT_PATH + "/client-2048.crt", config.CERT_PATH + "/client-2048.key")
            if token:
                _current_session_token = token
                _last_session_time = now
            else:
                _current_session_token = None # Clear invalid token
            return _current_session_token

    # Case 3: Token cached and fresh
    return _current_session_token

if __name__ == "__main__":

    if not BETFAIR_USERNAME:
        print("Error: A config_secrets.py file with your Betfair credentials is required.")
        sys.exit(1)
        
    # 1. Login to get a session token
    session_token = get_session()

    
    if session_token:
        # 2. Find the event
        team_name = input("Enter team name to search: ")
        events = markets.find_football_events(session_token, BETFAIR_API_KEY, team_name)
        
        if events:
            print(f"\nFound {len(events)} events:")
            for i, event in enumerate(events):
                print(f"{i + 1}: {event['event']['name']} ({event['event']['openDate']})")
            
            try:
                choice = int(input("\nEnter the number of the event to view: "))
                if 1 <= choice <= len(events):
                    selected_event = events[choice - 1]
                else:
                    print("Invalid selection.")
                    sys.exit(0)
            except ValueError:
                print("Invalid input.")
                sys.exit(0)

            event_id = selected_event['event']['id']
            event_name = selected_event['event']['name']
            print(f"\nSelected Event: {event_name} with ID: {event_id}")

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
