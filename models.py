
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import uuid





class Deal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
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
    risk_score: float = 0.0
    industry: str = ""
    notes: str = ""


class Prospect(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    company: str
    contact_name: str
    industry: str
    size: str = "Mid-Market"
    engagement_signals: List[str] = []
    email: str = ""
    linkedin: str = ""
    website_visits: int = 0
    content_downloads: int = 0


class Customer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    company: str
    contact_name: str
    usage_data: Dict[str, Any] = {}
    sentiment: str = "Neutral"
    mrr: float = 0.0
    contract_end_date: str = ""
    support_tickets: int = 0
    last_login_days_ago: int = 0
    feature_adoption: float = 50.0


class AuditLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    agent_name: str
    action: str
    entity_type: str
    entity_id: str
    input_summary: str
    output_summary: str
    details: Dict[str, Any] = {}





class DataStore:
    def __init__(self):
        self.deals: Dict[str, Deal] = {}
        self.prospects: Dict[str, Prospect] = {}
        self.customers: Dict[str, Customer] = {}
        self.audit_logs: List[AuditLog] = []
        self._seed_demo_data()

    def _seed_demo_data(self):
        now = datetime.now()

        deal_high = Deal(
            id="deal-001",
            client_name="Rajesh Sharma",
            company="TechNova Solutions",
            deal_value=1250000,
            stage="Negotiation",
            days_in_stage=18,
            last_contact_date=(now - timedelta(days=6)).strftime("%Y-%m-%d"),
            email_opened=False,
            reply_received=False,
            meeting_status="Cancelled",
            probability=30,
            risk_score=0,
            industry="SaaS",
            notes="Champion went silent after pricing discussion. CFO involved."
        )

        deal_medium = Deal(
            id="deal-002",
            client_name="Priya Patel",
            company="FinEdge Analytics",
            deal_value=875000,
            stage="Proposal",
            days_in_stage=12,
            last_contact_date=(now - timedelta(days=3)).strftime("%Y-%m-%d"),
            email_opened=True,
            reply_received=False,
            meeting_status="Scheduled",
            probability=55,
            risk_score=0,
            industry="FinTech",
            notes="Proposal sent, awaiting feedback. Multiple stakeholders involved."
        )

        deal_healthy = Deal(
            id="deal-003",
            client_name="Amit Kumar",
            company="GreenWave Energy",
            deal_value=2100000,
            stage="Qualification",
            days_in_stage=4,
            last_contact_date=(now - timedelta(days=1)).strftime("%Y-%m-%d"),
            email_opened=True,
            reply_received=True,
            meeting_status="Completed",
            probability=75,
            risk_score=0,
            industry="CleanTech",
            notes="Strong engagement. Technical evaluation completed. Budget approved."
        )

        for d in [deal_high, deal_medium, deal_healthy]:
            self.deals[d.id] = d

        prospects_data = [
            Prospect(
                id="pros-001",
                company="DataStream AI",
                contact_name="Vikram Mehta",
                industry="AI/ML",
                size="Enterprise",
                engagement_signals=["Visited pricing page 3x", "Downloaded whitepaper", "Attended webinar"],
                email="vikram@datastream.ai",
                website_visits=12,
                content_downloads=3
            ),
            Prospect(
                id="pros-002",
                company="CloudFirst India",
                contact_name="Sneha Reddy",
                industry="Cloud Infrastructure",
                size="Mid-Market",
                engagement_signals=["LinkedIn connection accepted", "Opened 2 emails"],
                email="sneha@cloudfirst.in",
                website_visits=4,
                content_downloads=1
            ),
            Prospect(
                id="pros-003",
                company="RetailMax",
                contact_name="Arjun Nair",
                industry="Retail Tech",
                size="SMB",
                engagement_signals=["Cold — no signals"],
                email="arjun@retailmax.co",
                website_visits=0,
                content_downloads=0
            ),
        ]
        for p in prospects_data:
            self.prospects[p.id] = p

        customer_churn = Customer(
            id="cust-001",
            company="MediCore Health",
            contact_name="Dr. Kavita Singh",
            usage_data={
                "logins_last_30d": 3,
                "features_used": 2,
                "total_features": 12,
                "api_calls_trend": "declining",
                "last_support_ticket": "Unresolved - 10 days"
            },
            sentiment="Negative",
            mrr=45000,
            contract_end_date=(now + timedelta(days=45)).strftime("%Y-%m-%d"),
            support_tickets=5,
            last_login_days_ago=12,
            feature_adoption=16.7
        )

        customer_healthy = Customer(
            id="cust-002",
            company="EduPrime Learning",
            contact_name="Rohit Verma",
            usage_data={
                "logins_last_30d": 28,
                "features_used": 10,
                "total_features": 12,
                "api_calls_trend": "growing",
                "last_support_ticket": "Resolved - 2 days"
            },
            sentiment="Positive",
            mrr=120000,
            contract_end_date=(now + timedelta(days=200)).strftime("%Y-%m-%d"),
            support_tickets=1,
            last_login_days_ago=1,
            feature_adoption=83.3
        )

        for c in [customer_churn, customer_healthy]:
            self.customers[c.id] = c

    def add_audit_log(self, agent_name: str, action: str, entity_type: str,
                      entity_id: str, input_summary: str, output_summary: str,
                      details: Dict[str, Any] = {}):
        log = AuditLog(
            agent_name=agent_name,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            input_summary=input_summary,
            output_summary=output_summary,
            details=details
        )
        self.audit_logs.append(log)
        return log

store = DataStore()
