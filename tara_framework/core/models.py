"""
Core data models for the TARA framework.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
import uuid
from datetime import datetime


class AssetType(Enum):
    """Types of assets in automotive systems."""
    PHYSICAL = "physical"
    SOFTWARE = "software"
    DATA = "data"
    FUNCTION = "function"


class ThreatType(Enum):
    """Types of threats."""
    MALWARE = "malware"
    SOCIAL_ENGINEERING = "social_engineering"
    PHYSICAL_ACCESS = "physical_access"
    SUPPLY_CHAIN = "supply_chain"
    INSIDER_THREAT = "insider_threat"
    REMOTE_EXPLOITATION = "remote_exploitation"


class RiskLevel(Enum):
    """Risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NodeType(Enum):
    """Types of attack tree nodes."""
    ROOT = "root"
    INTERMEDIATE = "intermediate"
    LEAF = "leaf"


class DifficultyLevel(Enum):
    """Difficulty levels for attack steps."""
    TRIVIAL = "trivial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


@dataclass
class Asset:
    """Represents an asset in the automotive system."""
    name: str
    asset_type: AssetType
    description: str
    location: str
    value: float
    dependencies: List[str] = field(default_factory=list)
    security_controls: List[str] = field(default_factory=list)
    vulnerabilities: List[str] = field(default_factory=list)
    impact_safety: float = 0.0
    impact_financial: float = 0.0
    impact_operational: float = 0.0
    impact_privacy: float = 0.0
    asset_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    def get_total_impact(self) -> float:
        """Calculate total impact score."""
        return (self.impact_safety + self.impact_financial + 
                self.impact_operational + self.impact_privacy)


@dataclass
class AssetValue:
    """Comprehensive asset valuation."""
    asset: Asset
    safety_score: float
    financial_score: float
    operational_score: float
    privacy_score: float
    total_score: float
    valuation_method: str
    justification: str
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if self.total_score == 0:
            self.total_score = (self.safety_score + self.financial_score + 
                              self.operational_score + self.privacy_score)


@dataclass
class Threat:
    """Represents a threat to the system."""
    name: str
    threat_type: ThreatType
    description: str
    likelihood: float  # 0.0 to 1.0
    impact: float  # 1.0 to 10.0
    attack_vectors: List[str] = field(default_factory=list)
    affected_assets: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)
    threat_actors: List[str] = field(default_factory=list)
    threat_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Vulnerability:
    """Represents a vulnerability in the system."""
    name: str
    description: str
    severity: str  # low, medium, high, critical
    exploitability: str  # low, medium, high
    cvss_score: Optional[float] = None
    cve_id: Optional[str] = None
    affected_assets: List[str] = field(default_factory=list)
    remediation: Optional[str] = None
    vulnerability_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class RiskAssessment:
    """Risk assessment result."""
    threat: Threat
    vulnerability: Vulnerability
    asset: Asset
    risk_level: RiskLevel
    risk_score: float
    likelihood: float
    impact: float
    justification: str
    risk_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AttackNode:
    """Represents a node in an attack tree."""
    name: str
    node_type: NodeType
    description: str
    prerequisites: List[str] = field(default_factory=list)
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    cost: float = 0.0
    time_required: str = "unknown"
    tools_needed: List[str] = field(default_factory=list)
    success_probability: float = 0.5
    detection_probability: float = 0.3
    children: List['AttackNode'] = field(default_factory=list)
    parent: Optional['AttackNode'] = None
    countermeasures: List[str] = field(default_factory=list)
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_child(self, child: 'AttackNode'):
        """Add a child node."""
        child.parent = self
        self.children.append(child)
    
    def is_leaf(self) -> bool:
        """Check if this is a leaf node."""
        return len(self.children) == 0
    
    def is_root(self) -> bool:
        """Check if this is a root node."""
        return self.parent is None


@dataclass
class AttackPath:
    """Represents a complete attack path through an attack tree."""
    nodes: List[AttackNode]
    total_cost: float
    total_time: str
    success_probability: float
    detection_probability: float
    feasibility_score: float
    path_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if self.total_cost == 0:
            self.total_cost = sum(node.cost for node in self.nodes)
        
        if self.success_probability == 0:
            # Calculate combined success probability
            prob = 1.0
            for node in self.nodes:
                prob *= node.success_probability
            self.success_probability = prob


