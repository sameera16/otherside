#!/usr/bin/env python3
"""
SMB Outreach Campaign Manager
Creates targeted email drafts for behind-the-scenes experience platform.
"""

import json
import sys
from gmail_sender import GmailSender
from email_templates import customize_template

# Your contact info - UPDATE THESE
SENDER_NAME = "Sameera"
SENDER_EMAIL = "sameeramudigonda@gmail.com" 
SENDER_PHONE = "+1 (916) 607-8474"  # Update with your actual phone

def load_business_prospects():
    """Load business prospects from JSON file."""
    with open('business_prospects.json', 'r') as f:
        return json.load(f)

def create_campaign_drafts():
    """Create email drafts for all business prospects."""
    
    # Initialize Gmail sender
    sender = GmailSender()
    
    # Load prospects
    prospects = load_business_prospects()
    
    # Mapping business categories to template types
    business_type_mapping = {
        'coffee_roasters': 'coffee_roaster',
        'boutique_bakeries': 'bakery',
        'flower_studios': 'florist',
        'craft_breweries': 'brewery',
        'specialty_tea': 'tea_shop',
        'chocolate_makers': 'chocolate_maker'
    }
    
    all_drafts = []
    
    print("Creating email drafts for outreach campaign...\n")
    
    # Process each business category
    for category, businesses in prospects.items():
        print(f"Processing {category}...")
        
        # Map category to template type
        template_type = business_type_mapping.get(category)
        if not template_type:
            # Try to map more flexibly
            if 'coffee' in category:
                template_type = 'coffee_roaster'
            elif 'bakery' in category or 'baking' in category:
                template_type = 'bakery'
            elif 'flower' in category or 'florist' in category:
                template_type = 'florist'
            elif 'brew' in category:
                template_type = 'brewery'
            elif 'tea' in category:
                template_type = 'tea_shop'
            elif 'chocolate' in category:
                template_type = 'chocolate_maker'
            else:
                print(f"  Warning: No template found for category {category}, skipping...")
                continue
        
        # Create drafts for each business in category
        for business in businesses:
            try:
                # Customize email template
                email_content = customize_template(
                    business_type=template_type,
                    business_name=business['name'],
                    sender_name=SENDER_NAME,
                    sender_email=SENDER_EMAIL,
                    sender_phone=SENDER_PHONE
                )
                
                # Prepare draft data
                draft_data = {
                    'to_emails': [business['email']],
                    'subject': email_content['subject'],
                    'body': email_content['body']
                }
                
                # Create draft
                result = sender.create_draft(**draft_data)
                
                draft_info = {
                    'business_name': business['name'],
                    'business_type': business['type'],
                    'email': business['email'],
                    'draft_id': result['id'],
                    'subject': email_content['subject'],
                    'template_used': template_type
                }
                
                all_drafts.append(draft_info)
                print(f"  ✓ Created draft for {business['name']}")
                
            except Exception as e:
                print(f"  ✗ Failed to create draft for {business['name']}: {e}")
    
    # Save draft information for later reference
    with open('campaign_drafts.json', 'w') as f:
        json.dump(all_drafts, f, indent=2)
    
    print(f"\n📧 Campaign Summary:")
    print(f"Total drafts created: {len(all_drafts)}")
    print(f"Draft details saved to: campaign_drafts.json")
    print(f"\nNext steps:")
    print(f"1. Review drafts in your Gmail drafts folder")
    print(f"2. Edit any drafts as needed")
    print(f"3. Use send_campaign_drafts() to send approved drafts")
    
    return all_drafts

def send_campaign_drafts(draft_ids_to_send=None):
    """Send previously created drafts."""
    
    sender = GmailSender()
    
    # Load draft information
    try:
        with open('campaign_drafts.json', 'r') as f:
            all_drafts = json.load(f)
    except FileNotFoundError:
        print("No campaign drafts found. Run create_campaign_drafts() first.")
        return
    
    # If no specific drafts specified, ask user
    if draft_ids_to_send is None:
        print("Available drafts:")
        for i, draft in enumerate(all_drafts):
            print(f"{i+1}. {draft['business_name']} ({draft['business_type']})")
        
        choice = input("\nSend all drafts? (y/n): ").lower().strip()
        if choice == 'y':
            draft_ids_to_send = [draft['draft_id'] for draft in all_drafts]
        else:
            print("Specify draft numbers to send (comma-separated), or 'none' to cancel:")
            user_input = input().strip()
            if user_input.lower() == 'none':
                return
            
            try:
                indices = [int(x.strip()) - 1 for x in user_input.split(',')]
                draft_ids_to_send = [all_drafts[i]['draft_id'] for i in indices]
            except (ValueError, IndexError):
                print("Invalid selection. Cancelling.")
                return
    
    # Send selected drafts
    sent_count = 0
    for draft_id in draft_ids_to_send:
        try:
            sender.send_draft(draft_id)
            sent_count += 1
        except Exception as e:
            print(f"Failed to send draft {draft_id}: {e}")
    
    print(f"\n📤 Sent {sent_count} emails successfully!")

def list_campaign_status():
    """Show status of campaign drafts."""
    try:
        with open('campaign_drafts.json', 'r') as f:
            drafts = json.load(f)
        
        print("Campaign Draft Status:")
        print("=" * 50)
        
        by_type = {}
        for draft in drafts:
            btype = draft['business_type']
            if btype not in by_type:
                by_type[btype] = []
            by_type[btype].append(draft)
        
        for business_type, type_drafts in by_type.items():
            print(f"\n{business_type.upper()}:")
            for draft in type_drafts:
                print(f"  • {draft['business_name']} - {draft['email']}")
        
        print(f"\nTotal: {len(drafts)} drafts created")
        
    except FileNotFoundError:
        print("No campaign drafts found. Run create_campaign_drafts() first.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'create':
            create_campaign_drafts()
        elif command == 'send':
            send_campaign_drafts()
        elif command == 'status':
            list_campaign_status()
        else:
            print("Usage: python outreach_campaign.py [create|send|status]")
    else:
        print("SMB Outreach Campaign Manager")
        print("Available commands:")
        print("  create - Create email drafts for all prospects")
        print("  send   - Send previously created drafts")
        print("  status - Show campaign status")
        print("\nExample: python outreach_campaign.py create")