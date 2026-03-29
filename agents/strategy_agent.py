


class StrategyAgent:
    name = "Strategy Agent"

    def analyze(self, deal: dict, risk_score: float, engagement_level: str, signal_data: dict = None) -> dict:
        strategies = []
        primary_strategy = ""
        urgency = "low"

        deal_value = deal.get("deal_value", 0)
        stage = deal.get("stage", "Prospecting")
        days_in_stage = deal.get("days_in_stage", 0)
        probability = deal.get("probability", 50)


        if risk_score >= 70:
            urgency = "critical"
            primary_strategy = "Executive Escalation & Recovery"
            strategies = [
                {
                    "action": "Executive Sponsor Outreach",
                    "description": "Arrange a call between your VP/CXO and the client's decision maker within 24 hours",
                    "priority": "critical",
                    "timeline": "Immediate",
                    "expected_impact": "Re-establish trust and urgency at the executive level"
                },
                {
                    "action": "Revised Value Proposition",
                    "description": "Prepare a customized ROI analysis based on the client's specific pain points and industry benchmarks",
                    "priority": "high",
                    "timeline": "Within 24 hours",
                    "expected_impact": "Address potential objections with data-driven business case"
                },
                {
                    "action": "Strategic Discount / Incentive",
                    "description": f"Offer a time-limited 10-15% discount or added value package to create urgency (potential savings: ₹{deal_value*0.1:,.0f} - ₹{deal_value*0.15:,.0f})",
                    "priority": "medium",
                    "timeline": "Present during executive call",
                    "expected_impact": "Overcome budget objections and create urgency"
                },
                {
                    "action": "Multi-Channel Re-engagement",
                    "description": "Execute simultaneous outreach via Email + LinkedIn + WhatsApp to maximize touchpoints",
                    "priority": "high",
                    "timeline": "Within 12 hours",
                    "expected_impact": "Break through communication barriers"
                }
            ]


        elif risk_score >= 40:
            urgency = "high"
            primary_strategy = "Proactive Engagement & Acceleration"
            strategies = [
                {
                    "action": "Personalized Follow-Up Call",
                    "description": "Schedule a focused 20-minute call to address concerns and present next steps",
                    "priority": "high",
                    "timeline": "Within 24-48 hours",
                    "expected_impact": "Maintain momentum and address potential blockers"
                },
                {
                    "action": "Stakeholder Mapping",
                    "description": "Identify and engage additional stakeholders who can champion the deal internally",
                    "priority": "medium",
                    "timeline": "Within 48 hours",
                    "expected_impact": "Build consensus and reduce dependency on single contact"
                },
                {
                    "action": "Urgency Message",
                    "description": "Send a time-sensitive communication highlighting upcoming changes, limited availability, or competitive advantage",
                    "priority": "medium",
                    "timeline": "Within 24 hours",
                    "expected_impact": "Create a reason for the client to prioritize this decision"
                }
            ]


        else:
            urgency = "moderate"
            primary_strategy = "Strategic Advancement"
            strategies = [
                {
                    "action": "Stage Advancement Push",
                    "description": f"Prepare materials to move deal from {stage} to next stage",
                    "priority": "medium",
                    "timeline": "This week",
                    "expected_impact": "Accelerate deal velocity and demonstrate progress"
                },
                {
                    "action": "Relationship Deepening",
                    "description": "Share exclusive industry insights or invite to an upcoming event/webinar",
                    "priority": "low",
                    "timeline": "Within the week",
                    "expected_impact": "Build stronger relationship for long-term partnership"
                }
            ]

        reasoning = self._build_reasoning(deal, risk_score, urgency, primary_strategy, strategies)

        return {
            "agent": self.name,
            "deal_id": deal.get("id"),
            "primary_strategy": primary_strategy,
            "urgency": urgency,
            "strategies": strategies,
            "total_actions": len(strategies),
            "reasoning": reasoning
        }

    def _build_reasoning(self, deal, risk_score, urgency, primary_strategy, strategies):
        parts = [
            f"Based on a risk score of {risk_score}/100, the recommended strategy is '{primary_strategy}' with {urgency.upper()} urgency.",
            f"Deal value of ₹{deal.get('deal_value', 0):,.0f} in {deal.get('stage')} stage warrants {len(strategies)} coordinated actions."
        ]
        if urgency == "critical":
            parts.append("The window for recovery is narrowing. Immediate, multi-channel intervention is essential to prevent deal loss.")
        elif urgency == "high":
            parts.append("Proactive engagement now can prevent escalation to critical status. Focus on demonstrating value and removing friction.")
        else:
            parts.append("Deal is on track. Focus on advancing to the next stage while deepening the relationship.")
        return " ".join(parts)
