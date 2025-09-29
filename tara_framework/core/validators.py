"""
Data validation utilities for the TARA framework.
"""

from typing import List, Dict, Any, Optional
from .models import Asset, Threat, Vulnerability, AttackTree, AttackNode
from .exceptions import ValidationError


class DataValidator:
    """Base class for data validation."""
    
    @staticmethod
    def validate_required_fields(data: dict, required_fields: List[str]) -> List[str]:
        """Validate that required fields are present."""
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None:
                missing_fields.append(field)
        return missing_fields
    
    @staticmethod
    def validate_value_range(value: float, min_val: float, max_val: float) -> bool:
        """Validate that a value is within the specified range."""
        return min_val <= value <= max_val
    
    @staticmethod
    def validate_enum_value(value: str, valid_values: List[str]) -> bool:
        """Validate that a value is one of the valid enum values."""
        return value in valid_values


class AssetValidator(DataValidator):
    """Validator for Asset objects."""
    
    @staticmethod
    def validate_asset(asset: Asset) -> List[str]:
        """Validate an Asset object."""
        errors = []
        
        # Check required fields
        if not asset.name or len(asset.name.strip()) == 0:
            errors.append("Asset name is required")
        
        if not asset.description or len(asset.description.strip()) == 0:
            errors.append("Asset description is required")
        
        if not asset.location or len(asset.location.strip()) == 0:
            errors.append("Asset location is required")
        
        # Check value range
        if not DataValidator.validate_value_range(asset.value, 1.0, 10.0):
            errors.append("Asset value must be between 1.0 and 10.0")
        
        # Check impact scores
        impact_fields = [
            ("impact_safety", asset.impact_safety),
            ("impact_financial", asset.impact_financial),
            ("impact_operational", asset.impact_operational),
            ("impact_privacy", asset.impact_privacy)
        ]
        
        for field_name, value in impact_fields:
            if not DataValidator.validate_value_range(value, 0.0, 10.0):
                errors.append(f"{field_name} must be between 0.0 and 10.0")
        
        return errors
    
    @staticmethod
    def validate_asset_data(asset_data: dict) -> List[str]:
        """Validate asset data dictionary."""
        errors = []
        
        required_fields = ["name", "asset_type", "description", "location", "value"]
        missing_fields = DataValidator.validate_required_fields(asset_data, required_fields)
        errors.extend([f"Missing required field: {field}" for field in missing_fields])
        
        if "value" in asset_data:
            if not DataValidator.validate_value_range(asset_data["value"], 1.0, 10.0):
                errors.append("Asset value must be between 1.0 and 10.0")
        
        return errors


class ThreatValidator(DataValidator):
    """Validator for Threat objects."""
    
    @staticmethod
    def validate_threat(threat: Threat) -> List[str]:
        """Validate a Threat object."""
        errors = []
        
        # Check required fields
        if not threat.name or len(threat.name.strip()) == 0:
            errors.append("Threat name is required")
        
        if not threat.description or len(threat.description.strip()) == 0:
            errors.append("Threat description is required")
        
        # Check likelihood range
        if not DataValidator.validate_value_range(threat.likelihood, 0.0, 1.0):
            errors.append("Threat likelihood must be between 0.0 and 1.0")
        
        # Check impact range
        if not DataValidator.validate_value_range(threat.impact, 1.0, 10.0):
            errors.append("Threat impact must be between 1.0 and 10.0")
        
        return errors
    
    @staticmethod
    def validate_threat_data(threat_data: dict) -> List[str]:
        """Validate threat data dictionary."""
        errors = []
        
        required_fields = ["name", "threat_type", "description", "likelihood", "impact"]
        missing_fields = DataValidator.validate_required_fields(threat_data, required_fields)
        errors.extend([f"Missing required field: {field}" for field in missing_fields])
        
        if "likelihood" in threat_data:
            if not DataValidator.validate_value_range(threat_data["likelihood"], 0.0, 1.0):
                errors.append("Threat likelihood must be between 0.0 and 1.0")
        
        if "impact" in threat_data:
            if not DataValidator.validate_value_range(threat_data["impact"], 1.0, 10.0):
                errors.append("Threat impact must be between 1.0 and 10.0")
        
        return errors


class VulnerabilityValidator(DataValidator):
    """Validator for Vulnerability objects."""
    
    @staticmethod
    def validate_vulnerability(vulnerability: Vulnerability) -> List[str]:
        """Validate a Vulnerability object."""
        errors = []
        
        # Check required fields
        if not vulnerability.name or len(vulnerability.name.strip()) == 0:
            errors.append("Vulnerability name is required")
        
        if not vulnerability.description or len(vulnerability.description.strip()) == 0:
            errors.append("Vulnerability description is required")
        
        # Check severity
        valid_severities = ["low", "medium", "high", "critical"]
        if not DataValidator.validate_enum_value(vulnerability.severity, valid_severities):
            errors.append(f"Vulnerability severity must be one of: {valid_severities}")
        
        # Check exploitability
        valid_exploitabilities = ["low", "medium", "high"]
        if not DataValidator.validate_enum_value(vulnerability.exploitability, valid_exploitabilities):
            errors.append(f"Vulnerability exploitability must be one of: {valid_exploitabilities}")
        
        # Check CVSS score if provided
        if vulnerability.cvss_score is not None:
            if not DataValidator.validate_value_range(vulnerability.cvss_score, 0.0, 10.0):
                errors.append("CVSS score must be between 0.0 and 10.0")
        
        return errors


