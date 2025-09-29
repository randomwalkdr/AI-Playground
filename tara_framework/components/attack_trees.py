"""
Attack Trees component implementation.
"""

from typing import List, Dict, Any, Optional, Tuple
import uuid
from datetime import datetime

from ..core.models import (
    Asset, Threat, AttackNode, AttackTree, AttackPath, NodeType, DifficultyLevel
)
from ..core.exceptions import AttackTreeConstructionError
from ..core.validators import AttackTreeValidator


class AttackTreesComponent:
    """Attack Trees component for detailed attack path modeling."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Attack Trees component with configuration."""
        self.config = config or {}
        self.max_tree_depth = self.config.get("max_tree_depth", 10)
        self.node_validation = self.config.get("node_validation", True)
        self.path_analysis_method = self.config.get("path_analysis_method", "feasibility_based")
        
        # Default attack patterns for automotive systems
        self.attack_patterns = {
            "remote_exploitation": [
                "network_reconnaissance",
                "vulnerability_scanning", 
                "exploit_development",
                "payload_deployment",
                "persistence_establishment"
            ],
            "physical_access": [
                "physical_proximity",
                "hardware_access",
                "firmware_modification",
                "data_extraction",
                "system_compromise"
            ],
            "supply_chain": [
                "component_compromise",
                "firmware_backdoor",
                "hardware_trojan",
                "malicious_update",
                "system_integration"
            ],
            "social_engineering": [
                "target_identification",
                "credential_harvesting",
                "phishing_attack",
                "insider_recruitment",
                "privilege_escalation"
            ]
        }
        
        # Default node templates
        self.node_templates = {
            "reconnaissance": {
                "difficulty": DifficultyLevel.EASY,
                "cost": 1000,
                "time_required": "1-2 weeks",
                "tools_needed": ["network_scanner", "vulnerability_scanner"],
                "success_probability": 0.8,
                "detection_probability": 0.2
            },
            "exploitation": {
                "difficulty": DifficultyLevel.MEDIUM,
                "cost": 5000,
                "time_required": "1-4 weeks",
                "tools_needed": ["exploit_framework", "custom_tools"],
                "success_probability": 0.6,
                "detection_probability": 0.4
            },
            "persistence": {
                "difficulty": DifficultyLevel.HARD,
                "cost": 10000,
                "time_required": "2-8 weeks",
                "tools_needed": ["rootkit", "backdoor"],
                "success_probability": 0.4,
                "detection_probability": 0.6
            }
        }
    
    def construct_attack_tree(self, target_asset: Asset, threat_scenario: Dict[str, Any]) -> AttackTree:
        """
        Construct an attack tree for a specific target asset and threat scenario.
        
        Args:
            target_asset: Target asset for the attack
            threat_scenario: Specific threat scenario to model
            
        Returns:
            Structured attack tree with nodes and paths
        """
        try:
            goal = threat_scenario.get("goal", f"compromise_{target_asset.name.lower()}")
            attacker_profile = threat_scenario.get("attacker_profile", "skilled_insider")
            attack_vector = threat_scenario.get("attack_vector", "remote_exploitation")
            
            # Create root node
            root_node = AttackNode(
                name=goal,
                node_type=NodeType.ROOT,
                description=f"Ultimate goal: {goal}",
                difficulty=DifficultyLevel.EXPERT,
                cost=0,
                success_probability=1.0,
                detection_probability=0.0
            )
            
            # Build tree structure based on attack vector
            if attack_vector in self.attack_patterns:
                self._build_tree_from_pattern(root_node, attack_vector, attacker_profile)
            else:
                self._build_generic_tree(root_node, attacker_profile)
            
            # Create attack tree
            tree = AttackTree(
                root_node=root_node,
                target_asset=target_asset,
                threat_scenario=goal,
                description=f"Attack tree for {goal} targeting {target_asset.name}"
            )
            
            # Generate attack paths
            tree.generate_attack_paths()
            
            # Validate tree if enabled
            if self.node_validation:
                errors = AttackTreeValidator.validate_attack_tree(tree)
                if errors:
                    raise AttackTreeConstructionError(
                        f"Attack tree validation failed: {', '.join(errors)}",
                        invalid_nodes=errors
                    )
            
            return tree
            
        except Exception as e:
            if isinstance(e, AttackTreeConstructionError):
                raise
            raise AttackTreeConstructionError(f"Attack tree construction failed: {str(e)}")
    
    def _build_tree_from_pattern(self, root_node: AttackNode, attack_vector: str, attacker_profile: str):
        """Build attack tree from predefined attack pattern."""
        pattern_steps = self.attack_patterns[attack_vector]
        
        for i, step in enumerate(pattern_steps):
            # Create intermediate node
            intermediate_node = AttackNode(
                name=step,
                node_type=NodeType.INTERMEDIATE,
                description=f"Step {i+1}: {step.replace('_', ' ').title()}",
                difficulty=DifficultyLevel.MEDIUM,
                cost=2000,
                success_probability=0.7,
                detection_probability=0.3
            )
            
            # Add leaf nodes for this step
            self._add_leaf_nodes_for_step(intermediate_node, step, attacker_profile)
            
            # Connect to root
            root_node.add_child(intermediate_node)
    
    def _build_generic_tree(self, root_node: AttackNode, attacker_profile: str):
        """Build generic attack tree structure."""
        # Create main attack phases
        phases = [
            "reconnaissance",
            "initial_access", 
            "lateral_movement",
            "persistence",
            "objective_achievement"
        ]
        
        for phase in phases:
            phase_node = AttackNode(
                name=phase,
                node_type=NodeType.INTERMEDIATE,
                description=f"Phase: {phase.replace('_', ' ').title()}",
                difficulty=DifficultyLevel.MEDIUM,
                cost=3000,
                success_probability=0.6,
                detection_probability=0.4
            )
            
            # Add specific attack methods for this phase
            self._add_attack_methods(phase_node, phase, attacker_profile)
            
            # Connect to root
            root_node.add_child(phase_node)
    
    def _add_leaf_nodes_for_step(self, parent_node: AttackNode, step: str, attacker_profile: str):
        """Add leaf nodes for a specific attack step."""
        # Get template for this step type
        template = self.node_templates.get(step, self.node_templates["exploitation"])
        
        # Create specific attack methods
        if step == "network_reconnaissance":
            methods = ["port_scanning", "service_enumeration", "vulnerability_scanning"]
        elif step == "exploit_development":
            methods = ["known_exploit_use", "custom_exploit_development", "zero_day_exploitation"]
        elif step == "physical_access":
            methods = ["direct_hardware_access", "usb_attack", "wireless_attack"]
        else:
            methods = [f"{step}_method_1", f"{step}_method_2", f"{step}_method_3"]
        
        for method in methods:
            leaf_node = AttackNode(
                name=method,
                node_type=NodeType.LEAF,
                description=f"Specific method: {method.replace('_', ' ').title()}",
                difficulty=template["difficulty"],
                cost=template["cost"],
                time_required=template["time_required"],
                tools_needed=template["tools_needed"],
                success_probability=template["success_probability"],
                detection_probability=template["detection_probability"]
            )
            
            parent_node.add_child(leaf_node)
    
    def _add_attack_methods(self, parent_node: AttackNode, phase: str, attacker_profile: str):
        """Add specific attack methods for a phase."""
        method_templates = {
            "reconnaissance": {
                "difficulty": DifficultyLevel.EASY,
                "cost": 500,
                "success_probability": 0.9,
                "detection_probability": 0.1
            },
            "initial_access": {
                "difficulty": DifficultyLevel.MEDIUM,
                "cost": 2000,
                "success_probability": 0.7,
                "detection_probability": 0.3
            },
            "lateral_movement": {
                "difficulty": DifficultyLevel.HARD,
                "cost": 5000,
                "success_probability": 0.5,
                "detection_probability": 0.5
            },
            "persistence": {
                "difficulty": DifficultyLevel.EXPERT,
                "cost": 10000,
                "success_probability": 0.3,
                "detection_probability": 0.7
            },
            "objective_achievement": {
                "difficulty": DifficultyLevel.MEDIUM,
                "cost": 3000,
                "success_probability": 0.8,
                "detection_probability": 0.2
            }
        }
        
        template = method_templates.get(phase, method_templates["initial_access"])
        
        # Create 2-3 specific methods for each phase
        methods = [
            f"{phase}_method_1",
            f"{phase}_method_2", 
            f"{phase}_method_3"
        ]
        
        for method in methods:
            leaf_node = AttackNode(
                name=method,
                node_type=NodeType.LEAF,
                description=f"Specific {phase} method: {method}",
                difficulty=template["difficulty"],
                cost=template["cost"],
                success_probability=template["success_probability"],
                detection_probability=template["detection_probability"]
            )
            
            parent_node.add_child(leaf_node)
    
    def add_attack_node(self, tree: AttackTree, parent_node: AttackNode, 
                       node_data: Dict[str, Any]) -> AttackNode:
        """
        Add a new attack node to an existing attack tree.
        
        Args:
            tree: Target attack tree
            parent_node: Parent node for the new node
            node_data: Node information
            
        Returns:
            Newly created attack node
        """
        try:
            # Create new node
            new_node = AttackNode(
                name=node_data["name"],
                node_type=NodeType(node_data.get("type", "leaf")),
                description=node_data.get("description", ""),
                prerequisites=node_data.get("prerequisites", []),
                difficulty=DifficultyLevel(node_data.get("difficulty", "medium")),
                cost=node_data.get("cost", 0),
                time_required=node_data.get("time_required", "unknown"),
                tools_needed=node_data.get("tools_needed", []),
                success_probability=node_data.get("success_probability", 0.5),
                detection_probability=node_data.get("detection_probability", 0.3)
            )
            
            # Add to parent
            parent_node.add_child(new_node)
            
            # Regenerate attack paths
            tree.generate_attack_paths()
            
            return new_node
            
        except Exception as e:
            raise AttackTreeConstructionError(f"Failed to add attack node: {str(e)}")
    
    def analyze_attack_paths(self, tree: AttackTree, analysis_type: str) -> Dict[str, Any]:
        """
        Analyze all possible attack paths in the tree.
        
        Args:
            tree: Attack tree to analyze
            analysis_type: Type of analysis ("feasibility", "cost", "probability")
            
        Returns:
            Analysis results for all attack paths
        """
        if analysis_type == "feasibility":
            return self._analyze_path_feasibility(tree)
        elif analysis_type == "cost":
            return self._analyze_path_costs(tree)
        elif analysis_type == "probability":
            return self._analyze_path_probabilities(tree)
        else:
            return self._analyze_path_comprehensive(tree)
    
    def _analyze_path_feasibility(self, tree: AttackTree) -> Dict[str, Any]:
        """Analyze attack path feasibility."""
        feasible_paths = []
        
        for path in tree.attack_paths:
            # Calculate feasibility score based on multiple factors
            feasibility_score = self._calculate_feasibility_score(path)
            path.feasibility_score = feasibility_score
            
            feasible_paths.append({
                "path_id": path.path_id,
                "feasibility_score": feasibility_score,
                "total_cost": path.total_cost,
                "success_probability": path.success_probability,
                "detection_probability": path.detection_probability,
                "nodes": [node.name for node in path.nodes]
            })
        
        # Sort by feasibility score
        feasible_paths.sort(key=lambda x: x["feasibility_score"], reverse=True)
        
        return {
            "analysis_type": "feasibility",
            "total_paths": len(feasible_paths),
            "feasible_paths": feasible_paths,
            "most_feasible": feasible_paths[0] if feasible_paths else None
        }
    
    def _calculate_feasibility_score(self, path: AttackPath) -> float:
        """Calculate feasibility score for an attack path."""
        # Factors affecting feasibility
        cost_factor = max(0, 1 - (path.total_cost / 50000))  # Normalize cost
        success_factor = path.success_probability
        detection_factor = 1 - path.detection_probability  # Lower detection = higher feasibility
        
        # Weighted combination
        feasibility = (cost_factor * 0.3 + success_factor * 0.5 + detection_factor * 0.2)
        
        return min(feasibility, 1.0)
    
    def _analyze_path_costs(self, tree: AttackTree) -> Dict[str, Any]:
        """Analyze attack path costs."""
        cost_analysis = []
        
        for path in tree.attack_paths:
            cost_analysis.append({
                "path_id": path.path_id,
                "total_cost": path.total_cost,
                "node_costs": [{"node": node.name, "cost": node.cost} for node in path.nodes],
                "cost_per_node": path.total_cost / len(path.nodes) if path.nodes else 0
            })
        
        # Sort by total cost
        cost_analysis.sort(key=lambda x: x["total_cost"])
        
        return {
            "analysis_type": "cost",
            "total_paths": len(cost_analysis),
            "cost_analysis": cost_analysis,
            "cheapest_path": cost_analysis[0] if cost_analysis else None,
            "most_expensive_path": cost_analysis[-1] if cost_analysis else None
        }
    
    def _analyze_path_probabilities(self, tree: AttackTree) -> Dict[str, Any]:
        """Analyze attack path success and detection probabilities."""
        probability_analysis = []
        
        for path in tree.attack_paths:
            probability_analysis.append({
                "path_id": path.path_id,
                "success_probability": path.success_probability,
                "detection_probability": path.detection_probability,
                "net_success_probability": path.success_probability * (1 - path.detection_probability),
                "nodes": [{"node": node.name, "success_prob": node.success_probability, 
                          "detection_prob": node.detection_probability} for node in path.nodes]
            })
        
        # Sort by net success probability
        probability_analysis.sort(key=lambda x: x["net_success_probability"], reverse=True)
        
        return {
            "analysis_type": "probability",
            "total_paths": len(probability_analysis),
            "probability_analysis": probability_analysis,
            "most_likely_success": probability_analysis[0] if probability_analysis else None
        }
    
    def _analyze_path_comprehensive(self, tree: AttackTree) -> Dict[str, Any]:
        """Comprehensive analysis of all attack paths."""
        comprehensive_analysis = []
        
        for path in tree.attack_paths:
            feasibility_score = self._calculate_feasibility_score(path)
            net_success_probability = path.success_probability * (1 - path.detection_probability)
            
            comprehensive_analysis.append({
                "path_id": path.path_id,
                "feasibility_score": feasibility_score,
                "total_cost": path.total_cost,
                "success_probability": path.success_probability,
                "detection_probability": path.detection_probability,
                "net_success_probability": net_success_probability,
                "risk_score": feasibility_score * net_success_probability,
                "nodes": [node.name for node in path.nodes],
                "node_details": [{"name": node.name, "cost": node.cost, "difficulty": node.difficulty.value} 
                               for node in path.nodes]
            })
        
        # Sort by risk score
        comprehensive_analysis.sort(key=lambda x: x["risk_score"], reverse=True)
        
        return {
            "analysis_type": "comprehensive",
            "total_paths": len(comprehensive_analysis),
            "comprehensive_analysis": comprehensive_analysis,
            "highest_risk_path": comprehensive_analysis[0] if comprehensive_analysis else None
        }
    
    def identify_critical_nodes(self, tree: AttackTree, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify critical nodes that are most important for attack success.
        
        Args:
            tree: Attack tree to analyze
            criteria: Criteria for identifying critical nodes
            
        Returns:
            List of critical nodes with importance scores
        """
        path_frequency_threshold = criteria.get("path_frequency", 0.8)
        difficulty_threshold = criteria.get("difficulty_threshold", "low")
        cost_threshold = criteria.get("cost_threshold", 10000)
        
        critical_nodes = []
        
        for node in tree.all_nodes:
            # Calculate path frequency
            path_frequency = sum(1 for path in tree.attack_paths if node in path.nodes) / len(tree.attack_paths)
            
            # Check if node meets criteria
            is_critical = (
                path_frequency >= path_frequency_threshold and
                node.difficulty.value <= difficulty_threshold and
                node.cost <= cost_threshold
            )
            
            if is_critical:
                # Calculate importance score
                importance_score = (
                    path_frequency * 0.4 +
                    (1 - node.cost / cost_threshold) * 0.3 +
                    (1 - node.detection_probability) * 0.3
                )
                
                critical_nodes.append({
                    "node": node,
                    "name": node.name,
                    "importance_score": importance_score,
                    "path_frequency": path_frequency,
                    "difficulty": node.difficulty.value,
                    "cost": node.cost,
                    "success_probability": node.success_probability,
                    "detection_probability": node.detection_probability,
                    "recommended_countermeasures": self._get_recommended_countermeasures(node)
                })
        
        # Sort by importance score
        critical_nodes.sort(key=lambda x: x["importance_score"], reverse=True)
        
        return critical_nodes
    
    def _get_recommended_countermeasures(self, node: AttackNode) -> List[str]:
        """Get recommended countermeasures for a node."""
        countermeasures = []
        
        # Based on node characteristics
        if node.difficulty == DifficultyLevel.EASY:
            countermeasures.append("Implement basic security controls")
        
        if node.cost < 5000:
            countermeasures.append("Add cost barriers")
        
        if node.success_probability > 0.7:
            countermeasures.append("Reduce success probability")
        
        if node.detection_probability < 0.3:
            countermeasures.append("Improve detection capabilities")
        
        # Generic countermeasures
        countermeasures.extend([
            "Monitor for attack indicators",
            "Implement defense in depth",
            "Regular security assessments"
        ])
        
        return countermeasures
    
    def get_feasible_paths(self, analysis_result: Dict[str, Any], threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Get attack paths above feasibility threshold."""
        if analysis_result["analysis_type"] != "feasibility":
            raise ValueError("Analysis result must be of type 'feasibility'")
        
        return [path for path in analysis_result["feasible_paths"] 
                if path["feasibility_score"] >= threshold]
    
    def update_attack_paths(self, tree: AttackTree):
        """Update attack paths after tree modification."""
        tree.generate_attack_paths()
        
        # Recalculate path properties
        for path in tree.attack_paths:
            path.total_cost = sum(node.cost for node in path.nodes)
            
            # Recalculate success probability
            success_prob = 1.0
            for node in path.nodes:
                success_prob *= node.success_probability
            path.success_probability = success_prob
            
            # Recalculate detection probability
            detection_prob = 1.0
            for node in path.nodes:
                detection_prob *= (1 - node.detection_probability)
            path.detection_probability = 1 - detection_prob