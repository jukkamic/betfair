import requests
import datetime
import config

def call_api(session_token, api_key, method, params):
    """
    A helper function to make a JSON-RPC call to the Betfair API.
    """
    if not session_token:
        print("Cannot call API without a session token.")
        return None

    headers = {
        'X-Application': api_key,
        'X-Authentication': session_token,
        'content-type': 'application/json'
    }
    json_rpc_req = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    response = requests.post(config.API_URL, json=json_rpc_req, headers=headers)
    
    try:
        response.raise_for_status() # Raises an exception for bad status codes
        json_response = response.json()
        
        if "result" in json_response:
            return json_response["result"]
        elif "error" in json_response:
            print(f"API Error for method {method}: {json_response['error']}")
            return None

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error calling API method {method}: {e}")
        print(f"Response content: {response.text}")
        return None


def find_football_event(session_token, api_key, team_a, team_b):
    """
    Finds a football event by the names of the two teams.
    """
    print(f"Searching for event: {team_a} vs {team_b}")
    event_filter = {
        "filter": {
            "eventTypeIds": ["1"],  # 1 is the ID for Soccer
            "marketCountries": ["DE"], # Germany
            "textQuery": f"{team_a} v {team_b}",
            "marketStartTime": {
                "from": (datetime.datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }
    }
    
    events = call_api(session_token, api_key, "SportsAPING/v1.0/listEvents", event_filter)
    
    if events and len(events) > 0:
        print(f"Found {len(events)} matching event(s).")
        # Assuming the first result is the correct one
        return events[0]
    else:
        print("Could not find the specified event.")
        return None


def get_market_catalogue(session_token, api_key, event_id):
    """
    Gets the market catalogue (including marketId) for a given event.
    We are interested in the 'Match Odds' market.
    """
    print(f"Getting market catalogue for event ID: {event_id}")
    market_filter = {
        "filter": {
            "eventIds": [event_id],
            "marketTypeCodes": ["MATCH_ODDS"]
        },
        "maxResults": "1",
        "marketProjection": ["RUNNER_DESCRIPTION"]
    }
    
    markets = call_api(session_token, api_key, "SportsAPING/v1.0/listMarketCatalogue", market_filter)
    
    if markets and len(markets) > 0:
        print("Found 'Match Odds' market.")
        return markets[0]
    else:
        print("Could not find 'Match Odds' market for this event.")
        return None

def get_market_odds(session_token, api_key, market_id):
    """
    Retrieves the odds for a given market.
    """
    print(f"Retrieving odds for Market ID: {market_id}")
    market_book_params = {
        "marketIds": [market_id],
        "priceProjection": {
            "priceData": ["EX_BEST_OFFERS"]
        }
    }

    odds = call_api(session_token, api_key, "SportsAPING/v1.0/listMarketBook", market_book_params)
    return odds
