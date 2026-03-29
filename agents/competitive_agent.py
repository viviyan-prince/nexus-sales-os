


class CompetitiveAgent:
    name = "Competitive Intelligence Agent"

    COMPETITOR_DB = {
        "SaaS": {
            "competitors": ["Salesforce", "HubSpot", "Zoho CRM"],
            "our_strengths": ["AI-powered automation", "Faster implementation", "Lower TCO", "Superior analytics"],
            "common_objections": [
                "We already use Salesforce",
                "Your platform is newer / less proven",
                "We need enterprise-grade security",
                "Integration with existing tools"
            ]
        },
        "FinTech": {
            "competitors": ["Bloomberg Terminal", "Refinitiv", "FactSet"],
            "our_strengths": ["Modern AI capabilities", "Cost-effective", "Cloud-native", "Rapid deployment"],
            "common_objections": [
                "Regulatory compliance concerns",
                "Data security requirements",
                "Need real-time feeds",
                "Existing vendor contracts"
            ]
        },
        "CleanTech": {
            "competitors": ["Enverus", "Power Factors", "Stem Inc"],
            "our_strengths": ["Cross-sector analytics", "Predictive maintenance AI", "Carbon tracking", "Unified platform"],
            "common_objections": [
                "Industry-specific requirements",
                "Need on-premise deployment",
                "Complex data integrations",
                "Long procurement cycles"
            ]
        },
        "default": {
            "competitors": ["Established incumbents", "Niche point solutions", "In-house solutions"],
            "our_strengths": ["AI-first architecture", "Rapid deployment", "Superior UX", "Proven ROI"],
            "common_objections": [
                "We already have a solution",
                "Budget constraints",
                "Implementation timeline concerns",
                "Team adoption risks"
            ]
        }
    }

    def analyze(self, deal: dict) -> dict:
        industry = deal.get("industry", "default")
        company = deal.get("company", "Unknown")
        deal_value = deal.get("deal_value", 0)

        intel = self.COMPETITOR_DB.get(industry, self.COMPETITOR_DB["default"])

        battlecards = []
        for competitor in intel["competitors"]:
            battlecards.append({
                "competitor": competitor,
                "key_differentiators": [
                    f"Our AI automation reduces manual effort by 60% compared to {competitor}",
                    f"Implementation time is 3x faster than {competitor}",
                    f"TCO is 40% lower over 3 years vs. {competitor}"
                ],
                "win_strategy": f"Lead with ROI data. Show {company} how we outperform {competitor} on automation, speed, and cost. Use customer testimonials from {industry} sector.",
                "risk_factors": [f"{competitor}'s brand recognition", "Existing integrations", "Switching costs"],
                "counter_narrative": f"While {competitor} has market presence, our AI-native approach delivers measurably better outcomes. We're not replacing a legacy tool — we're upgrading to intelligent automation."
            })

        objection_handlers = []
        for objection in intel["common_objections"]:
            handler = self._generate_handler(objection, company, industry, intel["our_strengths"])
            objection_handlers.append(handler)

        positioning = {
            "headline": f"The AI-Native Revenue Intelligence Platform for {industry}",
            "value_proposition": f"We help {industry} companies like {company} increase revenue by 35% through autonomous AI-powered sales intelligence — not just analytics, but actionable decisions.",
            "key_messages": [
                f"Purpose-built for {industry} with deep domain expertise",
                "AI agents that don't just analyze — they act",
                "Proven ROI within 90 days",
                f"Trusted by leading {industry} companies"
            ],
            "proof_points": [
                {"metric": "35%", "description": "Average revenue increase for customers"},
                {"metric": "60%", "description": "Reduction in manual sales operations"},
                {"metric": "90 days", "description": "Average time to measurable ROI"},
                {"metric": "3x", "description": "Faster pipeline velocity"}
            ]
        }

        reasoning = f"Analyzed competitive landscape for {company} in {industry}. Identified {len(intel['competitors'])} primary competitors. Generated {len(battlecards)} battlecards and {len(objection_handlers)} objection handlers. Positioning strategy emphasizes AI-native differentiation and proven ROI to counter incumbent advantages."

        return {
            "agent": self.name,
            "deal_id": deal.get("id"),
            "industry": industry,
            "battlecards": battlecards,
            "objection_handlers": objection_handlers,
            "positioning": positioning,
            "competitive_advantage_score": 78,
            "reasoning": reasoning
        }

    def _generate_handler(self, objection, company, industry, strengths):
        handlers = {
            "We already use Salesforce": {
                "objection": objection,
                "response": "I completely understand — Salesforce is a powerful CRM. What we offer is complementary: an AI intelligence layer that sits on top of your existing CRM and actively identifies risks, automates outreach, and recovers revenue. Many of our customers use us alongside Salesforce.",
                "proof": "Our Salesforce integration takes 2 hours to set up, and customers see value within the first week.",
                "approach": "Complement, don't compete"
            },
            "Budget constraints": {
                "objection": objection,
                "response": f"I hear you. That's exactly why we focus on demonstrating ROI first. For a deal size like {company}'s, our customers typically see 5-10x return within the first quarter. We also offer flexible pricing to align with your budget cycle.",
                "proof": "Average customer saves 40% more revenue than the platform costs within 90 days.",
                "approach": "ROI-first justification"
            }
        }

        if objection in handlers:
            return handlers[objection]

        return {
            "objection": objection,
            "response": f"Great question. This is something we hear from {industry} companies regularly, and we've designed our solution specifically to address this. Our {strengths[0].lower()} approach means {company} can overcome this concern while gaining competitive advantage.",
            "proof": f"We've helped multiple {industry} companies successfully navigate this exact concern.",
            "approach": "Acknowledge, address, redirect to value"
        }
