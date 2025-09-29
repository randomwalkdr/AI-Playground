#!/usr/bin/env python3
"""
Test script for the TARA framework implementation.
This script verifies that all components work correctly together.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from tara_framework import TARAFramework
        print("✓ TARAFramework imported successfully")
        
        from tara_framework.core.models import Asset, Threat, AttackTree, GameModel
        print("✓ Core models imported successfully")
        
        from tara_framework.components.tara import TARAComponent
        print("✓ TARA component imported successfully")
        
        from tara_framework.components.attack_trees import AttackTreesComponent
        print("✓ Attack Trees component imported successfully")
        
        from tara_framework.components.game_theory import GameTheoryComponent
        print("✓ Game Theory component imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic framework functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from tara_framework import TARAFramework
        
        # Initialize framework
        framework = TARAFramework()
        print("✓ Framework initialized successfully")
        
        # Test TARA component
        tara = framework.tara
        print("✓ TARA component accessible")
        
        # Test Attack Trees component
        attack_trees = framework.attack_trees
        print("✓ Attack Trees component accessible")
        
        # Test Game Theory component
        game_theory = framework.game_theory
        print("✓ Game Theory component accessible")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_simple_analysis():
    """Test a simple analysis workflow."""
    print("\nTesting simple analysis...")
    
    try:
        from tara_framework import TARAFramework
        
        # Initialize framework
        framework = TARAFramework()
        
        # Define simple system
        system_definition = {
            "scope": {
                "boundaries": "test_system",
                "focus_areas": ["communication"],
                "exclusions": []
            },
            "asset_types": ["software"],
            "threat_intelligence": {
                "threat_actors": ["script_kiddies"],
                "attack_vectors": ["wireless"],
                "motivations": ["financial"]
            }
        }
        
        # Run TARA analysis
        tara_results = framework.tara.run_analysis(system_definition)
        print(f"✓ TARA analysis completed: {len(tara_results['assets'])} assets, {len(tara_results['threats'])} threats")
        
        # Test attack tree construction
        if tara_results['high_risk_assets']:
            asset = tara_results['high_risk_assets'][0]
            threat_scenario = {
                "goal": f"compromise_{asset.name.lower()}",
                "attacker_profile": "script_kiddies",
                "attack_vector": "wireless"
            }
            
            tree = framework.attack_trees.construct_attack_tree(asset, threat_scenario)
            print(f"✓ Attack tree constructed: {len(tree.all_nodes)} nodes, {len(tree.attack_paths)} paths")
            
            # Test path analysis
            analysis = framework.attack_trees.analyze_attack_paths(tree, "feasibility")
            print(f"✓ Path analysis completed: {analysis['analysis_type']}")
            
            # Test game theory
            attacker = framework.game_theory.create_attacker_profile({
                "name": "test_attacker",
                "skill_level": "low",
                "resources": "limited",
                "motivation": "financial"
            })
            
            defender = framework.game_theory.create_defender_profile({
                "name": "test_defender",
                "budget": 100000,
                "expertise_level": "medium",
                "response_time": "fast"
            })
            
            game = framework.game_theory.create_game_model(tree, attacker, defender)
            print("✓ Game model created successfully")
            
            equilibrium = framework.game_theory.find_nash_equilibrium(game)
            print(f"✓ Nash equilibrium found: {equilibrium.attacker_strategy} vs {equilibrium.defender_strategy}")
        
        return True
    except Exception as e:
        print(f"✗ Simple analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_export_functionality():
    """Test export functionality."""
    print("\nTesting export functionality...")
    
    try:
        from tara_framework import TARAFramework
        
        # Initialize framework
        framework = TARAFramework()
        
        # Create a simple analysis result
        from tara_framework.core.models import AnalysisResult, Asset, AssetType, Threat, ThreatType
        
        # Create dummy data
        asset = Asset(
            name="Test Asset",
            asset_type=AssetType.SOFTWARE,
            description="Test asset for export",
            location="test_system",
            value=5.0
        )
        
        threat = Threat(
            name="Test Threat",
            threat_type=ThreatType.MALWARE,
            description="Test threat for export",
            likelihood=0.5,
            impact=5.0
        )
        
        result = AnalysisResult(
            asset_inventory=[asset],
            threat_assessment=[threat],
            risk_assessment=[],
            attack_trees=[],
            game_theory_results=[],
            recommendations=[]
        )
        
        # Test JSON export
        json_file = framework.export_results(result, "json")
        print(f"✓ JSON export successful: {json_file}")
        
        # Test PDF export
        pdf_file = framework.export_results(result, "pdf")
        print(f"✓ PDF export successful: {pdf_file}")
        
        # Test executive summary
        summary = framework.generate_executive_summary(result)
        print(f"✓ Executive summary generated: {len(summary.key_findings)} findings")
        
        return True
    except Exception as e:
        print(f"✗ Export functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("TARA Framework Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_simple_analysis,
        test_export_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Framework is working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    exit(main())