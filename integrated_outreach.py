#!/usr/bin/env python3
"""
Integrated Outreach System - Combines intelligence + email + landing pages
"""

import json
from business_intelligence import BusinessIntelligence
from email_templates import EMAIL_TEMPLATES
from gmail_sender import GmailSender

class IntegratedOutreach:
    def __init__(self):
        self.bi = BusinessIntelligence()
        self.gmail = GmailSender()
        self.base_url = "https://outbound.com"  # Your landing page domain
    
    def create_personalized_campaign(self, business_name: str, business_type: str, 
                                   location: str, email: str):
        """Create complete personalized campaign for a business."""
        
        # Step 1: Generate business intelligence
        print(f"Analyzing {business_name}...")
        intelligence = self.bi.generate_business_intelligence(business_name, business_type, location)
        
        # Step 2: Create personalized copy
        copy = self.bi.create_personalized_copy(intelligence)
        
        # Step 3: Generate landing page URL
        business_slug = business_name.lower().replace(' ', '-').replace('&', 'and')
        landing_url = f"{self.base_url}/{business_slug}-preview"
        
        # Step 4: Create personalized email
        email_body = f"""Hi {business_name},

{copy['personalized_opening']}

I'm Sameera, founder of Outbound - a platform where people book behind-the-scenes experiences at local businesses.

{copy['revenue_hook']}.

Want to see how? I created a personalized revenue calculator just for {business_name}:
👉 {landing_url}

Takes 2 minutes to see your specific setup analysis and projected earnings.

Many similar businesses are already earning ${intelligence['revenue_projections']['monthly_revenue']:,}/month - they love the effortless additional income while sharing their craft.

Best,
Sameera
Founder, Outbound
sameeramudigonda@gmail.com
+1 (916) 607-8474"""

        # Step 5: Create email draft
        draft_result = self.gmail.create_draft(
            to_emails=[email],
            subject=copy['subject_line'],
            body=email_body
        )
        
        # Step 6: Save campaign data
        campaign_data = {
            "business_name": business_name,
            "email": email,
            "intelligence": intelligence,
            "personalized_copy": copy,
            "landing_url": landing_url,
            "draft_id": draft_result['id'],
            "email_body": email_body
        }
        
        return campaign_data
    
    def generate_landing_page_data(self, intelligence: dict) -> dict:
        """Generate all data needed for landing page."""
        business_name = intelligence["business_name"]
        revenue = intelligence["revenue_projections"]
        reviews = intelligence["reviews_analysis"]
        location_demand = intelligence["location_demand"]
        website = intelligence["website_analysis"]
        
        return {
            "hero_title": f"{business_name}: Your process could earn ${revenue['monthly_revenue']:,}/month",
            "setup_analysis": {
                "has_open_kitchen": website.get("has_open_kitchen", False),
                "operating_hours": website.get("operating_hours", "Unknown"),
                "specialty_process": website.get("specialty_process", "Unknown"),
                "foot_traffic": website.get("foot_traffic", "Unknown")
            },
            "demand_proof": {
                "monthly_searches": location_demand.get("monthly_searches", 0),
                "curiosity_mentions": reviews.get("curiosity_mentions", 0),
                "interest_score": location_demand.get("local_interest_score", 0),
                "sample_quotes": reviews.get("sample_quotes", [])
            },
            "revenue_calculator": {
                "hourly_rate": revenue["hourly_rate"],
                "daily_sessions": revenue["daily_sessions"],
                "weekly_sessions": revenue["weekly_sessions"],
                "monthly_revenue": revenue["monthly_revenue"],
                "annual_revenue": revenue["annual_revenue"]
            },
            "cta_text": f"Join {business_name} in earning ${revenue['monthly_revenue']:,}/month"
        }

def create_full_campaign():
    """Create complete campaigns for all prospect businesses."""
    outreach = IntegratedOutreach()
    
    # Load business prospects
    with open('business_prospects.json', 'r') as f:
        prospects = json.load(f)
    
    all_campaigns = []
    
    # Process each business
    for category, businesses in prospects.items():
        print(f"\nProcessing {category}...")
        
        # Map category to business type
        business_type_mapping = {
            'coffee_roasters': 'coffee_roaster',
            'boutique_bakeries': 'bakery',
            'flower_studios': 'florist',
            'craft_breweries': 'brewery',
            'specialty_tea': 'tea_shop',
            'chocolate_makers': 'chocolate_maker'
        }
        
        business_type = business_type_mapping.get(category, 'coffee_roaster')
        
        for business in businesses:
            try:
                campaign = outreach.create_personalized_campaign(
                    business_name=business['name'],
                    business_type=business_type,
                    location=business['location'],
                    email=business['email']
                )
                
                all_campaigns.append(campaign)
                print(f"  ✓ Created campaign for {business['name']}")
                
                # Generate landing page data
                landing_data = outreach.generate_landing_page_data(campaign['intelligence'])
                
                # Save landing page data
                business_slug = business['name'].lower().replace(' ', '-').replace('&', 'and')
                with open(f'landing_pages/{business_slug}.json', 'w') as f:
                    json.dump(landing_data, f, indent=2)
                
            except Exception as e:
                print(f"  ✗ Failed for {business['name']}: {e}")
    
    # Save all campaign data
    with open('personalized_campaigns.json', 'w') as f:
        json.dump(all_campaigns, f, indent=2)
    
    print(f"\n🎉 Created {len(all_campaigns)} personalized campaigns!")
    print("Each business gets:")
    print("1. Personalized email with their specific revenue numbers")
    print("2. Custom landing page URL with their intelligence data")
    print("3. Real review mentions and local demand proof")
    
    return all_campaigns

if __name__ == "__main__":
    # Create landing pages directory
    import os
    os.makedirs('landing_pages', exist_ok=True)
    
    # Run full campaign creation
    campaigns = create_full_campaign()
    
    # Show sample campaign
    if campaigns:
        sample = campaigns[0]
        print(f"\n--- Sample Campaign: {sample['business_name']} ---")
        print(f"Subject: {sample['personalized_copy']['subject_line']}")
        print(f"Landing URL: {sample['landing_url']}")
        print(f"Revenue Projection: ${sample['intelligence']['revenue_projections']['monthly_revenue']:,}/month")
        print(f"Draft ID: {sample['draft_id']}")