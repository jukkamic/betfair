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

### Test mode
The project may be run in test mode without the need for the following credentials setup procedures.

```bash
python app.py --test
```

### Live mode

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

2. **Some copy-pasteable commands when running in dev container:**
    1. openssl genrsa -out client-2048.key 2048
    2. You will have to edit /usr/lib/ssl/openssl.cnf according to docs linked above. Append the required section to end.
    3. openssl req -new -config /usr/lib/ssl/openssl.cnf -key client-2048.key -out client-2048.csr
    4. openssl x509 -req -days 365 -in client-2048.csr -signkey client-2048.key -out client-2048.crt -extfile /usr/lib/ssl/openssl.cnf -extensions ssl_client

3.  **Place Certificates in the project:**
    - Create a folder named `ssl` in the root directory.
    - Place your generated `client-2048.crt` and `client-2048.key` files inside this `ssl` folder.

    *Note: The path `ssl` is defined in `config.py`. and `.gitignore`* 

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

4.  **Upload Certificate to Betfair:**
    Make sure you have uploaded the public certificate (`client-2048.crt`) to your Betfair account via "My Security" -> "Automated Access" (or as described in the documentation linked above).

## AI Configuration for developers
Here's a config.yaml for Continue extension with your z.ai agent

```
name: Local Config
version: 1.0.0
schema: v1
models:
  - name: Z.ai Assistant
    provider: openai
    model: glm-4.7
    apiBase: https://api.z.ai/api/coding/paas/v4
    apiKey: <your-api-key-here>
    baseSystemMessage: You are an expert, senior software engineer and a helpful programming assistant. Always provide clean, efficient, and well-documented code. When writing Python, adhere to PEP 8 standards. We are working on a hobby project that is a custom Web UI for Betfair API. In order to be educational we follow professional standards in security, logging and testing. The difference to a business environment is only that we don't need to worry about scaling and we can implement our own user authentication and in general we are free from enterprise requirements.
    baseAgentSystemMessage: You are a systematic coding agent with file-editing capabilities. Break down problems methodically, verify your steps, and strictly format code blocks. Do not make assumptions about the codebase without checking. The user is working inside a Docker Dev Container on Windows. 1. Do not suggest using a Python virtual environment (venv), as the Docker container handles isolation. 2. Prefer standard libraries or packages listed in requirements.txt. 3. When providing shell commands, assume a Linux (bash) environment. 4. Be concise and helpful.        
    basePlanSystemMessage: You are a planning agent. Your only job is to create clear, actionable, step-by-step architectural blueprints for development tasks. Do not write the final implementation code; only outline the structural plan.
```

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
