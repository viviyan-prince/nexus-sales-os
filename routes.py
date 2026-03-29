
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from models import store, Deal, Prospect, Customer
from agents.signal_agent import SignalAgent
from agents.pipeline_agent import PipelineAgent
from agents.deal_agent import DealAgent
from agents.prospecting_agent import ProspectingAgent
from agents.strategy_agent import StrategyAgent
from agents.outreach_agent import OutreachAgent
from agents.retention_agent import RetentionAgent
from agents.competitive_agent import CompetitiveAgent
from agents.revenue_impact_agent import RevenueImpactAgent
from agents.orchestrator_agent import OrchestratorAgent


router = APIRouter(prefix="/api")


signal_agent = SignalAgent()
pipeline_agent = PipelineAgent()
deal_agent = DealAgent()
prospecting_agent = ProspectingAgent()
strategy_agent = StrategyAgent()
outreach_agent = OutreachAgent()
retention_agent = RetentionAgent()
competitive_agent = CompetitiveAgent()
revenue_impact_agent = RevenueImpactAgent()
orchestrator = OrchestratorAgent()





class DealCreate(BaseModel):
    client_name: str
    company: str
    deal_value: float
    stage: str = "Prospecting"
    days_in_stage: int = 0
    last_contact_date: str = ""
    email_opened: bool = False
    reply_received: bool = False
    meeting_status: str = "None"
    probability: float = 50.0
    industry: str = ""
    notes: str = ""

class AnalyzeRequest(BaseModel):
    deal_id: str

class ProspectAnalyzeRequest(BaseModel):
    prospect_id: str

class RetentionRequest(BaseModel):
    customer_id: str

class CompetitiveRequest(BaseModel):
    deal_id: str

class OutreachRequest(BaseModel):
    deal_id: str





@router.post("/deal")
def create_deal(data: DealCreate):
    deal = Deal(**data.model_dump())
    store.deals[deal.id] = deal
    store.add_audit_log("System", "Deal Created", "deal", deal.id,
                        f"New deal: {deal.company}", f"Deal {deal.id} created with value ₹{deal.deal_value:,.0f}")
    return {"status": "created", "deal": deal.model_dump()}


@router.get("/deals")
def list_deals():
    deals = [d.model_dump() for d in store.deals.values()]
    return {"deals": deals, "total": len(deals)}


