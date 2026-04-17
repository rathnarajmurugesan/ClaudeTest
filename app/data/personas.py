from typing import Optional
from app.models import PersonaCard

_PERSONA_CARDS: dict[str, PersonaCard] = {
    "CEO": PersonaCard(
        core_responsibilities=[
            "Set and communicate long-term organizational strategy",
            "Drive revenue growth and profitability targets",
            "Manage board, investor, and stakeholder relationships",
            "Lead M&A strategy, partnerships, and ecosystem development",
            "Build and retain the executive leadership team",
            "Champion organizational culture and enterprise-wide transformation",
        ],
        external_signals=[
            "Market disruption from digital-native and AI-first competitors",
            "ESG and sustainability pressure from investors and regulators",
            "Geopolitical volatility affecting global supply chains and operations",
            "Talent wars and rapidly evolving workforce expectations",
            "Regulatory and policy shifts across core markets",
        ],
        objections_concerns_risks=[
            "Unclear ROI and uncertain long-term business impact",
            "Risk of disrupting core operations during large-scale transformation",
            "Vendor lock-in, dependency, and partnership reliability concerns",
            "Change fatigue and organizational resistance to transformation",
            "Reputational and brand risk from high-profile initiative failures",
        ],
        value_gaps=[
            "Insufficient industry-specific benchmarking and peer comparison data",
            "Weak differentiation of offering from competing vendors",
            "No clear causal link between the initiative and growth or margin targets",
            "Limited executive peer reference examples and success stories",
            "Absence of a phased risk mitigation and value realization roadmap",
        ],
    ),
    "CFO": PersonaCard(
        core_responsibilities=[
            "Lead financial planning, analysis, and performance reporting",
            "Oversee capital allocation, investment decisions, and CAPEX/OPEX trade-offs",
            "Manage enterprise risk, compliance, and internal controls",
            "Direct treasury, cash flow management, and debt strategy",
            "Support M&A financial due diligence and post-merger integration",
            "Maintain investor relations and shape external financial communications",
        ],
        external_signals=[
            "Interest rate volatility and tightening credit market conditions",
            "FX exposure, hedging complexity, and cross-border currency risks",
            "Evolving accounting standards (IFRS 17, ASC 842) and reporting obligations",
            "Increased regulatory scrutiny around financial disclosures and ESG reporting",
            "Persistent inflation eroding margins and complicating cost modeling",
        ],
        objections_concerns_risks=[
            "Unproven ROI with no guaranteed or contractually committed financial outcomes",
            "Risk of budget overruns and cost escalation beyond approved thresholds",
            "Compliance, audit trail, and financial control gaps during transitions",
            "Cash flow and working capital impact during multi-year implementations",
            "Difficulty quantifying and attributing value of intangible or indirect benefits",
        ],
        value_gaps=[
            "Lack of robust financial modeling, TCO analysis, and sensitivity scenarios",
            "No clearly defined payback period, IRR, or NPV projections",
            "Insufficient detail on cost takeout opportunities and efficiency gains",
            "Missing benchmarks against industry-standard financial KPIs",
            "Weak narrative around finance function modernization and capability uplift",
        ],
    ),
    "CIO": PersonaCard(
        core_responsibilities=[
            "Define and execute the enterprise technology and digital strategy",
            "Manage IT infrastructure, enterprise architecture, and cybersecurity posture",
            "Drive digital transformation, AI adoption, and innovation programs",
            "Oversee vendor relationships, IT sourcing, and contract governance",
            "Ensure business continuity, disaster recovery, and operational resilience",
            "Align technology investments with enterprise business priorities and value",
        ],
        external_signals=[
            "Accelerating adoption of generative AI, cloud-native, and automation platforms",
            "Increasing frequency and sophistication of ransomware and nation-state cyber threats",
            "Legacy system debt creating modernization urgency and operational risk",
            "Critical skills shortage in emerging technology disciplines",
            "Data sovereignty, privacy regulations, and cross-border data transfer restrictions",
        ],
        objections_concerns_risks=[
            "Integration complexity with heterogeneous legacy systems and technical debt",
            "New security vulnerabilities and expanded attack surface from third-party solutions",
            "Risk of deepening technical debt through poorly managed implementations",
            "Concerns about vendor reliability, long-term product support, and roadmap",
            "Shadow IT proliferation and enterprise governance challenges",
        ],
        value_gaps=[
            "Unclear integration roadmap and compatibility with current IT landscape",
            "Insufficient cybersecurity architecture detail and threat model alignment",
            "No defined plan for knowledge transfer, skills building, and team enablement",
            "Missing metrics and KPIs for measuring IT performance improvement",
            "Weak articulation of scalability, resilience, and future-proofing strategy",
        ],
    ),
    "COO": PersonaCard(
        core_responsibilities=[
            "Optimize end-to-end operational efficiency and cost performance",
            "Manage supply chain, logistics, procurement, and vendor ecosystems",
            "Drive process standardization, automation, and continuous improvement",
            "Ensure quality management, regulatory compliance, and service delivery excellence",
            "Lead large-scale operational transformation and restructuring programs",
            "Maintain business continuity, operational resilience, and crisis readiness",
        ],
        external_signals=[
            "Supply chain disruptions from geopolitical tensions and climate events",
            "Labor market volatility and growing workforce automation pressure",
            "Customer demand volatility and rising expectations for service speed and quality",
            "Sustainability mandates and carbon reduction targets for operations",
            "Industry 4.0, smart factory, and intelligent operations trends",
        ],
        objections_concerns_risks=[
            "Operational disruption to core processes during implementation windows",
            "Underestimated complexity of change management at scale across sites and functions",
            "Over-dependence on third-party delivery partners for critical operations",
            "Risk of underestimating integration complexity and data migration effort",
            "Loss of operational visibility or control during transition periods",
        ],
        value_gaps=[
            "Insufficient evidence of operational KPI improvement from comparable implementations",
            "Unclear implementation sequencing, cutover plan, and go-live risk management",
            "Missing workforce impact assessment and reskilling/upskilling strategy",
            "Weak clarity on process ownership, governance, and accountability post-go-live",
            "No defined operational resilience benchmarks or continuity safeguards",
        ],
    ),
    "CMO": PersonaCard(
        core_responsibilities=[
            "Define brand strategy, market positioning, and competitive differentiation",
            "Drive customer acquisition, retention, lifetime value, and revenue growth",
            "Lead digital marketing, omnichannel execution, and campaign performance",
            "Manage marketing technology stack, data assets, and analytics capabilities",
            "Translate customer insights and market intelligence into product and service strategy",
            "Measure, report, and continuously optimize marketing ROI and attribution",
        ],
        external_signals=[
            "Rapidly shifting consumer behavior, preferences, and channel expectations",
            "First-party data imperative driven by cookie deprecation and privacy regulation",
            "Generative AI transforming personalization, content creation, and creative production",
            "Growing consumer demand for authentic, purpose-driven brand narratives",
            "Social commerce rise and continued fragmentation of digital channels",
        ],
        objections_concerns_risks=[
            "Risk of brand dilution, inconsistent messaging, or loss of brand control",
            "Unclear direct impact on customer acquisition costs and retention metrics",
            "Data privacy and consent compliance risk in personalization and targeting",
            "Potential cannibalization or disruption of existing marketing investments",
            "Attribution complexity and difficulty linking initiatives to revenue outcomes",
        ],
        value_gaps=[
            "Limited data on customer journey impact, lifecycle value, and churn reduction",
            "Weak narrative connecting the initiative to sustainable brand differentiation",
            "Insufficient customer segmentation depth and behavioral targeting specificity",
            "Missing martech integration plan and interoperability with existing stack",
            "No clear connection to customer lifetime value improvement or NPS uplift",
        ],
    ),
}


def get_persona_card(persona_id: str) -> Optional[PersonaCard]:
    return _PERSONA_CARDS.get(persona_id.upper())


def get_all_personas() -> dict[str, PersonaCard]:
    return _PERSONA_CARDS
