"""
High-conversion cold email templates for different business types.
These templates address trust, value, and operational concerns.
"""

EMAIL_TEMPLATES = {
    "coffee_roaster": {
        "subject": "Partnership opportunity: Outbound platform launch",
        "body": """Hi {business_name} team,

I'm Sameera, founder of Outbound - a new platform where people can book real, behind-the-scenes experiences at local businesses.

Coffee lovers are endlessly curious about roasting. They want to watch the beans transform, smell the aromas, see the timing and precision that goes into each batch. But they rarely get the chance to just... observe.

Here's what I'm building: Coffee enthusiasts book 1-hour slots to quietly watch your roasting process during regular operations. Think of it as "behind-the-scenes access" rather than formal instruction.

You pick a one-hour slot (say 10-11 AM or any quiet time). A paying guest books that time to observe your team at work - safely from a designated area. You earn around $40 per hour for hosting, and we handle scheduling, payment, and promotion.

It's simple: they watch, you work normally. No teaching required, no disruption to your process. Just pure curiosity being satisfied.

Many small business owners are already joining Outbound - they see it as an effortless way to create additional income while connecting people with experiences they'd never normally access.

Would you be open to a quick 10-minute chat this week?

Best regards,
{sender_name}
Founder, Outbound
{sender_email}
{sender_phone}"""
    },
    
    "bakery": {
        "subject": "Outbound platform - early partner invitation",
        "body": """Hi {business_name},

I'm Sameera, founder of Outbound - a platform where people can book behind-the-scenes experiences at local businesses.

Baking enthusiasts are fascinated by your process. They want to watch dough transform, see timing techniques, observe the craft that creates those perfect loaves. But they rarely get to just... watch.

Here's the concept: Food lovers book 1-hour slots to quietly observe your baking during regular operations. No instruction needed - just pure curiosity about how artisan bread comes to life.

You pick a one-hour slot (maybe during morning prep or afternoon baking). A paying guest books that time to observe your work - safely from a designated area. You earn around $45 per hour, and we handle all scheduling and payments.

Simple: they watch, you bake normally. No teaching, no disruption to your workflow. Just satisfying people's genuine curiosity about your craft.

Many bakeries are already joining - they love earning extra revenue while sharing what they're passionate about, without any additional effort.

Would you be open to a 10-minute chat this week?

Warm regards,
{sender_name}
Founder, Outbound
{sender_email}
{sender_phone}"""
    },
    
    "florist": {
        "subject": "Behind-the-scenes experiences platform - invitation",
        "body": """Hi {business_name},

I'm Sameera, founder of Outbound - a platform where people book behind-the-scenes experiences at local businesses.

Flower arrangement is endlessly fascinating to watch. People are curious about color choices, stem techniques, how you build those stunning compositions. But they rarely get to just... observe the process.

Here's what I'm building: Flower enthusiasts book 1-hour slots to quietly watch you create arrangements during your regular work. No instruction - just pure observation of your creative process.

You pick a one-hour slot (maybe during prep time or custom orders). A paying guest books that time to observe your creative process - from a designated area. You earn around $40 per hour, and we handle scheduling and payments.

It's that simple: they watch, you arrange normally. No teaching required, no change to your workflow. Just people satisfying their curiosity about floral artistry.

Many florists are already joining Outbound - they see it as effortless additional income while sharing their passion with people who genuinely appreciate the craft.

Would you be open to a quick 10-minute chat this week?

Best,
{sender_name}
Founder, Outbound
{sender_email}
{sender_phone}"""
    },
    
    "brewery": {
        "subject": "Partnership opportunity: Outbound experiences platform",
        "body": """Hi {business_name},

I'm Sameera, founder of Outbound - a platform where people book behind-the-scenes experiences at local businesses.

Beer enthusiasts are endlessly curious about brewing. They want to watch the mashing, see fermentation in action, observe the precise timing that creates great beer. But beyond formal tours, they rarely get to just... watch.

Here's the concept: Beer lovers book 1-hour slots to quietly observe your brewing process during regular operations. Think of it as "behind-the-scenes access" rather than formal instruction.

You pick a one-hour slot (maybe during brewing prep or active brewing). A paying guest books that time to observe your work - safely from a designated area. You earn around $45 per hour, and we handle scheduling and payments.

Simple: they watch, you brew normally. No formal presentation needed, no change to your process. Just satisfying genuine curiosity about craft brewing.

Many breweries are already joining Outbound - they love earning additional revenue while sharing their passion with people who truly appreciate the craft.

Would you be open to a 10-minute chat this week?

Cheers,
{sender_name}
Founder, Outbound
{sender_email}
{sender_phone}"""
    },
    
    "tea_shop": {
        "subject": "Early invitation: Outbound platform launch",
        "body": """Hi {business_name},

I'm Sameera, founder of Outbound - a platform where people book behind-the-scenes experiences at local businesses.

Tea preparation is naturally meditative to watch. People are curious about steeping techniques, blending processes, the mindful ritual of creating the perfect cup. But they rarely get to just... observe.

Here's what I'm building: Tea enthusiasts book 1-hour slots to quietly watch your tea preparation during regular operations. No instruction needed - just pure observation of your craft.

You pick a one-hour slot (maybe during blend creation or ceremony prep). A paying guest books that time to observe your process - from a designated quiet area. You earn around $40 per hour, and we handle scheduling and payments.

It's simple: they watch, you prepare normally. No teaching required, no disruption to your workflow. Just people satisfying their curiosity about tea artistry.

Many tea shops are already joining Outbound - they see it as effortless additional income while sharing the meditative beauty of their craft.

Would you be open to a 10-minute chat this week?

With gratitude,
{sender_name}
Founder, Outbound
{sender_email}
{sender_phone}"""
    },
    
    "chocolate_maker": {
        "subject": "Artisan business partnership - Outbound platform",
        "body": """Hi {business_name},

I'm Sameera, founder of Outbound - a platform where people book behind-the-scenes experiences at local businesses.

Chocolate lovers are fascinated by bean-to-bar transformation. They want to watch beans roasting, see grinding techniques, observe the magic that turns cacao into chocolate. But they rarely get to just... watch.

Here's the concept: Chocolate enthusiasts book 1-hour slots to quietly observe your chocolate making during regular operations. No instruction needed - just pure observation of your craft.

You pick a one-hour slot (maybe during roasting or tempering). A paying guest books that time to observe your process - safely from a designated area. You earn around $45 per hour, and we handle scheduling and payments.

Simple: they watch, you create normally. No teaching required, no disruption to your production. Just satisfying people's genuine curiosity about artisan chocolate making.

Many chocolate makers are already joining Outbound - they love earning additional revenue while sharing their passion with people who truly appreciate the craft.

Would you be open to a 10-minute chat this week?

Best regards,
{sender_name}
Founder, Outbound
{sender_email}
{sender_phone}"""
    }
}

# Template customization function
def customize_template(business_type, business_name, sender_name, sender_email, sender_phone):
    """Customize email template for specific business."""
    template = EMAIL_TEMPLATES.get(business_type)
    if not template:
        raise ValueError(f"No template found for business type: {business_type}")
    
    return {
        "subject": template["subject"],
        "body": template["body"].format(
            business_name=business_name,
            sender_name=sender_name,
            sender_email=sender_email,
            sender_phone=sender_phone
        )
    }