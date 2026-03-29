


class PipelineAgent:
    name = "Pipeline Intelligence Agent"

    STAGE_ORDER = ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
    HEALTHY_DAYS = {"Prospecting": 7, "Qualification": 10, "Proposal": 14, "Negotiation": 10}

    def analyze(self, deals: list) -> dict:
        active_deals = [d for d in deals if d.get("stage") not in ("Closed Won", "Closed Lost")]
        total_pipeline = sum(d.get("deal_value", 0) for d in active_deals)

        stage_dist = {}
        stage_values = {}
        for stage in self.STAGE_ORDER:
            stage_deals = [d for d in active_deals if d.get("stage") == stage]
            stage_dist[stage] = len(stage_deals)
            stage_values[stage] = sum(d.get("deal_value", 0) for d in stage_deals)

        bottlenecks = []
        for d in active_deals:
            stage = d.get("stage", "Prospecting")
            days = d.get("days_in_stage", 0)
            limit = self.HEALTHY_DAYS.get(stage, 10)
            if days > limit:
                bottlenecks.append({
                    "deal_id": d.get("id"),
                    "client": d.get("client_name"),
                    "company": d.get("company"),
                    "stage": stage,
                    "days_in_stage": days,
                    "healthy_limit": limit,
                    "days_overdue": days - limit,
                    "deal_value": d.get("deal_value", 0),
                    "severity": "critical" if days > limit * 2 else "warning"
                })

        at_risk_deals = [d for d in active_deals if d.get("risk_score", 0) > 50 or d.get("days_in_stage", 0) > self.HEALTHY_DAYS.get(d.get("stage", ""), 10)]
        revenue_at_risk = sum(d.get("deal_value", 0) for d in at_risk_deals)

        weighted_pipeline = sum(d.get("deal_value", 0) * (d.get("probability", 50) / 100) for d in active_deals)

        avg_days = sum(d.get("days_in_stage", 0) for d in active_deals) / max(len(active_deals), 1)

        actions = []
        if bottlenecks:
            critical_bn = [b for b in bottlenecks if b["severity"] == "critical"]
            if critical_bn:
                actions.append({
                    "priority": "urgent",
                    "action": f"Immediately address {len(critical_bn)} critically stalled deal(s)",
                    "deals": [b["deal_id"] for b in critical_bn],
                    "impact": sum(b["deal_value"] for b in critical_bn)
                })
            actions.append({
                "priority": "high",
                "action": "Review pipeline velocity — multiple deals exceeding healthy stage duration",
                "details": f"{len(bottlenecks)} deal(s) are bottlenecked across the pipeline"
            })

        if revenue_at_risk > total_pipeline * 0.3:
            actions.append({
                "priority": "high",
                "action": f"Revenue exposure alert: ₹{revenue_at_risk:,.0f} ({revenue_at_risk/max(total_pipeline,1)*100:.0f}% of pipeline) is at risk",
                "details": "Consider deal acceleration strategies and risk mitigation plans"
            })

        if revenue_at_risk < total_pipeline * 0.2 and len(bottlenecks) == 0:
            health = "Excellent"
        elif revenue_at_risk < total_pipeline * 0.3 and len(bottlenecks) <= 1:
            health = "Good"
        elif revenue_at_risk < total_pipeline * 0.5:
            health = "Fair"
        else:
            health = "Critical"

        reasoning = self._build_reasoning(total_pipeline, revenue_at_risk, bottlenecks, avg_days, health)

        return {
            "agent": self.name,
            "total_pipeline_value": total_pipeline,
            "weighted_pipeline_value": round(weighted_pipeline, 2),
            "total_active_deals": len(active_deals),
            "revenue_at_risk": revenue_at_risk,
            "revenue_at_risk_pct": round(revenue_at_risk / max(total_pipeline, 1) * 100, 1),
            "stage_distribution": stage_dist,
            "stage_values": stage_values,
            "bottlenecks": bottlenecks,
            "avg_days_in_stage": round(avg_days, 1),
            "pipeline_health": health,
            "suggested_actions": actions,
            "reasoning": reasoning
        }

    def _build_reasoning(self, total, at_risk, bottlenecks, avg_days, health):
        parts = [f"Pipeline health is {health.upper()} with ₹{total:,.0f} total value."]
        if at_risk > 0:
            parts.append(f"₹{at_risk:,.0f} in revenue is currently at risk and requires immediate attention.")
        if bottlenecks:
            parts.append(f"{len(bottlenecks)} deal(s) are stalled beyond healthy limits, creating pipeline bottlenecks.")
        parts.append(f"Average stage duration is {avg_days:.1f} days across active deals.")
        return " ".join(parts)
