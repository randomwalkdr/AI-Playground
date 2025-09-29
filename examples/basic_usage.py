#!/usr/bin/env python3
"""
Basic usage example for the TARA framework.
This example demonstrates how to use the framework for a simple automotive cybersecurity analysis.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tara_framework import TARAFramework


def main():
    """Run a basic TARA analysis example."""
    print("TARA Framework - Basic Usage Example")
    print("=" * 50)
    
    # Initialize the framework
    framework = TARAFramework(
        scope="telematics_ecu",
        analysis_type="comprehensive",
        output_format="structured"
    )
    
    # Configure basic parameters
    framework.configure(
        risk_tolerance="medium",
        analysis_depth="detailed",
        game_theory_model="nash_equilibrium"
    )
    
    # Define system for analysis
    system_definition = {
        "scope": {
            "boundaries": "telematics_ecu",
            "focus_areas": ["communication", "data_storage", "authentication"],
            "exclusions": ["mechanical_components"]
        },
        "asset_types": ["physical", "software", "data", "function"],
        "threat_intelligence": {
            "threat_actors": ["script_kiddies", "organized_crime", "state_actors"],
            "attack_vectors": ["wireless", "physical", "supply_chain"],
            "motivations": ["financial", "espionage", "disruption"]
        },
        "asset_valuation_criteria": {
            "weights": {
                "safety": 0.4,
                "financial": 0.3,
                "operational": 0.2,
                "privacy": 0.1
            }
        },
        "assets": [],  # Will be populated by TARA analysis
        "threats": []  # Will be populated by TARA analysis
    }
    
    try:
        # Run comprehensive analysis
        print("Running comprehensive analysis...")
        result = framework.run_comprehensive_analysis(system_definition)
        
        # Display results summary
        print(f"\nAnalysis Results Summary:")
        print(f"Assets analyzed: {len(result.asset_inventory)}")
        print(f"Threats identified: {len(result.threat_assessment)}")
        print(f"Attack trees constructed: {len(result.attack_trees)}")
        print(f"Game theory models: {len(result.game_theory_results)}")
        print(f"Recommendations: {len(result.recommendations)}")
        
        # Show asset inventory
        print(f"\nAsset Inventory:")
        for asset in result.asset_inventory:
            print(f"- {asset.name} ({asset.asset_type.value}): Value {asset.value}")
        
        # Show high-risk assets
        high_risk_assets = [asset for asset in result.asset_inventory if asset.value >= 7.0]
        print(f"\nHigh-Risk Assets ({len(high_risk_assets)}):")
        for asset in high_risk_assets:
            print(f"- {asset.name}: {asset.get_total_impact():.1f} total impact")
        
        # Show critical risks
        critical_risks = [risk for risk in result.risk_assessment if risk.risk_level.value == 'critical']
        print(f"\nCritical Risks ({len(critical_risks)}):")
        for risk in critical_risks:
            print(f"- {risk.threat.name}: {risk.risk_score:.2f} risk score")
        
        # Show attack trees
        print(f"\nAttack Trees:")
        for tree in result.attack_trees:
            print(f"- {tree.root_node.name}: {len(tree.attack_paths)} attack paths")
            
            # Show most feasible path
            if tree.attack_paths:
                most_feasible = max(tree.attack_paths, key=lambda p: p.feasibility_score)
                print(f"  Most feasible path: {most_feasible.feasibility_score:.2f} feasibility")
        
        # Show game theory results
        print(f"\nGame Theory Results:")
        for i, game_result in enumerate(result.game_theory_results):
            print(f"- Scenario {i+1}:")
            print(f"  Attacker strategy: {game_result.attacker_strategy}")
            print(f"  Defender strategy: {game_result.defender_strategy}")
            print(f"  Attack success probability: {game_result.attack_success_probability:.2f}")
            print(f"  Equilibrium stability: {game_result.stability:.2f}")
        
        # Show top recommendations
        print(f"\nTop Recommendations:")
        for i, rec in enumerate(result.recommendations[:5], 1):
            print(f"{i}. {rec.title}")
            print(f"   Priority: {rec.priority}")
            print(f"   Cost: ${rec.estimated_cost:,}")
            print(f"   Effectiveness: {rec.effectiveness_score:.2f}")
            print(f"   Time: {rec.implementation_time}")
            print()
        
        # Generate executive summary
        print("Generating executive summary...")
        summary = framework.generate_executive_summary(result)
        
        print(f"\nExecutive Summary:")
        print(f"Key Findings:")
        for finding in summary.key_findings:
            print(f"- {finding}")
        
        print(f"\nRisk Overview: {summary.risk_overview}")
        
        print(f"\nTop Recommendations:")
        for rec in summary.recommendations:
            print(f"- {rec}")
        
        print(f"\nInvestment Priorities:")
        for priority in summary.investment_priorities:
            print(f"- {priority}")
        
        # Export results
        print(f"\nExporting results...")
        json_file = framework.export_results(result, "json")
        pdf_file = framework.export_results(result, "pdf")
        
        print(f"Results exported to:")
        print(f"- JSON: {json_file}")
        print(f"- PDF: {pdf_file}")
        
        print(f"\nAnalysis completed successfully!")
        
    except Exception as e:
        print(f"Analysis failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())