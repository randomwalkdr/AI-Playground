class RiskAssessmentResult:
    def __init__(self, risks=None):
        self.risks = risks or []

class AnalysisResult:
    def __init__(self):
        self.asset_inventory = []
        self.threat_assessment = []
        self.risk_assessment = RiskAssessmentResult()
        self.attack_trees = []
        self.game_theory_results = []
        self.critical_vulnerabilities = []
        self.high_risk_paths = []
        self.recommendations = []

class Recommendation:
    def __init__(self, title, priority="high", estimated_cost=10000, effectiveness_score=0.8):
        self.title = title
        self.priority = priority
        self.category = "technical"
        self.estimated_cost = estimated_cost
        self.effectiveness_score = effectiveness_score
        self.implementation_time = "1_month"
        self.description = "Implement security controls"
        self.associated_risks = []
        self.prerequisites = []

class ExecutiveSummary:
    def __init__(self):
        self.key_findings = ["High risk found"]
        self.risk_overview = "Overall risk is high"
        self.recommendations = ["Implement controls"]
        self.investment_priorities = ["Network security"]
