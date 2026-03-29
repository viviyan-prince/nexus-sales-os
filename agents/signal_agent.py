
from datetime import datetime, timedelta


class SignalAgent:
    name = "Signal Agent"

    def analyze(self, deal: dict) -> dict:
        last_contact = deal.get("last_contact_date", "")
        email_opened = deal.get("email_opened", False)
        reply_received = deal.get("reply_received", False)
        meeting_status = deal.get("meeting_status", "None")


        days_silent = 0
        if last_contact:
            try:
                lc = datetime.strptime(last_contact, "%Y-%m-%d")
                days_silent = (datetime.now() - lc).days
            except ValueError:
                days_silent = 0

        signals = []
        engagement_score = 100

        if days_silent >= 5:
            signals.append({"type": "critical", "message": f"No contact for {days_silent} days — client may be disengaging"})
            engagement_score -= 35
        elif days_silent >= 3:
            signals.append({"type": "warning", "message": f"Last contact was {days_silent} days ago — follow-up needed"})
            engagement_score -= 15

        if not email_opened:
            signals.append({"type": "critical", "message": "Last email was NOT opened — message may be ignored or in spam"})
            engagement_score -= 25
        else:
            signals.append({"type": "positive", "message": "Email was opened — contact is aware of communication"})

        if not reply_received:
            signals.append({"type": "warning", "message": "No reply received — one-directional communication"})
            engagement_score -= 20
        else:
            signals.append({"type": "positive", "message": "Reply received — active bi-directional engagement"})

        if meeting_status == "Cancelled":
            signals.append({"type": "critical", "message": "Meeting was CANCELLED — potential loss of interest"})
            engagement_score -= 20
        elif meeting_status == "Completed":
            signals.append({"type": "positive", "message": "Meeting completed — strong engagement signal"})
            engagement_score += 10
        elif meeting_status == "Scheduled":
            signals.append({"type": "positive", "message": "Meeting scheduled — engagement is active"})
            engagement_score += 5
        else:
            signals.append({"type": "warning", "message": "No meeting scheduled — limited face-to-face engagement"})
            engagement_score -= 10

        engagement_score = max(0, min(100, engagement_score))

        if engagement_score < 30:
            level = "Critical"
        elif engagement_score < 50:
            level = "Low"
        elif engagement_score < 70:
            level = "Medium"
        else:
            level = "High"

        reasoning_parts = []
        critical_signals = [s for s in signals if s["type"] == "critical"]
        if critical_signals:
            reasoning_parts.append(f"Found {len(critical_signals)} critical signal(s): " +
                                   "; ".join(s["message"] for s in critical_signals))
        if days_silent >= 5:
            reasoning_parts.append(f"The {days_silent}-day silence pattern suggests the deal champion may have gone cold or internal priorities have shifted.")
        if not email_opened and not reply_received:
            reasoning_parts.append("Complete communication blackout — the contact is not engaging with any outreach attempts.")

        return {
            "agent": self.name,
            "engagement_score": engagement_score,
            "engagement_level": level,
            "days_since_contact": days_silent,
            "signals": signals,
            "risk_indicators": [s["message"] for s in signals if s["type"] in ("critical", "warning")],
            "positive_indicators": [s["message"] for s in signals if s["type"] == "positive"],
            "reasoning": " ".join(reasoning_parts) if reasoning_parts else "Engagement signals are within normal range. No immediate concerns detected.",
            "recommendation": self._get_recommendation(engagement_score, days_silent, meeting_status)
        }

    def _get_recommendation(self, score, days_silent, meeting_status):
        if score < 30:
            return "URGENT: Escalate immediately. Consider executive sponsor outreach or an in-person meeting to re-engage the client."
        if score < 50:
            return "Schedule a call within 24 hours. Use a value-driven approach — share a case study or ROI analysis to reignite interest."
        if score < 70:
            return "Send a personalized follow-up within 48 hours. Reference specific pain points discussed earlier."
        return "Engagement is healthy. Continue current cadence and prepare for next stage advancement."
