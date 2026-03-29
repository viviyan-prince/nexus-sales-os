
from agents.signal_agent import SignalAgent
from agents.deal_agent import DealAgent
from agents.strategy_agent import StrategyAgent
from agents.outreach_agent import OutreachAgent
from agents.revenue_impact_agent import RevenueImpactAgent
from agents.competitive_agent import CompetitiveAgent


class OrchestratorAgent:
    name = "Orchestrator Agent"

    def __init__(self):
        self.signal_agent = SignalAgent()
        self.deal_agent = DealAgent()
        self.strategy_agent = StrategyAgent()
        self.outreach_agent = OutreachAgent()
        self.revenue_impact_agent = RevenueImpactAgent()
        self.competitive_agent = CompetitiveAgent()

    def analyze_deal(self, deal: dict) -> dict:
        pipeline_log = []


        pipeline_log.append({"step": 1, "agent": "Signal Agent", "status": "running"})
        signal_result = self.signal_agent.analyze(deal)
        pipeline_log[-1]["status"] = "complete"


        pipeline_log.append({"step": 2, "agent": "Deal Intelligence Agent", "status": "running"})
        deal_result = self.deal_agent.analyze(deal, signal_result)
        pipeline_log[-1]["status"] = "complete"


        pipeline_log.append({"step": 3, "agent": "Strategy Agent", "status": "running"})
        strategy_result = self.strategy_agent.analyze(
            deal, deal_result["risk_score"], signal_result["engagement_level"], signal_result
        )
        pipeline_log[-1]["status"] = "complete"


        pipeline_log.append({"step": 4, "agent": "Outreach Agent", "status": "running"})
        outreach_result = self.outreach_agent.generate(deal, strategy_result, deal_result)
        pipeline_log[-1]["status"] = "complete"


        pipeline_log.append({"step": 5, "agent": "Revenue Impact Agent", "status": "running"})
        revenue_result = self.revenue_impact_agent.analyze(deal, deal_result, strategy_result)
        pipeline_log[-1]["status"] = "complete"


        pipeline_log.append({"step": 6, "agent": "Competitive Intelligence Agent", "status": "running"})
        competitive_result = self.competitive_agent.analyze(deal)
        pipeline_log[-1]["status"] = "complete"

        return {
            "agent": self.name,
            "deal_id": deal.get("id"),
            "deal_summary": {
                "client": deal.get("client_name"),
                "company": deal.get("company"),
                "deal_value": deal.get("deal_value"),
                "stage": deal.get("stage")
            },
            "agents_executed": 6,
            "pipeline_log": pipeline_log,
            "signal_analysis": signal_result,
            "deal_intelligence": deal_result,
            "strategy": strategy_result,
            "outreach": outreach_result,
            "revenue_impact": revenue_result,
            "competitive_intelligence": competitive_result,
            "executive_summary": self._build_executive_summary(
                deal, deal_result, strategy_result, revenue_result
            )
        }

    def _build_executive_summary(self, deal, deal_result, strategy_result, revenue_result):
        risk_score = deal_result["risk_score"]
        risk_level = deal_result["risk_level"]
        revenue_recovered = revenue_result["revenue_recovered"]
        strategy_name = strategy_result["primary_strategy"]
        urgency = strategy_result["urgency"]

        parts = [
            f"🎯 EXECUTIVE SUMMARY — {deal.get('company')}",
            f"",
            f"Deal Value: ₹{deal.get('deal_value', 0):,.0f} | Stage: {deal.get('stage')}",
            f"Risk Score: {risk_score}/100 ({risk_level}) | Health Score: {100 - risk_score}/100",
            f"",
            f"Strategy: {strategy_name} (Urgency: {urgency.upper()})",
            f"",
            f"📊 Revenue Impact:",
            f"  Before AI: ₹{revenue_result['expected_revenue_before']:,.0f}",
            f"  After AI:  ₹{revenue_result['expected_revenue_after']:,.0f}",
            f"  💰 Revenue Saved: {revenue_result['revenue_saved_display']}",
            f"",
            f"The AI system executed 6 specialized agents to analyze this deal,",
            f"identified {len(deal_result['risk_factors'])} risk factor(s), and generated",
            f"a comprehensive recovery strategy with multi-channel outreach."
        ]
        return "\n".join(parts)
