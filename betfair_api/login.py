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
