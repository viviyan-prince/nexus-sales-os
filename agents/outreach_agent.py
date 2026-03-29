


class OutreachAgent:
    name = "Outreach Agent"

    def generate(self, deal: dict, strategy: dict, risk_data: dict = None) -> dict:
        client_name = deal.get("client_name", "Client")
        company = deal.get("company", "your organization")
        industry = deal.get("industry", "your industry")
        deal_value = deal.get("deal_value", 0)
        stage = deal.get("stage", "")
        risk_score = risk_data.get("risk_score", 0) if risk_data else 0
        urgency = strategy.get("urgency", "moderate")

        first_name = client_name.split()[0] if client_name else "there"

        messages = {
            "email": self._generate_email(first_name, client_name, company, industry, deal_value, stage, urgency, risk_score),
            "whatsapp": self._generate_whatsapp(first_name, company, industry, urgency),
            "linkedin": self._generate_linkedin(first_name, company, industry, urgency)
        }

        return {
            "agent": self.name,
            "deal_id": deal.get("id"),
            "messages": messages,
            "personalization_context": {
                "client": client_name,
                "company": company,
                "industry": industry,
                "urgency_level": urgency,
                "strategy_applied": strategy.get("primary_strategy", "")
            },
            "reasoning": f"Generated 3 personalized outreach messages (Email, WhatsApp, LinkedIn) for {client_name} at {company}. Messages are tailored to {urgency} urgency level and aligned with the '{strategy.get('primary_strategy', '')}' strategy. Each message includes contextual references to {industry} and the current {stage} stage."
        }

    def _generate_email(self, first_name, full_name, company, industry, deal_value, stage, urgency, risk_score):
        if urgency == "critical":
            return {
                "subject": f"{first_name}, let's get this across the line — exclusive offer inside",
                "body": f"""Hi {first_name},

I wanted to personally reach out because I believe the solution we've been discussing can make a significant impact at {company}.

I understand that priorities shift, and I want to make sure we're aligned with what matters most to your team right now. Based on our conversations and the challenges facing {industry} companies like {company}, I've prepared:

📊 A customized ROI analysis showing projected impact for {company}
🎯 An exclusive early-adopter package with preferential terms
📅 Priority implementation timeline with dedicated support

I'd love to schedule a brief 15-minute call to walk you through this — I'm confident it will be worth your time.

Would tomorrow or the day after work for a quick conversation?

Best regards,
Nexus Sales Team""",
                "tone": "urgent-professional",
                "cta": "Schedule call within 24 hours"
            }
        elif urgency == "high":
            return {
                "subject": f"Quick update for {company} — new insights for {industry}",
                "body": f"""Hi {first_name},

I came across some exciting developments in {industry} that I think are highly relevant to {company}'s goals.

We've recently helped a similar company achieve:
✅ 35% improvement in operational efficiency
✅ ROI within the first quarter
✅ Seamless integration with existing systems

I'd love to share the details and discuss how this could apply to your specific situation. We have a meeting scheduled, and I wanted to make sure you have everything you need to make the most of our time together.

Is there anything specific you'd like me to prepare or address?

Best,
Nexus Sales Team""",
                "tone": "consultative",
                "cta": "Confirm meeting and set agenda"
            }
        else:
            return {
                "subject": f"Exciting opportunity for {company}'s next chapter",
                "body": f"""Hi {first_name},

Great to see the momentum building on our collaboration discussion! I wanted to share a few things that might be useful as you evaluate:

🔍 Industry Report: Top trends shaping {industry} in 2026
💡 Success Story: How a company similar to {company} accelerated growth by 40%
📋 Next Steps: A clear roadmap for what our partnership would look like

I'm excited about the potential here and want to make sure you have all the information you need.

Let me know if you have any questions!

Cheers,
Nexus Sales Team""",
                "tone": "enthusiastic",
                "cta": "Share resources and maintain engagement"
            }

    def _generate_whatsapp(self, first_name, company, industry, urgency):
        if urgency == "critical":
            return {
                "message": f"Hi {first_name}! 👋 I sent you an email with a customized proposal for {company}. I've included some exclusive terms that I think you'll find compelling. Would you have 10 minutes this week for a quick call? I'm flexible on timing! 📞",
                "tone": "friendly-urgent",
                "emoji_strategy": "professional with light emoji use"
            }
        elif urgency == "high":
            return {
                "message": f"Hey {first_name}! 😊 Just shared some interesting {industry} insights via email that I thought you'd find valuable. Looking forward to our discussion — let me know if there's anything specific you'd like to explore! 🚀",
                "tone": "friendly-professional",
                "emoji_strategy": "warm and approachable"
            }
        else:
            return {
                "message": f"Hi {first_name}! Hope you're having a great week! 🙌 Just wanted to check in and see if you had a chance to review the materials I shared. Happy to answer any questions about how this could work for {company}! 💡",
                "tone": "casual-friendly",
                "emoji_strategy": "warm and casual"
            }

    def _generate_linkedin(self, first_name, company, industry, urgency):
        if urgency == "critical":
            return {
                "message": f"Hi {first_name}, I've been following {company}'s impressive work in {industry}. I've prepared a tailored analysis that shows how our solution could drive significant ROI for your team. I'd welcome a brief conversation — would you be open to connecting this week?",
                "tone": "professional-direct",
                "approach": "Value-first with clear CTA"
            }
        elif urgency == "high":
            return {
                "message": f"Hi {first_name}! I noticed some exciting trends in {industry} that align perfectly with what {company} is building. I'd love to share some insights that could be valuable for your team. Looking forward to connecting!",
                "tone": "professional-consultative",
                "approach": "Insight-led engagement"
            }
        else:
            return {
                "message": f"Hi {first_name}, great to connect! I work with several {industry} companies and I'm impressed by what {company} is doing. Would love to exchange perspectives on where the industry is heading. Cheers!",
                "tone": "professional-casual",
                "approach": "Relationship building"
            }
