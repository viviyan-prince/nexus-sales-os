
from datetime import datetime


class DealAgent:
    name = "Deal Intelligence Agent"

    def analyze(self, deal: dict, signal_data: dict = None) -> dict:
        risk_score = 0
        risk_factors = []
        positive_factors = []

        stage = deal.get("stage", "Prospecting")
        days_in_stage = deal.get("days_in_stage", 0)
        probability = deal.get("probability", 50)
        deal_value = deal.get("deal_value", 0)
        email_opened = deal.get("email_opened", False)
        reply_received = deal.get("reply_received", False)
        meeting_status = deal.get("meeting_status", "None")

        days_silent = 0
        last_contact = deal.get("last_contact_date", "")
        if last_contact:
            try:
                lc = datetime.strptime(last_contact, "%Y-%m-%d")
                days_silent = (datetime.now() - lc).days
            except ValueError:
                pass




        stage_limits = {"Prospecting": 7, "Qualification": 10, "Proposal": 14, "Negotiation": 10}
        limit = stage_limits.get(stage, 10)
        if days_in_stage > limit * 2:
            risk_score += 30
            risk_factors.append({
                "factor": "Severe Stage Stagnation",
                "detail": f"Deal stuck in {stage} for {days_in_stage} days (healthy: {limit} days)",
                "severity": "critical",
                "impact": 30
            })
        elif days_in_stage > limit:
            risk_score += 15
            risk_factors.append({
                "factor": "Stage Delay",
                "detail": f"Deal in {stage} for {days_in_stage} days (healthy: {limit} days)",
                "severity": "high",
                "impact": 15
            })
        else:
            positive_factors.append(f"Deal is progressing normally in {stage} ({days_in_stage}/{limit} days)")


        if days_silent >= 5:
            risk_score += 25
            risk_factors.append({
                "factor": "Communication Blackout",
                "detail": f"No contact for {days_silent} days — client may be evaluating competitors",
                "severity": "critical",
                "impact": 25
            })
        elif days_silent >= 3:
            risk_score += 10
            risk_factors.append({
                "factor": "Communication Gap",
                "detail": f"Last contact was {days_silent} days ago",
                "severity": "medium",
                "impact": 10
            })


        if not email_opened:
            risk_score += 15
            risk_factors.append({
                "factor": "Email Not Opened",
                "detail": "Latest email was not opened — contact may be unresponsive",
                "severity": "high",
                "impact": 15
            })

        if not reply_received:
            risk_score += 10
            risk_factors.append({
                "factor": "No Reply Received",
                "detail": "Contact has not replied to latest communication",
                "severity": "medium",
                "impact": 10
            })
        else:
            positive_factors.append("Active reply engagement")


        if meeting_status == "Cancelled":
            risk_score += 20
            risk_factors.append({
                "factor": "Meeting Cancelled",
                "detail": "Scheduled meeting was cancelled — signals deprioritization",
                "severity": "critical",
                "impact": 20
            })
        elif meeting_status == "Completed":
            risk_score -= 10
            positive_factors.append("Meeting was completed — strong engagement")
        elif meeting_status == "Scheduled":
            positive_factors.append("Meeting is scheduled — pipeline has momentum")

        risk_score = max(0, min(100, risk_score))

        if risk_score >= 70:
            adjusted_probability = max(10, probability - 30)
            forecast_adjustment = -30
        elif risk_score >= 50:
            adjusted_probability = max(15, probability - 15)
            forecast_adjustment = -15
        elif risk_score >= 30:
            adjusted_probability = max(20, probability - 5)
            forecast_adjustment = -5
        else:
            adjusted_probability = min(95, probability + 5)
            forecast_adjustment = 5

        if risk_score >= 70:
            risk_level = "High"
        elif risk_score >= 40:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        reasoning = self._build_reasoning(deal, risk_score, risk_level, risk_factors, positive_factors,
                                          adjusted_probability, forecast_adjustment)

        return {
            "agent": self.name,
            "deal_id": deal.get("id"),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "positive_factors": positive_factors,
            "original_probability": probability,
            "adjusted_probability": adjusted_probability,
            "forecast_adjustment": forecast_adjustment,
            "deal_health_score": 100 - risk_score,
            "reasoning": reasoning
        }

    def _build_reasoning(self, deal, risk_score, risk_level, risk_factors, positive_factors, adj_prob, adj):
        parts = []
        parts.append(f"Deal with {deal.get('company')} has a risk score of {risk_score}/100 ({risk_level} risk).")

        critical = [rf for rf in risk_factors if rf["severity"] == "critical"]
        if critical:
            parts.append(f"CRITICAL ISSUES: {', '.join(rf['factor'] for rf in critical)}.")

        if risk_score >= 70:
            parts.append(f"This deal requires IMMEDIATE intervention. Probability adjusted from {deal.get('probability')}% to {adj_prob}% ({adj:+d}pp).")
            parts.append("Recommend executive-level engagement and a revised proposal strategy.")
        elif risk_score >= 40:
            parts.append(f"Several risk indicators detected. Probability adjusted to {adj_prob}% ({adj:+d}pp). Proactive follow-up recommended within 24-48 hours.")
        else:
            parts.append(f"Deal is progressing well with a healthy risk profile. Probability adjusted to {adj_prob}% ({adj:+d}pp).")

        if positive_factors:
            parts.append(f"Positive signals: {'; '.join(positive_factors[:3])}.")

        return " ".join(parts)
