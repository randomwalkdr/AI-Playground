#!/usr/bin/env python3
"""
Advanced usage example for the TARA framework.
This example demonstrates advanced features including custom configurations,
scenario analysis, and detailed component usage.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tara_framework import TARAFramework
from tara_framework.core.models import Asset, AssetType, Threat, ThreatType


def main():
    """Run an advanced TARA analysis example."""
    print("TARA Framework - Advanced Usage Example")
    print("=" * 50)
    
    # Custom configuration
    custom_config = {
        "framework": {
            "version": "1.0",
            "analysis_depth": "detailed",
            "output_format": "structured"
        },
        "tara": {
            "asset_valuation_method": "weighted_scoring",
            "risk_tolerance": "low",
            "threat_intelligence_sources": ["cve", "mitre", "automotive_specific", "custom"]
        },
        "attack_trees": {
            "max_tree_depth": 10,
            "node_validation": True,
            "path_analysis_method": "comprehensive"
        },
        "game_theory": {
            "equilibrium_concept": "nash",
            "information_set": "incomplete",
            "sensitivity_analysis": True
        }
    }
    
    # Initialize framework with custom configuration
    framework = TARAFramework(config=custom_config)
    
    # Define comprehensive system for analysis
    system_definition = {
        "scope": {
            "boundaries": "autonomous_vehicle_system",
            "focus_areas": ["sensors", "computing_platform", "communication", "safety_systems"],
            "exclusions": ["mechanical_components", "external_infrastructure"]
        },
        "asset_types": ["physical", "software", "data", "function"],
        "threat_intelligence": {
            "threat_actors": [
                {
                    "name": "script_kiddies",
                    "skill_level": "low",
                    "resources": "limited",
                    "motivation": "notoriety"
                },
                {
                    "name": "organized_crime",
                    "skill_level": "medium",
                    "resources": "moderate",
                    "motivation": "financial_gain"
                },
                {
                    "name": "state_actors",
                    "skill_level": "high",
                    "resources": "extensive",
                    "motivation": "espionage"
                }
            ],
            "attack_vectors": ["wireless", "physical", "supply_chain", "social_engineering"],
            "motivations": ["financial", "espionage", "disruption", "safety_compromise"]
        },
        "asset_valuation_criteria": {
            "weights": {
                "safety": 0.5,  # Higher weight for safety in autonomous vehicles
                "financial": 0.2,
                "operational": 0.2,
                "privacy": 0.1
            }
        }
    }
    
    try:
        # Step 1: Run TARA analysis
        print("Step 1: Running TARA analysis...")
        tara_results = framework.tara.run_analysis(system_definition)
        
        print(f"TARA Results:")
        print(f"- Assets: {len(tara_results['assets'])}")
        print(f"- Threats: {len(tara_results['threats'])}")
        print(f"- Risks: {len(tara_results['risk_assessments'])}")
        print(f"- High-risk assets: {len(tara_results['high_risk_assets'])}")
        print(f"- Critical risks: {len(tara_results['critical_risks'])}")
        
        # Step 2: Detailed asset analysis
        print(f"\nStep 2: Detailed asset analysis...")
        for asset in tara_results['high_risk_assets']:
            print(f"\nHigh-Risk Asset: {asset.name}")
            print(f"- Type: {asset.asset_type.value}")
            print(f"- Value: {asset.value}")
            print(f"- Safety Impact: {asset.impact_safety}")
            print(f"- Financial Impact: {asset.impact_financial}")
            print(f"- Operational Impact: {asset.impact_operational}")
            print(f"- Privacy Impact: {asset.impact_privacy}")
            print(f"- Total Impact: {asset.get_total_impact():.2f}")
        
        # Step 3: Construct detailed attack trees
        print(f"\nStep 3: Constructing detailed attack trees...")
        attack_trees = []
        
        for i, high_risk_asset in enumerate(tara_results['high_risk_assets'][:3]):  # Limit to top 3
            print(f"\nConstructing attack tree for {high_risk_asset.name}...")
            
            # Create multiple threat scenarios
            threat_scenarios = [
                {
                    "goal": f"compromise_{high_risk_asset.name.lower()}",
                    "attacker_profile": "organized_crime",
                    "attack_vector": "remote_exploitation"
                },
                {
                    "goal": f"extract_data_from_{high_risk_asset.name.lower()}",
                    "attacker_profile": "state_actors",
                    "attack_vector": "supply_chain"
                }
            ]
            
            for scenario in threat_scenarios:
                tree = framework.attack_trees.construct_attack_tree(high_risk_asset, scenario)
                attack_trees.append(tree)
                
                print(f"- Tree: {tree.root_node.name}")
                print(f"  Nodes: {len(tree.all_nodes)}")
                print(f"  Leaf nodes: {len(tree.leaf_nodes)}")
                print(f"  Attack paths: {len(tree.attack_paths)}")
                
                # Analyze attack paths
                path_analysis = framework.attack_trees.analyze_attack_paths(tree, "comprehensive")
                print(f"  Analysis type: {path_analysis['analysis_type']}")
                
                if path_analysis['highest_risk_path']:
                    highest_risk = path_analysis['highest_risk_path']
                    print(f"  Highest risk path: {highest_risk['risk_score']:.3f} risk score")
                    print(f"    Feasibility: {highest_risk['feasibility_score']:.3f}")
                    print(f"    Success probability: {highest_risk['success_probability']:.3f}")
                    print(f"    Total cost: ${highest_risk['total_cost']:,}")
                
                # Identify critical nodes
                critical_nodes = framework.attack_trees.identify_critical_nodes(tree, {
                    "path_frequency": 0.7,
                    "difficulty_threshold": "medium",
                    "cost_threshold": 15000
                })
                
                print(f"  Critical nodes: {len(critical_nodes)}")
                for node_info in critical_nodes[:3]:  # Top 3
                    print(f"    - {node_info['name']}: {node_info['importance_score']:.3f} importance")
        
        # Step 4: Game theory analysis with multiple scenarios
        print(f"\nStep 4: Game theory analysis...")
        
        # Create multiple attacker profiles
        attacker_profiles = [
            framework.game_theory.create_attacker_profile({
                "name": "script_kiddie",
                "skill_level": "low",
                "resources": "limited",
                "motivation": "notoriety",
                "risk_tolerance": "high",
                "time_horizon": "short_term",
                "capabilities": ["basic_exploitation"],
                "budget": 10000,
                "team_size": 1
            }),
            framework.game_theory.create_attacker_profile({
                "name": "organized_crime",
                "skill_level": "medium",
                "resources": "moderate",
                "motivation": "financial_gain",
                "risk_tolerance": "medium",
                "time_horizon": "medium_term",
                "capabilities": ["social_engineering", "technical_exploitation"],
                "budget": 100000,
                "team_size": 5
            }),
            framework.game_theory.create_attacker_profile({
                "name": "state_actor",
                "skill_level": "high",
                "resources": "extensive",
                "motivation": "espionage",
                "risk_tolerance": "low",
                "time_horizon": "long_term",
                "capabilities": ["advanced_exploitation", "supply_chain_compromise"],
                "budget": 1000000,
                "team_size": 20
            })
        ]
        
        # Create defender profile
        defender_profile = framework.game_theory.create_defender_profile({
            "name": "autonomous_vehicle_manufacturer",
            "budget": 5000000,
            "expertise_level": "high",
            "response_time": "fast",
            "available_countermeasures": [
                "encryption", "authentication", "monitoring", "intrusion_detection",
                "secure_boot", "hardware_security", "threat_intelligence"
            ],
            "risk_tolerance": "low",
            "compliance_requirements": ["iso_21434", "un_ce_wp29", "sae_j3061"]
        })
        
        # Analyze each attack tree with each attacker profile
        game_results = []
        for tree in attack_trees[:2]:  # Limit to first 2 trees
            print(f"\nAnalyzing game for tree: {tree.root_node.name}")
            
            for attacker in attacker_profiles:
                print(f"  Attacker: {attacker.name}")
                
                # Create game model
                game_model = framework.game_theory.create_game_model(tree, attacker, defender_profile)
                
                # Find Nash equilibrium
                equilibrium = framework.game_theory.find_nash_equilibrium(game_model)
                game_results.append(equilibrium)
                
                print(f"    Strategy: {equilibrium.attacker_strategy} vs {equilibrium.defender_strategy}")
                print(f"    Payoffs: Attacker {equilibrium.attacker_payoff:.0f}, Defender {equilibrium.defender_payoff:.0f}")
                print(f"    Success probability: {equilibrium.attack_success_probability:.3f}")
                print(f"    Stability: {equilibrium.stability:.3f}")
                print(f"    Outcome: {equilibrium.expected_outcome}")
        
        # Step 5: Scenario analysis
        print(f"\nStep 5: Scenario analysis...")
        
        scenarios = [
            {
                "name": "budget_increase",
                "budget_increase": 0.5,
                "description": "Defender budget increased by 50%"
            },
            {
                "name": "new_vulnerability",
                "new_vulnerability": True,
                "description": "New critical vulnerability discovered"
            },
            {
                "name": "threat_intelligence_improvement",
                "threat_intelligence_quality": "high",
                "description": "Improved threat intelligence available"
            }
        ]
        
        # Use the first game model for scenario analysis
        if game_results:
            base_game_model = framework.game_theory.create_game_model(
                attack_trees[0], attacker_profiles[1], defender_profile
            )
            
            scenario_analysis = framework.game_theory.analyze_strategic_interactions(
                base_game_model, scenarios
            )
            
            print(f"Scenario Analysis Results:")
            for scenario_result in scenario_analysis['scenario_analysis']:
                print(f"\nScenario: {scenario_result['scenario_name']}")
                print(f"  Description: {scenario_result['scenario_parameters'].get('description', 'N/A')}")
                print(f"  Optimal attacker strategy: {scenario_result['optimal_attacker_strategy']}")
                print(f"  Optimal defender strategy: {scenario_result['optimal_defender_strategy']}")
                print(f"  Attack success probability: {scenario_result['attack_success_probability']:.3f}")
                print(f"  Expected defender payoff: {scenario_result['expected_defender_payoff']:.0f}")
            
            # Show scenario summary
            summary = scenario_analysis['summary']
            print(f"\nScenario Summary:")
            print(f"  Average attack success probability: {summary['average_attack_success_probability']:.3f}")
            print(f"  Average defender payoff: {summary['average_defender_payoff']:.0f}")
            print(f"  Best scenario: {summary['best_defender_scenario']}")
            print(f"  Worst scenario: {summary['worst_defender_scenario']}")
            
            print(f"\nRecommendations:")
            for rec in summary['recommendations']:
                print(f"  - {rec}")
        
        # Step 6: Generate comprehensive recommendations
        print(f"\nStep 6: Generating comprehensive recommendations...")
        
        # Create comprehensive analysis result
        from tara_framework.core.models import AnalysisResult, Recommendation
        
        recommendations = []
        
        # Asset-based recommendations
        for asset in tara_results['high_risk_assets']:
            rec = Recommendation(
                title=f"Secure {asset.name}",
                description=f"Implement comprehensive security controls for {asset.name}",
                priority="high",
                category="asset_security",
                estimated_cost=75000,
                effectiveness_score=0.85,
                implementation_time="4-6 months",
                associated_risks=[asset.asset_id],
                prerequisites=["security_team", "budget_approval", "stakeholder_buy_in"],
                countermeasures=["encryption", "access_control", "monitoring", "incident_response"]
            )
            recommendations.append(rec)
        
        # Risk-based recommendations
        for risk in tara_results['critical_risks']:
            rec = Recommendation(
                title=f"Mitigate {risk.threat.name}",
                description=f"Address critical risk: {risk.threat.name}",
                priority="critical",
                category="risk_mitigation",
                estimated_cost=150000,
                effectiveness_score=0.90,
                implementation_time="2-4 months",
                associated_risks=[risk.risk_id],
                prerequisites=["immediate_action", "executive_approval", "emergency_budget"],
                countermeasures=["patch_management", "incident_response", "security_monitoring", "threat_hunting"]
            )
            recommendations.append(rec)
        
        # Game theory-based recommendations
        for game_result in game_results:
            if game_result.attack_success_probability > 0.6:
                rec = Recommendation(
                    title="Improve Strategic Defense",
                    description=f"Current defense allows {game_result.attack_success_probability:.1%} attack success",
                    priority="high",
                    category="strategic_defense",
                    estimated_cost=200000,
                    effectiveness_score=0.80,
                    implementation_time="6-12 months",
                    associated_risks=["strategic_risk"],
                    prerequisites=["strategy_review", "budget_allocation", "stakeholder_alignment"],
                    countermeasures=["defense_in_depth", "threat_intelligence", "incident_response", "red_team_exercises"]
                )
                recommendations.append(rec)
        
        # Create final analysis result
        final_result = AnalysisResult(
            asset_inventory=tara_results['assets'],
            threat_assessment=tara_results['threats'],
            risk_assessment=tara_results['risk_assessments'],
            attack_trees=attack_trees,
            game_theory_results=game_results,
            recommendations=recommendations,
            analysis_metadata={
                "scope": system_definition['scope'],
                "analysis_type": "advanced_comprehensive",
                "timestamp": "2024-01-01T00:00:00",
                "framework_version": "1.0",
                "scenarios_analyzed": len(scenarios)
            }
        )
        
        # Display final recommendations
        print(f"\nFinal Recommendations ({len(recommendations)}):")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec.title}")
            print(f"   Priority: {rec.priority}")
            print(f"   Category: {rec.category}")
            print(f"   Cost: ${rec.estimated_cost:,}")
            print(f"   Effectiveness: {rec.effectiveness_score:.2f}")
            print(f"   Time: {rec.implementation_time}")
            print(f"   Prerequisites: {', '.join(rec.prerequisites)}")
            print()
        
        # Export comprehensive results
        print(f"Exporting comprehensive results...")
        json_file = framework.export_results(final_result, "json")
        xml_file = framework.export_results(final_result, "xml")
        pdf_file = framework.export_results(final_result, "pdf")
        
        print(f"Results exported to:")
        print(f"- JSON: {json_file}")
        print(f"- XML: {xml_file}")
        print(f"- PDF: {pdf_file}")
        
        # Generate executive summary
        print(f"\nGenerating executive summary...")
        summary = framework.generate_executive_summary(final_result)
        
        print(f"\nExecutive Summary:")
        print(f"Key Findings:")
        for finding in summary.key_findings:
            print(f"- {finding}")
        
        print(f"\nRisk Overview: {summary.risk_overview}")
        
        print(f"\nCritical Risks:")
        for risk in summary.critical_risks:
            print(f"- {risk}")
        
        print(f"\nInvestment Priorities:")
        for priority in summary.investment_priorities:
            print(f"- {priority}")
        
        print(f"\nAdvanced analysis completed successfully!")
        
    except Exception as e:
        print(f"Advanced analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())