@router.get("/deal/{deal_id}")
def get_deal(deal_id: str):
    deal = store.deals.get(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal.model_dump()





@router.post("/analyze-deal")
def analyze_deal(req: AnalyzeRequest):
    deal = store.deals.get(req.deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    deal_dict = deal.model_dump()
    result = orchestrator.analyze_deal(deal_dict)


    deal.risk_score = result["deal_intelligence"]["risk_score"]
    store.deals[deal.id] = deal


    store.add_audit_log("Orchestrator Agent", "Full Deal Analysis", "deal", deal.id,
                        f"Analyzed {deal.company} — 6 agents executed",
                        f"Risk: {result['deal_intelligence']['risk_score']}/100 | Revenue Saved: {result['revenue_impact']['revenue_saved_display']}",
                        {"risk_score": result["deal_intelligence"]["risk_score"],
                         "revenue_recovered": result["revenue_impact"]["revenue_recovered"]})

    return result


@router.post("/pipeline-analysis")
def pipeline_analysis():
    deals = [d.model_dump() for d in store.deals.values()]
    result = pipeline_agent.analyze(deals)

    store.add_audit_log("Pipeline Intelligence Agent", "Pipeline Analysis", "pipeline", "all",
                        f"Analyzed {len(deals)} deals",
                        f"Pipeline: ₹{result['total_pipeline_value']:,.0f} | At Risk: ₹{result['revenue_at_risk']:,.0f}")

    return result


@router.post("/generate-outreach")
def generate_outreach(req: OutreachRequest):
    deal = store.deals.get(req.deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    deal_dict = deal.model_dump()
    signal_result = signal_agent.analyze(deal_dict)
    deal_result = deal_agent.analyze(deal_dict, signal_result)
    strategy_result = strategy_agent.analyze(
        deal_dict, deal_result["risk_score"], signal_result["engagement_level"]
    )
    outreach_result = outreach_agent.generate(deal_dict, strategy_result, deal_result)

    store.add_audit_log("Outreach Agent", "Outreach Generated", "deal", deal.id,
                        f"Generated outreach for {deal.company}",
                        "Email + WhatsApp + LinkedIn messages generated")

    return outreach_result





@router.get("/prospects")
def list_prospects():
    prospects = [p.model_dump() for p in store.prospects.values()]
    return {"prospects": prospects, "total": len(prospects)}


@router.post("/analyze-prospect")
def analyze_prospect(req: ProspectAnalyzeRequest):
    prospect = store.prospects.get(req.prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")

    result = prospecting_agent.analyze(prospect.model_dump())

    store.add_audit_log("Prospecting Agent", "Prospect Analysis", "prospect", prospect.id,
                        f"Analyzed {prospect.company}",
                        f"ICP: {result['icp_score']}/100 | Level: {result['engagement_level']}")

    return result





@router.get("/customers")
def list_customers():
    customers = [c.model_dump() for c in store.customers.values()]
    return {"customers": customers, "total": len(customers)}


@router.post("/retention-analysis")
def retention_analysis(req: RetentionRequest):
    customer = store.customers.get(req.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    result = retention_agent.analyze(customer.model_dump())

    store.add_audit_log("Revenue Retention Agent", "Retention Analysis", "customer", customer.id,
                        f"Analyzed {customer.company}",
                        f"Churn Risk: {result['churn_probability']}% | MRR at Risk: ₹{result['mrr_at_risk']:,.0f}")

    return result





@router.post("/competitive-analysis")
def competitive_analysis(req: CompetitiveRequest):
    deal = store.deals.get(req.deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    result = competitive_agent.analyze(deal.model_dump())

    store.add_audit_log("Competitive Intelligence Agent", "Competitive Analysis", "deal", deal.id,
                        f"Analyzed {deal.company} in {deal.industry}",
                        f"Generated {len(result['battlecards'])} battlecards")

    return result





@router.get("/dashboard-summary")
def dashboard_summary():
    deals = list(store.deals.values())
    active_deals = [d for d in deals if d.stage not in ("Closed Won", "Closed Lost")]

    total_pipeline = sum(d.deal_value for d in active_deals)
    weighted_pipeline = sum(d.deal_value * (d.probability / 100) for d in active_deals)


    at_risk = []
    for d in active_deals:
        deal_dict = d.model_dump()
        signal = signal_agent.analyze(deal_dict)
        di = deal_agent.analyze(deal_dict, signal)
        d.risk_score = di["risk_score"]
        store.deals[d.id] = d
        if di["risk_score"] >= 40:
            at_risk.append({
                "id": d.id,
                "company": d.company,
                "client_name": d.client_name,
                "deal_value": d.deal_value,
                "risk_score": di["risk_score"],
                "risk_level": di["risk_level"],
                "stage": d.stage
            })

    revenue_at_risk = sum(d["deal_value"] for d in at_risk)


    stage_dist = {}
    stage_values = {}
    for stage in ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]:
        stage_deals = [d for d in deals if d.stage == stage]
        stage_dist[stage] = len(stage_deals)
        stage_values[stage] = sum(d.deal_value for d in stage_deals)

    return {
        "total_pipeline_value": total_pipeline,
        "weighted_pipeline_value": round(weighted_pipeline, 2),
        "total_deals": len(deals),
        "active_deals": len(active_deals),
        "at_risk_deals": at_risk,
        "at_risk_count": len(at_risk),
        "revenue_at_risk": revenue_at_risk,
        "stage_distribution": stage_dist,
        "stage_values": stage_values,
        "customers_count": len(store.customers),
        "prospects_count": len(store.prospects)
    }


@router.get("/audit-logs")
def get_audit_logs():
    logs = [log.model_dump() for log in reversed(store.audit_logs[-50:])]
    return {"logs": logs, "total": len(store.audit_logs)}
