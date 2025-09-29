"""
Main TARA framework integration layer.
"""

from typing import List, Dict, Any, Optional, Union
import json
import os
from datetime import datetime

from .core.models import (
    Asset, Threat, Vulnerability, RiskAssessment, AttackTree, AttackPath,
    AttackerProfile, DefenderProfile, GameModel, EquilibriumResult,
    AnalysisResult, Recommendation, ExecutiveSummary
)
from .core.exceptions import TARAFrameworkError, ConfigurationError, ValidationError
from .core.validators import validate_analysis_input
from .components.tara import TARAComponent
from .components.attack_trees import AttackTreesComponent
from .components.game_theory import GameTheoryComponent


class TARAFramework:
    """Main TARA framework class that integrates all components."""
    
    def __init__(self, scope: str = "vehicle_system", analysis_type: str = "comprehensive", 
                 output_format: str = "structured", config: Optional[Dict[str, Any]] = None):
        """
        Initialize the TARA framework.
        
        Args:
            scope: Analysis scope
            analysis_type: Type of analysis to perform
            output_format: Output format for results
            config: Framework configuration
        """
        self.scope = scope
        self.analysis_type = analysis_type
        self.output_format = output_format
        self.config = config or {}
        
        # Initialize components
        self.tara = TARAComponent(self.config.get("tara", {}))
        self.attack_trees = AttackTreesComponent(self.config.get("attack_trees", {}))
        self.game_theory = GameTheoryComponent(self.config.get("game_theory", {}))
        
        # Framework state
        self.analysis_results = None
        self.current_analysis = None
        
        # Default configuration
        self.default_config = {
            "framework": {
                "version": "1.0",
                "analysis_depth": "detailed",
                "output_format": "structured"
            },
            "tara": {
                "asset_valuation_method": "weighted_scoring",
                "risk_tolerance": "medium",
                "threat_intelligence_sources": ["cve", "mitre", "automotive_specific"]
            },
            "attack_trees": {
                "max_tree_depth": 8,
                "node_validation": True,
                "path_analysis_method": "feasibility_based"
            },
            "game_theory": {
                "equilibrium_concept": "nash",
                "information_set": "incomplete",
                "sensitivity_analysis": True
            }
        }
    
    def configure(self, **kwargs):
        """Configure framework parameters."""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
            else:
                self.config[key] = value
    
    def configure_framework(self, config: Dict[str, Any]):
        """Configure framework using a configuration dictionary."""
        try:
            # Validate configuration
            if not self.validate_configuration(config):
                raise ConfigurationError("Invalid configuration provided")
            
            # Update configuration
            self.config.update(config)
            
            # Reinitialize components with new configuration
            self.tara = TARAComponent(self.config.get("tara", {}))
            self.attack_trees = AttackTreesComponent(self.config.get("attack_trees", {}))
            self.game_theory = GameTheoryComponent(self.config.get("game_theory", {}))
            
        except Exception as e:
            raise ConfigurationError(f"Failed to configure framework: {str(e)}")
    
    def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """Validate framework configuration."""
        try:
            # Check required sections
            required_sections = ["framework", "tara", "attack_trees", "game_theory"]
            for section in required_sections:
                if section not in config:
                    return False
            
            # Validate framework section
            framework_config = config["framework"]
            if "version" not in framework_config:
                return False
            
            # Validate TARA section
            tara_config = config["tara"]
            if "asset_valuation_method" not in tara_config:
                return False
            
            # Validate attack trees section
            attack_trees_config = config["attack_trees"]
            if "max_tree_depth" not in attack_trees_config:
                return False
            
            # Validate game theory section
            game_theory_config = config["game_theory"]
            if "equilibrium_concept" not in game_theory_config:
                return False
            
            return True
            
        except Exception:
            return False
    
    def run_comprehensive_analysis(self, system_definition: Dict[str, Any]) -> AnalysisResult:
        """
        Run a comprehensive analysis using all framework components.
        
        Args:
            system_definition: Complete system definition and analysis parameters
            
        Returns:
            Comprehensive analysis results
        """
        try:
            # Validate input
            validation_errors = validate_analysis_input(system_definition)
            if validation_errors:
                raise ValidationError(f"Input validation failed: {', '.join(validation_errors)}")
            
            # Step 1: TARA Analysis
            print("Starting TARA analysis...")
            tara_results = self.tara.run_analysis(system_definition)
            
            # Step 2: Attack Tree Construction
            print("Constructing attack trees...")
            attack_trees = []
            for high_risk_asset in tara_results["high_risk_assets"]:
                # Create threat scenario for each high-risk asset
                threat_scenario = {
                    "goal": f"compromise_{high_risk_asset.name.lower()}",
                    "attacker_profile": "skilled_insider",
                    "attack_vector": "remote_exploitation"
                }
                
                tree = self.attack_trees.construct_attack_tree(high_risk_asset, threat_scenario)
                attack_trees.append(tree)
            
            # Step 3: Game Theory Analysis
            print("Performing game theory analysis...")
            game_theory_results = []
            for tree in attack_trees:
                # Create attacker and defender profiles
                attacker_profile = self.game_theory.create_attacker_profile({
                    "name": "organized_crime_group",
                    "skill_level": "advanced",
                    "resources": "high",
                    "motivation": "financial_gain",
                    "risk_tolerance": "medium",
                    "time_horizon": "short_term",
                    "capabilities": ["social_engineering", "technical_exploitation"],
                    "budget": 100000,
                    "team_size": 5
                })
                
                defender_profile = self.game_theory.create_defender_profile({
                    "name": "automotive_manufacturer",
                    "budget": 1000000,
                    "expertise_level": "high",
                    "response_time": "fast",
                    "available_countermeasures": ["encryption", "authentication", "monitoring"],
                    "risk_tolerance": "low"
                })
                
                # Create game model
                game_model = self.game_theory.create_game_model(tree, attacker_profile, defender_profile)
                
                # Find equilibrium
                equilibrium = self.game_theory.find_nash_equilibrium(game_model)
                game_theory_results.append(equilibrium)
            
            # Step 4: Generate Recommendations
            print("Generating recommendations...")
            recommendations = self.generate_recommendations_from_results(
                tara_results, attack_trees, game_theory_results
            )
            
            # Create comprehensive analysis result
            self.analysis_results = AnalysisResult(
                asset_inventory=tara_results["assets"],
                threat_assessment=tara_results["threats"],
                risk_assessment=tara_results["risk_assessments"],
                attack_trees=attack_trees,
                game_theory_results=game_theory_results,
                recommendations=recommendations,
                analysis_metadata={
                    "scope": system_definition.get("scope", {}),
                    "analysis_type": self.analysis_type,
                    "timestamp": datetime.now().isoformat(),
                    "framework_version": "1.0"
                }
            )
            
            print("Analysis completed successfully!")
            return self.analysis_results
            
        except Exception as e:
            raise TARAFrameworkError(f"Comprehensive analysis failed: {str(e)}")
    
    def generate_recommendations_from_results(self, tara_results: Dict[str, Any], 
                                            attack_trees: List[AttackTree], 
                                            game_theory_results: List[EquilibriumResult]) -> List[Recommendation]:
        """Generate recommendations based on analysis results."""
        recommendations = []
        
        # High-risk asset recommendations
        for asset in tara_results["high_risk_assets"]:
            recommendation = Recommendation(
                title=f"Secure {asset.name}",
                description=f"Implement additional security controls for {asset.name} due to high risk level",
                priority="high",
                category="asset_security",
                estimated_cost=50000,
                effectiveness_score=0.8,
                implementation_time="3-6 months",
                associated_risks=[asset.asset_id],
                prerequisites=["security_team", "budget_approval"],
                countermeasures=["encryption", "access_control", "monitoring"]
            )
            recommendations.append(recommendation)
        
        # Critical risk recommendations
        for risk in tara_results["critical_risks"]:
            recommendation = Recommendation(
                title=f"Mitigate {risk.threat.name}",
                description=f"Address critical risk: {risk.threat.name}",
                priority="critical",
                category="risk_mitigation",
                estimated_cost=100000,
                effectiveness_score=0.9,
                implementation_time="1-3 months",
                associated_risks=[risk.risk_id],
                prerequisites=["immediate_action", "executive_approval"],
                countermeasures=["patch_management", "incident_response", "security_monitoring"]
            )
            recommendations.append(recommendation)
        
        # Attack tree recommendations
        for tree in attack_trees:
            # Analyze critical nodes
            critical_nodes = self.attack_trees.identify_critical_nodes(tree, {
                "path_frequency": 0.8,
                "difficulty_threshold": "low",
                "cost_threshold": 10000
            })
            
            for node_info in critical_nodes[:3]:  # Top 3 critical nodes
                recommendation = Recommendation(
                    title=f"Protect against {node_info['name']}",
                    description=f"Implement countermeasures for critical attack node: {node_info['name']}",
                    priority="medium",
                    category="attack_prevention",
                    estimated_cost=25000,
                    effectiveness_score=0.7,
                    implementation_time="2-4 months",
                    associated_risks=[tree.tree_id],
                    prerequisites=["technical_implementation"],
                    countermeasures=node_info["recommended_countermeasures"]
                )
                recommendations.append(recommendation)
        
        # Game theory recommendations
        for equilibrium in game_theory_results:
            if equilibrium.attack_success_probability > 0.7:
                recommendation = Recommendation(
                    title="Improve Defense Strategy",
                    description=f"Current defense strategy allows {equilibrium.attack_success_probability:.1%} attack success probability",
                    priority="high",
                    category="strategic_defense",
                    estimated_cost=75000,
                    effectiveness_score=0.8,
                    implementation_time="4-6 months",
                    associated_risks=["strategic_risk"],
                    prerequisites=["strategy_review", "budget_allocation"],
                    countermeasures=["defense_in_depth", "threat_intelligence", "incident_response"]
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def generate_recommendations(self, analysis_result: AnalysisResult) -> List[Recommendation]:
        """
        Generate security recommendations based on analysis results.
        
        Args:
            analysis_result: Results from comprehensive analysis
            
        Returns:
            Prioritized security recommendations
        """
        if not analysis_result:
            raise TARAFrameworkError("No analysis results available for recommendation generation")
        
        return analysis_result.recommendations
    
    def export_results(self, analysis_result: AnalysisResult, format_type: str) -> str:
        """
        Export analysis results in various formats.
        
        Args:
            analysis_result: Analysis results to export
            format_type: Export format ("json", "xml", "pdf", "excel")
            
        Returns:
            Path to exported file
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format_type == "json":
                return self._export_to_json(analysis_result, timestamp)
            elif format_type == "xml":
                return self._export_to_xml(analysis_result, timestamp)
            elif format_type == "pdf":
                return self._export_to_pdf(analysis_result, timestamp)
            elif format_type == "excel":
                return self._export_to_excel(analysis_result, timestamp)
            else:
                raise TARAFrameworkError(f"Unsupported export format: {format_type}")
                
        except Exception as e:
            raise TARAFrameworkError(f"Export failed: {str(e)}")
    
    def _export_to_json(self, analysis_result: AnalysisResult, timestamp: str) -> str:
        """Export results to JSON format."""
        filename = f"tara_analysis_{timestamp}.json"
        filepath = os.path.join("/workspace", filename)
        
        # Convert to serializable format
        export_data = {
            "analysis_metadata": analysis_result.analysis_metadata,
            "assets": [self._asset_to_dict(asset) for asset in analysis_result.asset_inventory],
            "threats": [self._threat_to_dict(threat) for threat in analysis_result.threat_assessment],
            "risks": [self._risk_to_dict(risk) for risk in analysis_result.risk_assessment],
            "attack_trees": [self._tree_to_dict(tree) for tree in analysis_result.attack_trees],
            "game_theory_results": [self._equilibrium_to_dict(eq) for eq in analysis_result.game_theory_results],
            "recommendations": [self._recommendation_to_dict(rec) for rec in analysis_result.recommendations]
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return filepath
    
    def _export_to_xml(self, analysis_result: AnalysisResult, timestamp: str) -> str:
        """Export results to XML format."""
        filename = f"tara_analysis_{timestamp}.xml"
        filepath = os.path.join("/workspace", filename)
        
        # Simple XML export
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<tara_analysis>
    <metadata>
        <timestamp>{analysis_result.analysis_metadata.get('timestamp', '')}</timestamp>
        <framework_version>{analysis_result.analysis_metadata.get('framework_version', '')}</framework_version>
    </metadata>
    <assets>
        {''.join([f'<asset name="{asset.name}" type="{asset.asset_type.value}" value="{asset.value}"/>' for asset in analysis_result.asset_inventory])}
    </assets>
    <threats>
        {''.join([f'<threat name="{threat.name}" likelihood="{threat.likelihood}" impact="{threat.impact}"/>' for threat in analysis_result.threat_assessment])}
    </threats>
    <recommendations>
        {''.join([f'<recommendation title="{rec.title}" priority="{rec.priority}" cost="{rec.estimated_cost}"/>' for rec in analysis_result.recommendations])}
    </recommendations>
</tara_analysis>"""
        
        with open(filepath, 'w') as f:
            f.write(xml_content)
        
        return filepath
    
    def _export_to_pdf(self, analysis_result: AnalysisResult, timestamp: str) -> str:
        """Export results to PDF format."""
        filename = f"tara_analysis_{timestamp}.pdf"
        filepath = os.path.join("/workspace", filename)
        
        # Simple text-based PDF export
        pdf_content = f"""
TARA Framework Analysis Report
Generated: {timestamp}

EXECUTIVE SUMMARY
================
Total Assets: {len(analysis_result.asset_inventory)}
Total Threats: {len(analysis_result.threat_assessment)}
Total Risks: {len(analysis_result.risk_assessment)}
Attack Trees: {len(analysis_result.attack_trees)}
Recommendations: {len(analysis_result.recommendations)}

HIGH-RISK ASSETS
================
{chr(10).join([f"- {asset.name} (Value: {asset.value})" for asset in analysis_result.asset_inventory if asset.value >= 7.0])}

CRITICAL RISKS
==============
{chr(10).join([f"- {risk.threat.name} (Risk Level: {risk.risk_level.value})" for risk in analysis_result.risk_assessment if risk.risk_level.value == 'critical'])}

TOP RECOMMENDATIONS
==================
{chr(10).join([f"- {rec.title} (Priority: {rec.priority}, Cost: ${rec.estimated_cost:,})" for rec in analysis_result.recommendations[:5]])}
"""
        
        with open(filepath, 'w') as f:
            f.write(pdf_content)
        
        return filepath
    
    def _export_to_excel(self, analysis_result: AnalysisResult, timestamp: str) -> str:
        """Export results to Excel format."""
        filename = f"tara_analysis_{timestamp}.csv"
        filepath = os.path.join("/workspace", filename)
        
        # Simple CSV export
        csv_content = "Type,Name,Value,Priority,Cost\n"
        
        # Add assets
        for asset in analysis_result.asset_inventory:
            csv_content += f"Asset,{asset.name},{asset.value},,\n"
        
        # Add recommendations
        for rec in analysis_result.recommendations:
            csv_content += f"Recommendation,{rec.title},,{rec.priority},{rec.estimated_cost}\n"
        
        with open(filepath, 'w') as f:
            f.write(csv_content)
        
        return filepath
    
    def generate_executive_summary(self, analysis_result: AnalysisResult) -> ExecutiveSummary:
        """
        Generate an executive summary of the analysis.
        
        Args:
            analysis_result: Analysis results to summarize
            
        Returns:
            Executive summary document
        """
        try:
            # Key findings
            key_findings = [
                f"Identified {len(analysis_result.asset_inventory)} critical assets",
                f"Assessed {len(analysis_result.threat_assessment)} potential threats",
                f"Found {len(analysis_result.risk_assessment)} risk scenarios",
                f"Constructed {len(analysis_result.attack_trees)} attack trees",
                f"Generated {len(analysis_result.recommendations)} security recommendations"
            ]
            
            # Risk overview
            critical_risks = [risk for risk in analysis_result.risk_assessment if risk.risk_level.value == 'critical']
            high_risks = [risk for risk in analysis_result.risk_assessment if risk.risk_level.value == 'high']
            
            risk_overview = f"Critical risks: {len(critical_risks)}, High risks: {len(high_risks)}"
            
            # Top recommendations
            top_recommendations = [rec.title for rec in analysis_result.recommendations[:5]]
            
            # Investment priorities
            high_priority_recs = [rec for rec in analysis_result.recommendations if rec.priority == 'high']
            total_investment = sum(rec.estimated_cost for rec in high_priority_recs)
            
            investment_priorities = [
                f"High-priority recommendations: {len(high_priority_recs)}",
                f"Total estimated investment: ${total_investment:,}",
                f"Average cost per recommendation: ${total_investment // len(high_priority_recs) if high_priority_recs else 0:,}"
            ]
            
            # Critical risks
            critical_risk_names = [risk.threat.name for risk in critical_risks]
            
            return ExecutiveSummary(
                key_findings=key_findings,
                risk_overview=risk_overview,
                recommendations=top_recommendations,
                investment_priorities=investment_priorities,
                critical_risks=critical_risk_names
            )
            
        except Exception as e:
            raise TARAFrameworkError(f"Failed to generate executive summary: {str(e)}")
    
    def optimize_performance(self, performance_profile: Dict[str, Any]):
        """Optimize framework performance based on usage profile."""
        # This is a placeholder for performance optimization
        # In a real implementation, this would configure caching, parallel processing, etc.
        pass
    
    # Helper methods for serialization
    def _asset_to_dict(self, asset: Asset) -> Dict[str, Any]:
        """Convert Asset to dictionary."""
        return {
            "name": asset.name,
            "type": asset.asset_type.value,
            "value": asset.value,
            "location": asset.location,
            "impact_safety": asset.impact_safety,
            "impact_financial": asset.impact_financial,
            "impact_operational": asset.impact_operational,
            "impact_privacy": asset.impact_privacy
        }
    
    def _threat_to_dict(self, threat: Threat) -> Dict[str, Any]:
        """Convert Threat to dictionary."""
        return {
            "name": threat.name,
            "type": threat.threat_type.value,
            "likelihood": threat.likelihood,
            "impact": threat.impact,
            "description": threat.description
        }
    
    def _risk_to_dict(self, risk: RiskAssessment) -> Dict[str, Any]:
        """Convert RiskAssessment to dictionary."""
        return {
            "threat_name": risk.threat.name,
            "risk_level": risk.risk_level.value,
            "risk_score": risk.risk_score,
            "likelihood": risk.likelihood,
            "impact": risk.impact,
            "justification": risk.justification
        }
    
    def _tree_to_dict(self, tree: AttackTree) -> Dict[str, Any]:
        """Convert AttackTree to dictionary."""
        return {
            "target_asset": tree.target_asset.name,
            "threat_scenario": tree.threat_scenario,
            "total_nodes": len(tree.all_nodes),
            "attack_paths": len(tree.attack_paths),
            "description": tree.description
        }
    
    def _equilibrium_to_dict(self, equilibrium: EquilibriumResult) -> Dict[str, Any]:
        """Convert EquilibriumResult to dictionary."""
        return {
            "attacker_strategy": equilibrium.attacker_strategy,
            "defender_strategy": equilibrium.defender_strategy,
            "attacker_payoff": equilibrium.attacker_payoff,
            "defender_payoff": equilibrium.defender_payoff,
            "attack_success_probability": equilibrium.attack_success_probability,
            "stability": equilibrium.stability
        }
    
    def _recommendation_to_dict(self, rec: Recommendation) -> Dict[str, Any]:
        """Convert Recommendations to dictionary."""
        return {
            "title": rec.title,
            "priority": rec.priority,
            "category": rec.category,
            "estimated_cost": rec.estimated_cost,
            "effectiveness_score": rec.effectiveness_score,
            "implementation_time": rec.implementation_time,
            "description": rec.description
        }