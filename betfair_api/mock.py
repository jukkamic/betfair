"""
Mock Betfair API services for testing.
Reads real-world responses from test/resources/*.json files.
"""
import json
import os


def _load_json_file(filename):
    """Helper to load JSON data from test/resources directory."""
    # Get the path relative to this file (betfair_api/mock.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root, then into test/resources
    resources_path = os.path.join(current_dir, '..', 'test', 'resources', filename)
    
    try:
        with open(resources_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Mock data file not found: {resources_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {filename}: {e}")
        return None


def login(username, password, api_key, cert_path, key_path):
    """
    Mock login - returns a fake session token.
    Ignores credentials in test mode.
    """
    print(f"Mock login: Returning fake session token")
    return "mock_session_token_12345"


def keep_alive(session_token, api_key):
    """
    Mock keep-alive - returns the same token.
    """
    print(f"Mock keep-alive: Token refreshed")
    return session_token


def call_api(session_token, api_key, method, params):
    """
    Mock API call - returns mock data based on method.
    This mirrors the real call_api in markets.py but returns static JSON.
    """
    print(f"Mock API call: {method}")
    
    if method == "SportsAPING/v1/listEvents":
        return _mock_list_events(params)
    elif method == "SportsAPING/v1/listMarketCatalogue":
        return _mock_list_market_catalogue()
    elif method == "SportsAPING/v1/listMarketBook":
        return _mock_list_market_book()
    else:
        print(f"Mock API: Unknown method {method}")
        return None


def find_events(session_token, api_key, text_query, event_type_id="1"):
    """
    Mock find_events - returns mock events based on query text.
    """
    print(f"Mock search for events matching: {text_query} with type: {event_type_id}")
    
    # Load the mock list events data
    list_events_data = _load_json_file('listEvents.json')
    if not list_events_data:
        return []
    
    # listEvents.json contains an array of responses
    # We need to search through them based on the query
    query_lower = text_query.lower()
    
    for response_wrapper in list_events_data:
        response = response_wrapper[0]  # Each is wrapped in an array
        if 'result' in response:
            events = response['result']
            
            # Check if any event matches the query
            matching_events = []
            for event_data in events:
                event_name = event_data['event']['name'].lower()
                if query_lower in event_name:
                    matching_events.append(event_data)
            
            if matching_events:
                print(f"Mock: Found {len(matching_events)} matching event(s).")
                return matching_events
    
    print("Mock: No events found.")
    return []


def get_market_catalogue(session_token, api_key, event_id):
    """
    Mock get_market_catalogue - returns static market catalogue.
    """
    print(f"Mock: Getting market catalogue for event ID: {event_id}")
    
    # Load the mock market catalogue data
    catalogue_data = _load_json_file('listMarketCatalogue.json')
    if not catalogue_data:
        return None
    
    # The file contains a single response
    response = catalogue_data[0]
    if 'result' in response and len(response['result']) > 0:
        print("Mock: Found 'Match Odds' market.")
        return response['result'][0]
    else:
        print("Mock: Could not find 'Match Odds' market.")
        return None


def get_market_odds(session_token, api_key, market_id):
    """
    Mock get_market_odds - returns static market odds.
    Returns a list containing one market book (same format as real API).
    """
    print(f"Mock: Retrieving odds for Market ID: {market_id}")
    
    # Load the mock market book data
    book_data = _load_json_file('listMarketBook.json')
    if not book_data:
        return None
    
    # The file contains a single response
    response = book_data[0]
    if 'result' in response and len(response['result']) > 0:
        # Return the result array (list of market books)
        return response['result']
    else:
        print("Mock: Could not find market book data.")
        return None


# Internal helper functions for call_api compatibility

def _mock_list_events(params):
    """Helper to return events based on params (used by call_api)."""
    text_query = params.get('filter', {}).get('textQuery', '')
    event_type_id = params.get('filter', {}).get('eventTypeIds', ['1'])[0]
    
    # Use session_token and api_key placeholders (not used in mock)
    return find_events("mock_token", "mock_key", text_query, event_type_id)


def _mock_list_market_catalogue():
    """Helper to return market catalogue (used by call_api)."""
    return get_market_catalogue("mock_token", "mock_key", "mock_event_id")


def _mock_list_market_book():
    """Helper to return market book (used by call_api)."""
    return get_market_odds("mock_token", "mock_key", "mock_market_id")


def find_football_events(session_token, api_key, text_query):
    """
    Convenience function to find football/soccer events.
    Default event type ID is "1" for soccer.
    """
    return find_events(session_token, api_key, text_query, event_type_id="1")