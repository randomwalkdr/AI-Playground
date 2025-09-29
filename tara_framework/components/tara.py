"""
TARA (Threat Analysis and Risk Assessment) component implementation.
"""

from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime

from ..core.models import (
    Asset, AssetType, AssetValue, Threat, ThreatType, Vulnerability, 
    RiskAssessment, RiskLevel
)
from ..core.exceptions import AssetIdentificationError, ThreatAssessmentError
from ..core.validators import AssetValidator, ThreatValidator, VulnerabilityValidator


class TARAComponent:
    """TARA component for asset identification and threat assessment."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize TARA component with configuration."""
        self.config = config or {}
        self.asset_valuation_method = self.config.get("asset_valuation_method", "weighted_scoring")
        self.risk_tolerance = self.config.get("risk_tolerance", "medium")
        self.threat_intelligence_sources = self.config.get("threat_intelligence_sources", [])
        
        # Default asset categories for automotive systems
        self.asset_categories = {
            "physical": [
                "ecus", "sensors", "actuators", "communication_buses", 
                "gateway_modules", "infotainment_systems", "telematics_units"
            ],
            "software": [
                "firmware", "applications", "operating_systems", "middleware",
                "bootloaders", "device_drivers", "communication_stacks"
            ],
            "data": [
                "user_data", "operational_data", "configuration_data", "keys",
                "calibration_data", "diagnostic_data", "personal_information"
            ],
            "function": [
                "safety_functions", "control_functions", "communication_functions",
                "authentication_functions", "encryption_functions", "monitoring_functions"
            ]
        }
        
        # Default threat actors for automotive systems
        self.threat_actors = {
            "script_kiddies": {
                "skill_level": "low",
                "resources": "limited",
                "motivation": "notoriety",
                "risk_tolerance": "high"
            },
            "organized_crime": {
                "skill_level": "medium",
                "resources": "moderate",
                "motivation": "financial_gain",
                "risk_tolerance": "medium"
            },
            "state_actors": {
                "skill_level": "high",
                "resources": "extensive",
                "motivation": "espionage",
                "risk_tolerance": "low"
            },
            "insiders": {
                "skill_level": "medium",
                "resources": "moderate",
                "motivation": "personal_gain",
                "risk_tolerance": "medium"
            }
        }
    
    def identify_assets(self, system_scope: Dict[str, Any], asset_types: List[str]) -> List[Asset]:
        """
        Identify and catalog critical assets within the defined system scope.
        
        Args:
            system_scope: System boundaries and scope definition
            asset_types: Types of assets to identify
            
        Returns:
            List of identified assets
            
        Raises:
            AssetIdentificationError: If asset identification fails
        """
        try:
            assets = []
            boundaries = system_scope.get("boundaries", "entire_vehicle")
            focus_areas = system_scope.get("focus_areas", [])
            exclusions = system_scope.get("exclusions", [])
            
            for asset_type in asset_types:
                if asset_type in self.asset_categories:
                    category_assets = self._identify_assets_by_category(
                        asset_type, boundaries, focus_areas, exclusions
                    )
                    assets.extend(category_assets)
            
            # Validate identified assets
            for asset in assets:
                errors = AssetValidator.validate_asset(asset)
                if errors:
                    raise AssetIdentificationError(
                        f"Invalid asset '{asset.name}': {', '.join(errors)}",
                        missing_info=errors
                    )
            
            return assets
            
        except Exception as e:
            if isinstance(e, AssetIdentificationError):
                raise
            raise AssetIdentificationError(f"Asset identification failed: {str(e)}")
    
    def _identify_assets_by_category(self, category: str, boundaries: str, 
                                   focus_areas: List[str], exclusions: List[str]) -> List[Asset]:
        """Identify assets for a specific category."""
        assets = []
        subcategories = self.asset_categories.get(category, [])
        
        for subcategory in subcategories:
            # Skip excluded assets
            if any(exclusion in subcategory for exclusion in exclusions):
                continue
            
            # Focus on specific areas if specified
            if focus_areas and not any(area in subcategory for area in focus_areas):
                continue
            
            # Create asset based on subcategory
            asset = self._create_asset_from_subcategory(subcategory, category, boundaries)
            assets.append(asset)
        
        return assets
    
    def _create_asset_from_subcategory(self, subcategory: str, category: str, boundaries: str) -> Asset:
        """Create an Asset object from a subcategory."""
        # Default asset properties
        asset_properties = {
            "name": subcategory.replace("_", " ").title(),
            "asset_type": AssetType(category),
            "description": f"{subcategory.replace('_', ' ')} in {boundaries}",
            "location": boundaries,
            "value": 5.0,  # Default medium value
            "impact_safety": 3.0,
            "impact_financial": 4.0,
            "impact_operational": 3.0,
            "impact_privacy": 2.0
        }
        
        # Customize based on subcategory
        if "ecu" in subcategory or "control" in subcategory:
            asset_properties["impact_safety"] = 8.0
            asset_properties["value"] = 8.0
        elif "safety" in subcategory:
            asset_properties["impact_safety"] = 9.0
            asset_properties["value"] = 9.0
        elif "data" in subcategory or "user" in subcategory:
            asset_properties["impact_privacy"] = 7.0
            asset_properties["value"] = 6.0
        elif "communication" in subcategory:
            asset_properties["impact_operational"] = 6.0
            asset_properties["value"] = 7.0
        
        return Asset(**asset_properties)
    
    def assess_asset_value(self, asset: Asset, criteria: Dict[str, Any]) -> AssetValue:
        """
        Assess the value of an identified asset based on multiple criteria.
        
        Args:
            asset: Asset object to evaluate
            criteria: Valuation criteria
            
        Returns:
            Comprehensive asset valuation
        """
        if self.asset_valuation_method == "weighted_scoring":
            return self._assess_asset_value_weighted(asset, criteria)
        else:
            return self._assess_asset_value_simple(asset, criteria)
    
    def _assess_asset_value_weighted(self, asset: Asset, criteria: Dict[str, Any]) -> AssetValue:
        """Assess asset value using weighted scoring method."""
        weights = criteria.get("weights", {
            "safety": 0.4,
            "financial": 0.3,
            "operational": 0.2,
            "privacy": 0.1
        })
        
        safety_score = asset.impact_safety * weights["safety"]
        financial_score = asset.impact_financial * weights["financial"]
        operational_score = asset.impact_operational * weights["operational"]
        privacy_score = asset.impact_privacy * weights["privacy"]
        
        total_score = safety_score + financial_score + operational_score + privacy_score
        
        justification = f"Weighted scoring: Safety({safety_score:.2f}) + Financial({financial_score:.2f}) + Operational({operational_score:.2f}) + Privacy({privacy_score:.2f})"
        
        return AssetValue(
            asset=asset,
            safety_score=safety_score,
            financial_score=financial_score,
            operational_score=operational_score,
            privacy_score=privacy_score,
            total_score=total_score,
            valuation_method="weighted_scoring",
            justification=justification
        )
    
    def _assess_asset_value_simple(self, asset: Asset, criteria: Dict[str, Any]) -> AssetValue:
        """Assess asset value using simple averaging method."""
        total_score = (asset.impact_safety + asset.impact_financial + 
                      asset.impact_operational + asset.impact_privacy) / 4
        
        justification = f"Simple average: ({asset.impact_safety} + {asset.impact_financial} + {asset.impact_operational} + {asset.impact_privacy}) / 4"
        
        return AssetValue(
            asset=asset,
            safety_score=asset.impact_safety,
            financial_score=asset.impact_financial,
            operational_score=asset.impact_operational,
            privacy_score=asset.impact_privacy,
            total_score=total_score,
            valuation_method="simple_average",
            justification=justification
        )
    
    def identify_threats(self, assets: List[Asset], threat_intelligence: Dict[str, Any]) -> List[Threat]:
        """
        Identify potential threats targeting the identified assets.
        
        Args:
            assets: Previously identified assets
            threat_intelligence: Threat intelligence data and profiles
            
        Returns:
            List of identified threats with associated metadata
        """
        try:
            threats = []
            threat_actors = threat_intelligence.get("threat_actors", list(self.threat_actors.keys()))
            attack_vectors = threat_intelligence.get("attack_vectors", [])
            motivations = threat_intelligence.get("motivations", [])
            
            # Generate threats for each asset-threat actor combination
            for asset in assets:
                for actor in threat_actors:
                    threat = self._create_threat_for_asset(asset, actor, attack_vectors, motivations)
                    if threat:
                        threats.append(threat)
            
            # Validate identified threats
            for threat in threats:
                errors = ThreatValidator.validate_threat(threat)
                if errors:
                    raise ThreatAssessmentError(
                        f"Invalid threat '{threat.name}': {', '.join(errors)}",
                        invalid_threats=errors
                    )
            
            return threats
            
        except Exception as e:
            if isinstance(e, ThreatAssessmentError):
                raise
            raise ThreatAssessmentError(f"Threat identification failed: {str(e)}")
    
    def _create_threat_for_asset(self, asset: Asset, actor: str, 
                               attack_vectors: List[str], motivations: List[str]) -> Optional[Threat]:
        """Create a threat for a specific asset and threat actor."""
        actor_profile = self.threat_actors.get(actor, {})
        
        # Determine threat type based on asset and actor
        threat_type = self._determine_threat_type(asset, actor)
        
        # Calculate likelihood based on actor profile and asset
        likelihood = self._calculate_threat_likelihood(actor_profile, asset)
        
        # Calculate impact based on asset value
        impact = min(asset.get_total_impact(), 10.0)
        
        # Create threat name
        threat_name = f"{actor.replace('_', ' ').title()} targeting {asset.name}"
        
        # Create threat description
        description = f"{actor.replace('_', ' ')} attempting to compromise {asset.name} through {threat_type.value}"
        
        return Threat(
            name=threat_name,
            threat_type=threat_type,
            description=description,
            likelihood=likelihood,
            impact=impact,
            attack_vectors=attack_vectors,
            affected_assets=[asset.asset_id],
            threat_actors=[actor]
        )
    
    def _determine_threat_type(self, asset: Asset, actor: str) -> ThreatType:
        """Determine the most likely threat type for an asset-actor combination."""
        if asset.asset_type == AssetType.PHYSICAL:
            return ThreatType.PHYSICAL_ACCESS
        elif asset.asset_type == AssetType.SOFTWARE:
            return ThreatType.REMOTE_EXPLOITATION
        elif asset.asset_type == AssetType.DATA:
            return ThreatType.MALWARE
        else:
            return ThreatType.SOCIAL_ENGINEERING
    
    def _calculate_threat_likelihood(self, actor_profile: Dict[str, str], asset: Asset) -> float:
        """Calculate threat likelihood based on actor profile and asset."""
        base_likelihood = 0.3  # Base likelihood
        
        # Adjust based on actor skill level
        skill_level = actor_profile.get("skill_level", "medium")
        if skill_level == "low":
            base_likelihood *= 0.7
        elif skill_level == "high":
            base_likelihood *= 1.3
        
        # Adjust based on actor resources
        resources = actor_profile.get("resources", "moderate")
        if resources == "limited":
            base_likelihood *= 0.8
        elif resources == "extensive":
            base_likelihood *= 1.2
        
        # Adjust based on asset value (higher value = higher likelihood)
        value_factor = asset.value / 10.0
        base_likelihood *= (0.5 + value_factor * 0.5)
        
        return min(base_likelihood, 1.0)
    
    def assess_risk_level(self, threat: Threat, vulnerability: Vulnerability, 
                         impact: Dict[str, float]) -> RiskAssessment:
        """
        Calculate risk level for a specific threat-vulnerability-impact combination.
        
        Args:
            threat: Threat object
            vulnerability: Associated vulnerability
            impact: Potential impact assessment
            
        Returns:
            Calculated risk level
        """
        # Calculate risk score
        risk_score = threat.likelihood * threat.impact
        
        # Adjust based on vulnerability severity
        severity_multiplier = {
            "low": 0.5,
            "medium": 1.0,
            "high": 1.5,
            "critical": 2.0
        }.get(vulnerability.severity, 1.0)
        
        risk_score *= severity_multiplier
        
        # Determine risk level
        if risk_score >= 7.0:
            risk_level = RiskLevel.CRITICAL
        elif risk_score >= 5.0:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 3.0:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Create justification
        justification = f"Risk score: {risk_score:.2f} (likelihood: {threat.likelihood:.2f} × impact: {threat.impact:.2f} × severity: {severity_multiplier:.2f})"
        
        # Create dummy asset for risk assessment
        asset = Asset(
            name="Assessment Asset",
            asset_type=AssetType.SOFTWARE,
            description="Asset for risk assessment",
            location="system",
            value=threat.impact
        )
        
        return RiskAssessment(
            threat=threat,
            vulnerability=vulnerability,
            asset=asset,
            risk_level=risk_level,
            risk_score=risk_score,
            likelihood=threat.likelihood,
            impact=threat.impact,
            justification=justification
        )
    
    def run_analysis(self, system_definition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run comprehensive TARA analysis.
        
        Args:
            system_definition: Complete system definition and analysis parameters
            
        Returns:
            TARA analysis results
        """
        try:
            # Extract parameters
            scope = system_definition.get("scope", {})
            asset_types = system_definition.get("asset_types", ["physical", "software", "data", "function"])
            threat_intelligence = system_definition.get("threat_intelligence", {})
            
            # Step 1: Identify assets
            assets = self.identify_assets(scope, asset_types)
            
            # Step 2: Assess asset values
            asset_values = []
            for asset in assets:
                criteria = system_definition.get("asset_valuation_criteria", {})
                value = self.assess_asset_value(asset, criteria)
                asset_values.append(value)
            
            # Step 3: Identify threats
            threats = self.identify_threats(assets, threat_intelligence)
            
            # Step 4: Assess risks
            risk_assessments = []
            for threat in threats:
                # Create dummy vulnerability for each threat
                vulnerability = Vulnerability(
                    name=f"Vulnerability for {threat.name}",
                    description=f"Vulnerability associated with {threat.name}",
                    severity="medium",
                    exploitability="medium"
                )
                
                impact = {
                    "safety": threat.impact * 0.4,
                    "financial": threat.impact * 0.3,
                    "operational": threat.impact * 0.2,
                    "privacy": threat.impact * 0.1
                }
                
                risk = self.assess_risk_level(threat, vulnerability, impact)
                risk_assessments.append(risk)
            
            return {
                "assets": assets,
                "asset_values": asset_values,
                "threats": threats,
                "risk_assessments": risk_assessments,
                "high_risk_assets": [asset for asset in assets if asset.value >= 7.0],
                "critical_risks": [risk for risk in risk_assessments if risk.risk_level == RiskLevel.CRITICAL]
            }
            
        except Exception as e:
            raise ThreatAssessmentError(f"TARA analysis failed: {str(e)}")
    
    def get_high_risk_assets(self, assets: List[Asset], threshold: float = 7.0) -> List[Asset]:
        """Get assets with risk above threshold."""
        return [asset for asset in assets if asset.value >= threshold]
    
    def get_critical_risks(self, risk_assessments: List[RiskAssessment]) -> List[RiskAssessment]:
        """Get critical risk assessments."""
        return [risk for risk in risk_assessments if risk.risk_level == RiskLevel.CRITICAL]