


class ProspectingAgent:
    name = "Prospecting Agent"

    ICP_WEIGHTS = {
        "industry": 25,
        "size": 20,
        "engagement": 30,
        "signals": 25
    }

    TARGET_INDUSTRIES = ["AI/ML", "SaaS", "FinTech", "Cloud Infrastructure", "CleanTech", "HealthTech"]
    PREFERRED_SIZES = ["Enterprise", "Mid-Market"]

    def analyze(self, prospect: dict) -> dict:
        icp_score = 0
        icp_breakdown = {}


        industry = prospect.get("industry", "")
        if industry in self.TARGET_INDUSTRIES:
            ind_score = 25
        elif any(kw in industry.lower() for kw in ["tech", "digital", "software"]):
            ind_score = 15
        else:
            ind_score = 5
        icp_score += ind_score
        icp_breakdown["industry_fit"] = {"score": ind_score, "max": 25, "detail": f"{industry} — {'strong' if ind_score >= 20 else 'moderate' if ind_score >= 10 else 'weak'} ICP match"}


        size = prospect.get("size", "SMB")
        if size in self.PREFERRED_SIZES:
            size_score = 20
        elif size == "SMB":
            size_score = 12
        else:
            size_score = 5
        icp_score += size_score
        icp_breakdown["company_size"] = {"score": size_score, "max": 20, "detail": f"{size} segment — {'ideal' if size_score >= 18 else 'acceptable'} fit"}


        visits = prospect.get("website_visits", 0)
        downloads = prospect.get("content_downloads", 0)
        engage_score = min(30, (visits * 2) + (downloads * 5))
        icp_score += engage_score
        icp_breakdown["digital_engagement"] = {"score": engage_score, "max": 30, "detail": f"{visits} site visits, {downloads} content downloads"}


        signals = prospect.get("engagement_signals", [])
        sig_score = min(25, len(signals) * 8)
        icp_score += sig_score
        icp_breakdown["engagement_signals"] = {"score": sig_score, "max": 25, "detail": f"{len(signals)} active signal(s)"}

        icp_score = min(100, icp_score)

        if icp_score >= 70:
            engagement_level = "Hot"
        elif icp_score >= 40:
            engagement_level = "Warm"
        else:
            engagement_level = "Cold"

        outreach_sequence = self._generate_outreach(prospect, icp_score, engagement_level)

        reasoning = self._build_reasoning(prospect, icp_score, engagement_level, icp_breakdown)

        return {
            "agent": self.name,
            "prospect_id": prospect.get("id"),
            "icp_score": icp_score,
            "engagement_level": engagement_level,
            "icp_breakdown": icp_breakdown,
            "outreach_sequence": outreach_sequence,
            "reasoning": reasoning,
            "recommended_priority": "immediate" if engagement_level == "Hot" else "this_week" if engagement_level == "Warm" else "nurture"
        }

    def _generate_outreach(self, prospect, icp_score, level):
        name = prospect.get("contact_name", "there")
        company = prospect.get("company", "your company")
        industry = prospect.get("industry", "your industry")

        if level == "Hot":
            return [
                {"touch": 1, "day": 1, "channel": "Email", "action": f"Personalized intro email to {name} — reference their {industry} focus and recent engagement signals. Offer a 15-min strategic call."},
                {"touch": 2, "day": 2, "channel": "LinkedIn", "action": f"Connect with {name} on LinkedIn with a personalized note mentioning mutual industry interests."},
                {"touch": 3, "day": 4, "channel": "Email", "action": f"Follow-up with a relevant case study from {industry} showing measurable ROI. Include specific metrics."},
                {"touch": 4, "day": 6, "channel": "WhatsApp", "action": f"Send a brief WhatsApp message: 'Hi {name}, shared a {industry} case study via email — would love to discuss how we can help {company} achieve similar results. Free for a quick chat?'"},
                {"touch": 5, "day": 8, "channel": "Email", "action": f"Final value-driven email with a personalized demo link and a time-boxed offer for a strategy session."}
            ]
        elif level == "Warm":
            return [
                {"touch": 1, "day": 1, "channel": "Email", "action": f"Introduction email to {name} — highlight how companies in {industry} are transforming their revenue operations."},
                {"touch": 2, "day": 3, "channel": "LinkedIn", "action": f"Engage with {name}'s LinkedIn content (like/comment) before sending a connection request."},
                {"touch": 3, "day": 5, "channel": "Email", "action": f"Share an industry insight piece relevant to {company}'s likely challenges in {industry}."},
                {"touch": 4, "day": 8, "channel": "Email", "action": f"Send a comparison guide showing how peers in the {industry} space are leveraging AI for revenue growth."},
                {"touch": 5, "day": 12, "channel": "WhatsApp", "action": f"Casual message to {name}: 'Hi! I've been sharing some insights on {industry} transformation — would a 10-min call be valuable to explore this further?'"}
            ]
        else:
            return [
                {"touch": 1, "day": 1, "channel": "Email", "action": f"Cold outreach to {name} at {company} — lead with a provocative industry statistic about {industry}."},
                {"touch": 2, "day": 5, "channel": "LinkedIn", "action": f"View {name}'s LinkedIn profile, then send a connection request with a brief industry-relevant note."},
                {"touch": 3, "day": 10, "channel": "Email", "action": f"Follow-up email with a complimentary resource (whitepaper/webinar) relevant to {industry}."},
                {"touch": 4, "day": 15, "channel": "Email", "action": f"Share a success story from a company similar to {company} in terms of size and industry."},
                {"touch": 5, "day": 21, "channel": "LinkedIn", "action": f"Send a LinkedIn direct message offering a no-strings-attached industry consultation."}
            ]

    def _build_reasoning(self, prospect, icp_score, level, breakdown):
        name = prospect.get("contact_name", "Prospect")
        company = prospect.get("company", "Unknown")
        parts = [f"{name} at {company} has an ICP fit score of {icp_score}/100 ({level} lead)."]
        for key, val in breakdown.items():
            parts.append(f"{key.replace('_', ' ').title()}: {val['score']}/{val['max']} — {val['detail']}.")
        if level == "Hot":
            parts.append("RECOMMENDATION: Immediate outreach recommended. This prospect shows strong buying signals.")
        elif level == "Warm":
            parts.append("RECOMMENDATION: Prioritize this week. Build engagement through value-driven content before hard pitch.")
        else:
            parts.append("RECOMMENDATION: Place in nurture sequence. Focus on education and awareness building.")
        return " ".join(parts)
