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


def find_events(session_token, api_key, text_query, event_type_id="1"):
    """
    Finds events based on a text query and event type ID.
    Default event_type_id="1" is Soccer.
    """
    print(f"Searching for events matching: {text_query} with type: {event_type_id}")
    event_filter = {
        "filter": {
            "eventTypeIds": [str(event_type_id)],
            "textQuery": text_query,
            "marketStartTime": {
                "from": (datetime.datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }
    }
    
    events = call_api(session_token, api_key, config.LIST_EVENTS, event_filter)

    
    if events and len(events) > 0:
        print(f"Found {len(events)} matching event(s).")
        return events
    else:
        print("No events found.")
        return []


def get_market_catalogue(session_token, api_key, event_id):
    """
    Gets the market catalogue (including marketId) for a given event.
    We are interested in the 'Match Odds' market.
    """
    print(f"Getting market catalogue for event ID: {event_id}")
    market_filter = {
        "filter": {
            "eventIds": [event_id],
            "marketTypeCodes": ["RT_MATCH_ODDS","MATCH_ODDS"]
        },
        "maxResults": "1",
        "marketProjection": ["RUNNER_DESCRIPTION"]
    }
    
    markets = call_api(session_token, api_key, config.LIST_MARKET_CATALOGUE, market_filter)
    
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

    odds = call_api(session_token, api_key, config.LIST_MARKET_BOOK, market_book_params)
    return odds
