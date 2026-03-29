


class RevenueImpactAgent:
    name = "Revenue Impact Agent"

    def analyze(self, deal: dict, deal_analysis: dict, strategy: dict) -> dict:
        deal_value = deal.get("deal_value", 0)
        original_probability = deal.get("probability", 50)
        risk_score = deal_analysis.get("risk_score", 0)
        adjusted_probability = deal_analysis.get("adjusted_probability", original_probability)
        urgency = strategy.get("urgency", "moderate")

        revenue_before = deal_value * (original_probability / 100)

        intervention_boost = self._calculate_boost(risk_score, urgency, strategy)

        post_intervention_probability = min(95, adjusted_probability + intervention_boost)

        revenue_after = deal_value * (post_intervention_probability / 100)

        revenue_recovered = max(0, revenue_after - revenue_before)

        actions_count = strategy.get("total_actions", 0)
        estimated_effort_hours = actions_count * 2  # 2 hours per action
        hourly_rate = 2000  # ₹2000/hour
        intervention_cost = estimated_effort_hours * hourly_rate
        roi = (revenue_recovered / max(intervention_cost, 1)) * 100 if intervention_cost > 0 else 0

        reasoning = self._build_reasoning(
            deal, original_probability, adjusted_probability,
            post_intervention_probability, intervention_boost,
            revenue_before, revenue_after, revenue_recovered, roi
        )

        return {
            "agent": self.name,
            "deal_id": deal.get("id"),
            "deal_value": deal_value,
            "original_probability": original_probability,
            "ai_adjusted_probability": adjusted_probability,
            "post_intervention_probability": post_intervention_probability,
            "intervention_boost": intervention_boost,
            "expected_revenue_before": round(revenue_before, 2),
            "expected_revenue_after": round(revenue_after, 2),
            "revenue_recovered": round(revenue_recovered, 2),
            "revenue_saved_display": f"₹{revenue_recovered:,.0f}",
            "roi_percentage": round(roi, 1),
            "intervention_cost_estimate": intervention_cost,
            "impact_summary": {
                "probability_change": f"{original_probability}% → {post_intervention_probability}% (+{post_intervention_probability - original_probability}pp)",
                "revenue_change": f"₹{revenue_before:,.0f} → ₹{revenue_after:,.0f}",
                "net_recovery": f"₹{revenue_recovered:,.0f}",
                "roi": f"{roi:.0f}x return on intervention effort"
            },
            "reasoning": reasoning
        }

    def _calculate_boost(self, risk_score, urgency, strategy):
        base_boost = 0
        if urgency == "critical":
            base_boost = 35
        elif urgency == "high":
            base_boost = 20
        else:
            base_boost = 10

        actions = strategy.get("total_actions", 0)
        action_bonus = min(15, actions * 3)

        return base_boost + action_bonus

    def _build_reasoning(self, deal, orig_prob, adj_prob, post_prob, boost, rev_before, rev_after, recovered, roi):
        parts = []
        company = deal.get("company", "Unknown")
        deal_value = deal.get("deal_value", 0)

        parts.append(f"Revenue Impact Analysis for {company} (Deal Value: ₹{deal_value:,.0f}):")
        parts.append(f"BEFORE AI: {orig_prob}% probability → Expected Revenue: ₹{rev_before:,.0f}")
        parts.append(f"AI Risk Assessment adjusted probability to {adj_prob}%, identifying deal vulnerabilities.")
        parts.append(f"AFTER AI Intervention Strategy: Probability boosted by +{boost}pp to {post_prob}%.")
        parts.append(f"Expected Revenue AFTER: ₹{rev_after:,.0f}")
        parts.append(f"💰 REVENUE RECOVERED BY AI: ₹{recovered:,.0f}")
        parts.append(f"📈 ROI: {roi:.0f}x return on intervention effort.")

        if recovered > 0:
            parts.append(f"The AI system's intervention strategies are projected to recover ₹{recovered:,.0f} in pipeline value that would otherwise be at risk of loss.")

        return " ".join(parts)
