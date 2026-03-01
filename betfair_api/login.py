import requests
import config 

def login(username, password, api_key, cert_path, key_path):
    """
    Performs a non-interactive login to get a session token.
    """
    payload = f'username={username}&password={password}'
    headers = {
        'X-Application': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    print("Attempting to log in...")
    response = requests.post(config.LOGIN_URL, data=payload, headers=headers, cert=(cert_path, key_path))

    if response.status_code == 200:
        json_response = response.json()
        if json_response.get('loginStatus') == 'SUCCESS':
            print("Login successful.")
            return json_response.get('sessionToken')
        else:
            print(f"Login failed: {json_response.get('loginStatus')}")
            return None
    else:
        print(f"Login request failed with status code: {response.status_code}")
        response.raise_for_status()

def keep_alive(session_token, api_key):

    """
    Extends the session timeout period to be reset to the default value.
    The response contains the session token.
    """
    headers = {
        'X-Application': api_key,
        'X-Authentication': session_token,
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(config.KEEP_ALIVE_URL, headers=headers)
        
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get('status') == 'SUCCESS':
                print(f"Keep-Alive successful. Token refreshed.")
                return json_response.get('token') # This is usually the same token
            else:
                print(f"Keep-Alive failed: {json_response.get('error')}")
                return None
        else:
            print(f"Keep-Alive request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Keep-Alive error: {e}")
        return None