class AttackTreeValidator(DataValidator):
    """Validator for AttackTree objects."""
    
    @staticmethod
    def validate_attack_tree(tree: AttackTree) -> List[str]:
        """Validate an AttackTree object."""
        errors = []
        
        # Check required fields
        if not tree.target_asset:
            errors.append("Attack tree must have a target asset")
        
        if not tree.threat_scenario or len(tree.threat_scenario.strip()) == 0:
            errors.append("Attack tree must have a threat scenario")
        
        # Validate root node
        if not tree.root_node:
            errors.append("Attack tree must have a root node")
        else:
            node_errors = AttackTreeValidator.validate_attack_node(tree.root_node)
            errors.extend([f"Root node: {error}" for error in node_errors])
        
        # Check tree structure
        if tree.root_node and len(tree.root_node.children) == 0:
            errors.append("Attack tree must have at least one child node")
        
        # Validate all nodes
        for node in tree.all_nodes:
            node_errors = AttackTreeValidator.validate_attack_node(node)
            errors.extend([f"Node '{node.name}': {error}" for error in node_errors])
        
        return errors
    
    @staticmethod
    def validate_attack_node(node: AttackNode) -> List[str]:
        """Validate an AttackNode object."""
        errors = []
        
        # Check required fields
        if not node.name or len(node.name.strip()) == 0:
            errors.append("Node name is required")
        
        if not node.description or len(node.description.strip()) == 0:
            errors.append("Node description is required")
        
        # Check cost
        if node.cost < 0:
            errors.append("Node cost cannot be negative")
        
        # Check probabilities
        if not DataValidator.validate_value_range(node.success_probability, 0.0, 1.0):
            errors.append("Success probability must be between 0.0 and 1.0")
        
        if not DataValidator.validate_value_range(node.detection_probability, 0.0, 1.0):
            errors.append("Detection probability must be between 0.0 and 1.0")
        
        return errors


class GameTheoryValidator(DataValidator):
    """Validator for Game Theory objects."""
    
    @staticmethod
    def validate_game_model(game_model: 'GameModel') -> List[str]:
        """Validate a GameModel object."""
        errors = []
        
        # Check required fields
        if not game_model.attack_tree:
            errors.append("Game model must have an attack tree")
        
        if not game_model.attacker:
            errors.append("Game model must have an attacker profile")
        
        if not game_model.defender:
            errors.append("Game model must have a defender profile")
        
        # Check game type
        valid_game_types = ["simultaneous", "sequential", "repeated"]
        if not DataValidator.validate_enum_value(game_model.game_type, valid_game_types):
            errors.append(f"Game type must be one of: {valid_game_types}")
        
        # Check information set
        valid_info_sets = ["complete", "incomplete"]
        if not DataValidator.validate_enum_value(game_model.information_set, valid_info_sets):
            errors.append(f"Information set must be one of: {valid_info_sets}")
        
        return errors
    
    @staticmethod
    def validate_payoff_matrix(payoff_matrix: 'PayoffMatrix') -> List[str]:
        """Validate a PayoffMatrix object."""
        errors = []
        
        # Check required fields
        if not payoff_matrix.attacker_strategies:
            errors.append("Payoff matrix must have attacker strategies")
        
        if not payoff_matrix.defender_strategies:
            errors.append("Payoff matrix must have defender strategies")
        
        if not payoff_matrix.payoffs:
            errors.append("Payoff matrix must have payoff values")
        
        # Check payoff completeness
        expected_combinations = len(payoff_matrix.attacker_strategies) * len(payoff_matrix.defender_strategies)
        actual_combinations = len(payoff_matrix.payoffs)
        
        if actual_combinations != expected_combinations:
            errors.append(f"Payoff matrix incomplete: expected {expected_combinations} combinations, got {actual_combinations}")
        
        return errors


def validate_analysis_input(data: dict) -> List[str]:
    """Validate input data for analysis."""
    errors = []
    
    # Check for required top-level fields
    required_fields = ["scope", "assets", "threats"]
    missing_fields = DataValidator.validate_required_fields(data, required_fields)
    errors.extend([f"Missing required field: {field}" for field in missing_fields])
    
    # Validate assets if present
    if "assets" in data:
        for i, asset_data in enumerate(data["assets"]):
            asset_errors = AssetValidator.validate_asset_data(asset_data)
            errors.extend([f"Asset {i}: {error}" for error in asset_errors])
    
    # Validate threats if present
    if "threats" in data:
        for i, threat_data in enumerate(data["threats"]):
            threat_errors = ThreatValidator.validate_threat_data(threat_data)
            errors.extend([f"Threat {i}: {error}" for error in threat_errors])
    
    return errors