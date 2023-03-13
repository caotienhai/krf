import json
from google.oauth2.credentials import Credentials

def get_gmail_token():
    # Load credentials from file
    with open('D:/Setup/Others/vscode/.venv/client_secret.json', 'r') as token_file:
        token_data = json.load(token_file)

    # Build credentials object
    creds = Credentials.from_authorized_user_info(info=token_data)

    # Print access token
    print(creds.token)