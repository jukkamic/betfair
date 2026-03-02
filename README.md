# Betfair API Bot & Web App

This project contains a Python script for interacting with the Betfair Exchange API and a simple Flask web application. It allows you to search for football events, view markets, and see current odds.


# Setup & Installation

## Option 1: Local Installation (Standard)

### Prerequisites

- Python 3.x
- A Betfair account
- Betfair API Application Key

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Create Python virtual environment**
    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```
   
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Option 2: VS Code Dev Container (Recommended)


### Prerequisites
- Docker Desktop
- Visual Studio Code
- Dev Containers Extension (VS Code will usually prompt you to install this)

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    code .
    ```

VS Code will detect the .devcontainer folder and show a notification asking to "Reopen in Container". Click it.
*Alternatively, press F1 and select "Dev Containers: Reopen in Container".*
Done! VS Code will build the container and automatically install the dependencies listed in requirements.txt. You are now ready to code.


## Configuration

### 1. Credentials (`config_secrets.py`)

You need to create a file named `config_secrets.py` in the root directory of the project to store your Betfair credentials. This file is excluded from version control for security.

Create `config_secrets.py` and add the following:

```python
BETFAIR_USERNAME = 'your_betfair_username'
BETFAIR_PASSWORD = 'your_betfair_password'
BETFAIR_API_KEY = 'your_betfair_api_key'
```

### 2. SSL Certificates

This project uses the **Non-Interactive (Bot) Login** method, which requires SSL certificates (`client-2048.crt` and `client-2048.key`) to authenticate securely with Betfair.

**Steps to set up SSL:**

1.  **Generate Certificates:**
    Follow the official Betfair documentation to generate your self-signed certificates:
    [Betfair Non-Interactive Bot Login Documentation](https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687915/Non-Interactive+bot+login)

2.  **Place Certificates in the project:**
    - Create a folder named `ssl` in the root directory.
    - Place your generated `client-2048.crt` and `client-2048.key` files inside this `ssl` folder.

    *Note: The path `ssl` is defined in `config.py`.*

    Directory structure should look like this:
    ```
    /
    ├── config_secrets.py
    ├── config.py
    ├── main.py
    ├── ssl/
    │   ├── client-2048.crt
    │   └── client-2048.key
    └── ...
    ```

3.  **Upload Certificate to Betfair:**
    Make sure you have uploaded the public certificate (`client-2048.crt`) to your Betfair account via "My Security" -> "Automated Access" (or as described in the documentation linked above).

## Usage

### Command Line Interface (CLI)

To run the interactive CLI script which logs in and lets you search for markets:

```bash
python main.py
```

Follow the prompts to search for a team (e.g., "Arsenal"), select an event, and view the market odds.

### Web Application

To run the Flask web application:

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000/`.
*Note: The current web app implementation contains a basic login and does not yet fully integrate the Betfair API functionality found in `main.py`.*