@dataclass
class AttackTree:
    """Represents an attack tree."""
    root_node: AttackNode
    target_asset: Asset
    threat_scenario: str
    description: str
    attack_paths: List[AttackPath] = field(default_factory=list)
    tree_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def all_nodes(self) -> List[AttackNode]:
        """Get all nodes in the tree."""
        nodes = []
        self._collect_nodes(self.root_node, nodes)
        return nodes
    
    @property
    def leaf_nodes(self) -> List[AttackNode]:
        """Get all leaf nodes in the tree."""
        return [node for node in self.all_nodes if node.is_leaf()]
    
    def _collect_nodes(self, node: AttackNode, nodes: List[AttackNode]):
        """Recursively collect all nodes."""
        nodes.append(node)
        for child in node.children:
            self._collect_nodes(child, nodes)
    
    def find_node(self, name: str) -> Optional[AttackNode]:
        """Find a node by name."""
        for node in self.all_nodes:
            if node.name == name:
                return node
        return None
    
    def generate_attack_paths(self):
        """Generate all possible attack paths."""
        self.attack_paths = []
        self._generate_paths_from_node(self.root_node, [])
    
    def _generate_paths_from_node(self, node: AttackNode, current_path: List[AttackNode]):
        """Recursively generate attack paths."""
        current_path.append(node)
        
        if node.is_leaf():
            # Create attack path
            path = AttackPath(
                nodes=current_path.copy(),
                total_cost=sum(n.cost for n in current_path),
                total_time="calculated",
                success_probability=1.0,
                detection_probability=1.0,
                feasibility_score=0.5
            )
            self.attack_paths.append(path)
        else:
            for child in node.children:
                self._generate_paths_from_node(child, current_path)
        
        current_path.pop()


@dataclass
class AttackerProfile:
    """Profile of a potential attacker."""
    name: str
    skill_level: str  # low, medium, high
    resources: str  # limited, moderate, extensive
    motivation: str
    risk_tolerance: str  # low, medium, high
    time_horizon: str  # short, medium, long
    capabilities: List[str] = field(default_factory=list)
    budget: float = 0.0
    team_size: int = 1
    attack_preferences: List[str] = field(default_factory=list)
    profile_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DefenderProfile:
    """Profile of the defender (organization)."""
    name: str
    budget: float
    expertise_level: str  # low, medium, high
    response_time: str  # slow, medium, fast
    risk_tolerance: str  # low, medium, high
    available_countermeasures: List[str] = field(default_factory=list)
    compliance_requirements: List[str] = field(default_factory=list)
    organizational_capabilities: List[str] = field(default_factory=list)
    profile_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PayoffMatrix:
    """Payoff matrix for game theory analysis."""
    attacker_strategies: List[str]
    defender_strategies: List[str]
    payoffs: Dict[tuple, Dict[str, float]]  # (attacker_strategy, defender_strategy) -> {attacker_payoff, defender_payoff}
    matrix_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    def get_payoff(self, attacker_strategy: str, defender_strategy: str) -> Dict[str, float]:
        """Get payoffs for a strategy combination."""
        key = (attacker_strategy, defender_strategy)
        return self.payoffs.get(key, {"attacker_payoff": 0.0, "defender_payoff": 0.0})


@dataclass
class GameModel:
    """Game theory model for strategic analysis."""
    attack_tree: AttackTree
    attacker: AttackerProfile
    defender: DefenderProfile
    game_type: str  # simultaneous, sequential, repeated
    information_set: str  # complete, incomplete
    equilibrium_concept: str  # nash, subgame_perfect, etc.
    payoff_matrix: Optional[PayoffMatrix] = None
    equilibrium: Optional[Dict[str, Any]] = None
    sensitivity_analysis: Optional[Dict[str, Any]] = None
    model_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class EquilibriumResult:
    """Result of equilibrium analysis."""
    equilibrium_type: str
    attacker_strategy: str
    defender_strategy: str
    attacker_payoff: float
    defender_payoff: float
    stability: float
    expected_outcome: str
    attack_success_probability: float
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Recommendation:
    """Security recommendation."""
    title: str
    description: str
    priority: str  # low, medium, high, critical
    category: str
    estimated_cost: float
    effectiveness_score: float
    implementation_time: str
    associated_risks: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    countermeasures: List[str] = field(default_factory=list)
    recommendation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AnalysisResult:
    """Comprehensive analysis result."""
    asset_inventory: List[Asset]
    threat_assessment: List[Threat]
    risk_assessment: List[RiskAssessment]
    attack_trees: List[AttackTree]
    game_theory_results: List[EquilibriumResult]
    recommendations: List[Recommendation]
    analysis_metadata: Dict[str, Any] = field(default_factory=dict)
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def critical_vulnerabilities(self) -> List[Vulnerability]:
        """Get critical vulnerabilities from the analysis."""
        vulnerabilities = []
        for risk in self.risk_assessment:
            if risk.risk_level == RiskLevel.CRITICAL:
                vulnerabilities.append(risk.vulnerability)
        return vulnerabilities
    
    @property
    def high_risk_paths(self) -> List[AttackPath]:
        """Get high-risk attack paths."""
        high_risk_paths = []
        for tree in self.attack_trees:
            for path in tree.attack_paths:
                if path.feasibility_score > 0.7:  # High feasibility threshold
                    high_risk_paths.append(path)
        return high_risk_paths


@dataclass
class ExecutiveSummary:
    """Executive summary of analysis results."""
    key_findings: List[str]
    risk_overview: str
    recommendations: List[str]
    investment_priorities: List[str]
    critical_risks: List[str]
    summary_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)