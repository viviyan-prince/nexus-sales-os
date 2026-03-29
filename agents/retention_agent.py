
from datetime import datetime


class RetentionAgent:
    name = "Revenue Retention Agent"

    def analyze(self, customer: dict) -> dict:
        churn_score = 0
        churn_factors = []
        positive_signals = []

        mrr = customer.get("mrr", 0)
        sentiment = customer.get("sentiment", "Neutral")
        support_tickets = customer.get("support_tickets", 0)
        last_login_days = customer.get("last_login_days_ago", 0)
        feature_adoption = customer.get("feature_adoption", 50)
        usage_data = customer.get("usage_data", {})


        logins = usage_data.get("logins_last_30d", 15)
        if logins <= 3:
            churn_score += 30
            churn_factors.append({"factor": "Very Low Login Frequency", "detail": f"Only {logins} logins in 30 days — well below healthy threshold of 15+", "severity": "critical", "impact": 30})
        elif logins <= 10:
            churn_score += 15
            churn_factors.append({"factor": "Below Average Login Frequency", "detail": f"{logins} logins in 30 days — below healthy threshold", "severity": "warning", "impact": 15})
        else:
            positive_signals.append(f"Strong login frequency: {logins} logins in 30 days")


        if feature_adoption < 25:
            churn_score += 25
            churn_factors.append({"factor": "Critical Feature Adoption", "detail": f"Only {feature_adoption:.0f}% of features adopted — high risk of perceived low value", "severity": "critical", "impact": 25})
        elif feature_adoption < 50:
            churn_score += 12
            churn_factors.append({"factor": "Low Feature Adoption", "detail": f"{feature_adoption:.0f}% feature adoption — opportunity for training", "severity": "warning", "impact": 12})
        else:
            positive_signals.append(f"Good feature adoption at {feature_adoption:.0f}%")


        if sentiment == "Negative":
            churn_score += 20
            churn_factors.append({"factor": "Negative Sentiment", "detail": "Customer sentiment is negative — potential dissatisfaction", "severity": "critical", "impact": 20})
        elif sentiment == "Neutral":
            churn_score += 5
        else:
            positive_signals.append("Positive customer sentiment")


        if support_tickets >= 5:
            churn_score += 15
            churn_factors.append({"factor": "High Support Volume", "detail": f"{support_tickets} support tickets — indicates friction or product issues", "severity": "high", "impact": 15})
        elif support_tickets >= 3:
            churn_score += 8
            churn_factors.append({"factor": "Elevated Support Volume", "detail": f"{support_tickets} support tickets", "severity": "warning", "impact": 8})


        if last_login_days >= 14:
            churn_score += 15
            churn_factors.append({"factor": "Inactive Account", "detail": f"Last login {last_login_days} days ago", "severity": "critical", "impact": 15})
        elif last_login_days >= 7:
            churn_score += 8
            churn_factors.append({"factor": "Declining Activity", "detail": f"Last login {last_login_days} days ago", "severity": "warning", "impact": 8})


        api_trend = usage_data.get("api_calls_trend", "stable")
        if api_trend == "declining":
            churn_score += 10
            churn_factors.append({"factor": "Declining API Usage", "detail": "API call volume is trending down", "severity": "warning", "impact": 10})
        elif api_trend == "growing":
            positive_signals.append("API usage is growing — healthy integration")

        churn_score = min(100, max(0, churn_score))
        mrr_at_risk = mrr * (churn_score / 100)


        intervention = self._build_intervention(customer, churn_score, churn_factors, mrr)


        if churn_score >= 70:
            churn_level = "Critical"
        elif churn_score >= 40:
            churn_level = "Elevated"
        else:
            churn_level = "Low"


        contract_end = customer.get("contract_end_date", "")
        days_to_renewal = 365
        if contract_end:
            try:
                end_date = datetime.strptime(contract_end, "%Y-%m-%d")
                days_to_renewal = (end_date - datetime.now()).days
            except ValueError:
                pass

        reasoning = self._build_reasoning(customer, churn_score, churn_level, churn_factors, mrr, mrr_at_risk, days_to_renewal)

        return {
            "agent": self.name,
            "customer_id": customer.get("id"),
            "churn_probability": churn_score,
            "churn_level": churn_level,
            "mrr": mrr,
            "mrr_at_risk": round(mrr_at_risk, 2),
            "annual_revenue_at_risk": round(mrr_at_risk * 12, 2),
            "churn_factors": churn_factors,
            "positive_signals": positive_signals,
            "intervention_plan": intervention,
            "days_to_renewal": days_to_renewal,
            "reasoning": reasoning
        }

    def _build_intervention(self, customer, churn_score, factors, mrr):
        name = customer.get("contact_name", "Customer")
        company = customer.get("company", "")

        if churn_score >= 70:
            return {
                "urgency": "critical",
                "timeline": "Immediate (within 24 hours)",
                "actions": [
                    {"action": "Executive Health Check Call", "detail": f"Schedule immediate call between CS Director and {name} to understand concerns", "owner": "CS Director", "deadline": "24 hours"},
                    {"action": "Personalized Success Plan", "detail": f"Create a 30-day success plan with specific milestones and training sessions for {company}", "owner": "CSM", "deadline": "48 hours"},
                    {"action": "Feature Workshop", "detail": "Arrange a hands-on workshop to improve feature adoption and demonstrate full platform value", "owner": "Solutions Engineer", "deadline": "1 week"},
                    {"action": "Support Ticket Resolution", "detail": "Escalate all open tickets and resolve within SLA", "owner": "Support Lead", "deadline": "48 hours"},
                    {"action": "Renewal Incentive", "detail": f"Prepare a retention offer with enhanced terms or pricing adjustment (protect ₹{mrr:,.0f}/month)", "owner": "Account Manager", "deadline": "Before renewal discussion"}
                ]
            }
        elif churn_score >= 40:
            return {
                "urgency": "elevated",
                "timeline": "This week",
                "actions": [
                    {"action": "Proactive Check-In", "detail": f"Schedule a business review call with {name}", "owner": "CSM", "deadline": "This week"},
                    {"action": "Usage Optimization", "detail": "Share a usage guide highlighting underutilized features", "owner": "CSM", "deadline": "3 days"},
                    {"action": "Training Invitation", "detail": "Invite to upcoming webinar or training session", "owner": "Training Team", "deadline": "1 week"}
                ]
            }
        else:
            return {
                "urgency": "low",
                "timeline": "Ongoing",
                "actions": [
                    {"action": "Quarterly Business Review", "detail": "Maintain regular QBR schedule", "owner": "CSM", "deadline": "Next QBR"},
                    {"action": "Upsell Exploration", "detail": "Identify expansion opportunities based on strong usage patterns", "owner": "Account Manager", "deadline": "Next quarter"}
                ]
            }

    def _build_reasoning(self, customer, churn_score, churn_level, factors, mrr, mrr_at_risk, days_to_renewal):
        parts = [f"{customer.get('company')} has a churn probability of {churn_score}% ({churn_level} risk)."]
        parts.append(f"MRR of ₹{mrr:,.0f} with ₹{mrr_at_risk:,.0f}/month (₹{mrr_at_risk*12:,.0f}/year) at risk.")

        critical = [f for f in factors if f.get("severity") == "critical"]
        if critical:
            parts.append(f"Critical factors: {', '.join(f['factor'] for f in critical)}.")

        if days_to_renewal <= 60:
            parts.append(f"⚠️ Contract renewal in {days_to_renewal} days — making intervention particularly urgent.")

        if churn_score >= 70:
            parts.append("IMMEDIATE action required to prevent revenue loss. Multi-pronged intervention plan activated.")
        elif churn_score >= 40:
            parts.append("Proactive engagement recommended to address emerging risk signals before they escalate.")
        else:
            parts.append("Customer health is stable. Focus on deepening relationship and exploring expansion opportunities.")

        return " ".join(parts)
