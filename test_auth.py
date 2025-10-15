#!/usr/bin/env python3
"""
Simple Gmail API authentication test
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def test_auth():
    """Test Gmail API authentication."""
    creds = None
    
    # Load existing token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Test API connection
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # Test basic profile access
        profile = service.users().getProfile(userId='me').execute()
        print(f"✅ Authentication successful!")
        print(f"Email: {profile['emailAddress']}")
        print(f"Messages: {profile['messagesTotal']}")
        
        return service
        
    except Exception as error:
        print(f"❌ Error: {error}")
        return None

if __name__ == '__main__':
    print("Testing Gmail API authentication...")
    service = test_auth()
    
    if service:
        print("\n🎉 Ready to send emails!")
    else:
        print("\n🚨 Fix the authentication issues above.")
        print("\nMake sure:")
        print("1. Gmail API is enabled in Google Cloud Console")
        print("2. Your email is added as a test user in OAuth consent screen")
        print("3. You're using the correct Google account during OAuth flow")