# Gmail API Email Sender Setup Guide

## Prerequisites
1. Python 3.7+
2. Google Cloud Project with Gmail API enabled
3. OAuth2 credentials

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Enable Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### 3. Create OAuth2 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Download the credentials file as `credentials.json`
5. Place `credentials.json` in the project directory

### 4. First Run Authentication
```bash
python gmail_sender.py
```
- Browser will open for OAuth consent
- Grant permissions to send emails
- Token will be saved for future use

## Usage Examples

### Send Single Email
```python
from gmail_sender import GmailSender

sender = GmailSender()
sender.send_email(
    to_emails=['recipient@example.com'],
    subject='Test Subject',
    body='Plain text body',
    html_body='<h1>HTML body</h1>'
)
```

### Send to Multiple Recipients
```python
sender.send_email(
    to_emails=['user1@example.com', 'user2@example.com'],
    subject='Multiple Recipients',
    body='This goes to multiple people'
)
```

### Bulk Email with Different Content
```python
recipients = [
    {
        'to_emails': ['user1@example.com'],
        'subject': 'Personal Subject 1',
        'body': 'Personal message 1'
    },
    {
        'to_emails': ['user2@example.com'],
        'subject': 'Personal Subject 2', 
        'body': 'Personal message 2'
    }
]

results = sender.send_bulk_emails(recipients)
```

## Features
- OAuth2 authentication with token refresh
- Send to multiple recipients (to, cc, bcc)
- HTML and plain text emails
- Bulk email sending
- Error handling and logging
- Rate limit compliance