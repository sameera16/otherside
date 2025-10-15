#!/usr/bin/env python3
"""
Gmail API Email Sender
Sends emails using Google Gmail API with OAuth2 authentication.
"""

import base64
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

class GmailSender:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API using OAuth2."""
        creds = None
        
        # Load existing token
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"Please download your OAuth2 credentials from Google Cloud Console "
                        f"and save as '{CREDENTIALS_FILE}'"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def create_message(self, 
                      to_emails: List[str], 
                      subject: str, 
                      body: str, 
                      cc_emails: Optional[List[str]] = None,
                      bcc_emails: Optional[List[str]] = None,
                      html_body: Optional[str] = None) -> dict:
        """Create email message."""
        
        if html_body:
            message = MIMEMultipart('alternative')
            text_part = MIMEText(body, 'plain')
            html_part = MIMEText(html_body, 'html')
            message.attach(text_part)
            message.attach(html_part)
        else:
            message = MIMEText(body)
        
        message['to'] = ', '.join(to_emails)
        message['subject'] = subject
        
        if cc_emails:
            message['cc'] = ', '.join(cc_emails)
        
        if bcc_emails:
            message['bcc'] = ', '.join(bcc_emails)
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw_message}
    
    def send_email(self, 
                   to_emails: List[str], 
                   subject: str, 
                   body: str,
                   cc_emails: Optional[List[str]] = None,
                   bcc_emails: Optional[List[str]] = None,
                   html_body: Optional[str] = None) -> dict:
        """Send email to multiple recipients."""
        try:
            message = self.create_message(to_emails, subject, body, cc_emails, bcc_emails, html_body)
            result = self.service.users().messages().send(userId='me', body=message).execute()
            print(f"Email sent successfully! Message ID: {result['id']}")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise
    
    def create_draft(self, 
                     to_emails: List[str], 
                     subject: str, 
                     body: str,
                     cc_emails: Optional[List[str]] = None,
                     bcc_emails: Optional[List[str]] = None,
                     html_body: Optional[str] = None) -> dict:
        """Create email draft without sending."""
        try:
            message = self.create_message(to_emails, subject, body, cc_emails, bcc_emails, html_body)
            draft = {'message': message}
            result = self.service.users().drafts().create(userId='me', body=draft).execute()
            print(f"Draft created successfully! Draft ID: {result['id']}")
            print(f"To: {', '.join(to_emails)}")
            print(f"Subject: {subject}")
            return result
        except HttpError as error:
            print(f"An error occurred creating draft: {error}")
            raise
    
    def send_draft(self, draft_id: str) -> dict:
        """Send a previously created draft."""
        try:
            result = self.service.users().drafts().send(userId='me', body={'id': draft_id}).execute()
            print(f"Draft sent successfully! Message ID: {result['id']}")
            return result
        except HttpError as error:
            print(f"An error occurred sending draft: {error}")
            raise
    
    def list_drafts(self) -> List[dict]:
        """List all drafts."""
        try:
            result = self.service.users().drafts().list(userId='me').execute()
            drafts = result.get('drafts', [])
            print(f"Found {len(drafts)} drafts")
            return drafts
        except HttpError as error:
            print(f"An error occurred listing drafts: {error}")
            raise
    
    def delete_draft(self, draft_id: str) -> None:
        """Delete a draft."""
        try:
            self.service.users().drafts().delete(userId='me', id=draft_id).execute()
            print(f"Draft {draft_id} deleted successfully")
        except HttpError as error:
            print(f"An error occurred deleting draft: {error}")
            raise

    def send_bulk_emails(self, recipients: List[dict]) -> List[dict]:
        """Send individual emails to multiple recipients.
        
        Args:
            recipients: List of dicts with keys: to_emails, subject, body, cc_emails, bcc_emails, html_body
        """
        results = []
        for recipient_data in recipients:
            try:
                result = self.send_email(**recipient_data)
                results.append({'success': True, 'result': result, 'recipient': recipient_data})
            except Exception as e:
                results.append({'success': False, 'error': str(e), 'recipient': recipient_data})
        return results
    
    def create_bulk_drafts(self, recipients: List[dict]) -> List[dict]:
        """Create drafts for multiple recipients.
        
        Args:
            recipients: List of dicts with keys: to_emails, subject, body, cc_emails, bcc_emails, html_body
        """
        results = []
        for recipient_data in recipients:
            try:
                result = self.create_draft(**recipient_data)
                results.append({'success': True, 'result': result, 'recipient': recipient_data})
            except Exception as e:
                results.append({'success': False, 'error': str(e), 'recipient': recipient_data})
        return results

def main():
    """Example usage of Gmail sender."""
    try:
        sender = GmailSender()
        
        # Test email
        test_result = sender.send_email(
            to_emails=['sameeramudigonda@gmail.com'],
            subject='Test Email from Gmail API',
            body='Hello! This is a test email sent using the Gmail API implementation.',
            html_body='<h2>Hello!</h2><p>This is a <strong>test email</strong> sent using the Gmail API implementation.</p>'
        )
        
        print("Test email sent successfully!")
        
        # Example of sending to multiple recipients
        # bulk_recipients = [
        #     {
        #         'to_emails': ['user1@example.com'],
        #         'subject': 'Bulk Email 1',
        #         'body': 'This is bulk email 1'
        #     },
        #     {
        #         'to_emails': ['user2@example.com', 'user3@example.com'],
        #         'subject': 'Bulk Email 2',
        #         'body': 'This is bulk email 2 to multiple recipients'
        #     }
        # ]
        # 
        # bulk_results = sender.send_bulk_emails(bulk_recipients)
        # print(f"Bulk email results: {bulk_results}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nTo set up Gmail API credentials:")
        print("1. Go to Google Cloud Console")
        print("2. Enable Gmail API")
        print("3. Create OAuth2 credentials")
        print("4. Download credentials.json to this directory")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()