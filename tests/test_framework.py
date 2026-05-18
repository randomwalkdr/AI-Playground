import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tara_framework import TARAFramework
from tara_framework import ThreatScenario, Vulnerability

class TestTARAFramework(unittest.TestCase):
    def setUp(self):
        self.framework = TARAFramework(
            scope="telematics_ecu",
            analysis_type="comprehensive",
            output_format="structured"
        )
        self.framework.configure(
            risk_tolerance="medium",
            analysis_depth="detailed",
            game_theory_model="nash_equilibrium"
        )

    def test_quick_start(self):
        system_definition = {
            "scope": "telematics_ecu",
            "assets": ["firmware", "communication_stack", "user_data"],
            "threats": ["remote_exploitation", "physical_tampering"],
            "analysis_depth": "basic"
        }
        result = self.framework.run_comprehensive_analysis(system_definition)
        self.assertTrue(len(result.risk_assessment.risks) > 0)

    def test_tara_component(self):
        ecu_scope = {
            "boundaries": "powertrain_ecu",
            "focus_areas": ["engine_control", "transmission_control", "safety_systems"],
            "exclusions": ["mechanical_components", "external_sensors"]
        }
        assets = self.framework.tara.identify_assets(
            system_scope=ecu_scope,
            asset_types=["physical", "software", "data", "functions"]
        )
        self.assertEqual(len(assets), 5)

        threat_intel = {
            "threat_actors": [{"name": "script_kiddies", "skill_level": "low"}]
        }
        threats = self.framework.tara.identify_threats(assets, threat_intel)
        self.assertEqual(len(threats), 3)

        threat = threats[0]
        asset = assets[0]
        vulnerability = Vulnerability("unencrypted_can", "high", "medium", "desc")
        risk = self.framework.tara.assess_risk_level(threat, vulnerability, asset.impact)
        self.assertEqual(risk.level, "high")
        self.assertEqual(risk.score, 8.5)

    def test_update_attack_paths(self):
        assets = self.framework.tara.identify_assets({"boundaries": "powertrain_ecu"}, [])
        target_asset = assets.get_asset("powertrain_ecu")
        threat_scenario = ThreatScenario(
            goal="compromise_powertrain_ecu",
            attacker_profile="skilled_insider",
            attack_vector="remote_exploitation"
        )
        tree = self.framework.attack_trees.construct_attack_tree(target_asset, threat_scenario)

        # Adding a new node
        parent_node = tree.find_node("gain_physical_access")
        node_data = {
            "name": "exploit_cve_2023",
            "type": "leaf",
            "difficulty": "medium",
            "cost": 5000
        }
        self.framework.attack_trees.add_attack_node(tree, parent_node, node_data)

        tree.update_attack_paths()

        self.assertEqual(len(tree.attack_paths), 2)
        path_names = [[n.name for n in p.nodes] for p in tree.attack_paths]

        expected_path1 = ['compromise_powertrain_ecu', 'gain_physical_access', 'exploit_cve_2023']
        expected_path2 = ['compromise_powertrain_ecu', 'exploit_remote_vuln']

        self.assertIn(expected_path1, path_names)
        self.assertIn(expected_path2, path_names)

    def test_attack_trees(self):
        assets = self.framework.tara.identify_assets({"boundaries": "powertrain_ecu"}, [])
        target_asset = assets.get_asset("powertrain_ecu")
        threat_scenario = ThreatScenario(
            goal="compromise_powertrain_ecu",
            attacker_profile="skilled_insider",
            attack_vector="remote_exploitation"
        )

        tree = self.framework.attack_trees.construct_attack_tree(target_asset, threat_scenario)
        self.assertEqual(tree.root_node.name, "compromise_powertrain_ecu")
        self.assertEqual(len(tree.attack_paths), 2)

        node_data = {
            "name": "exploit_cve_2023",
            "type": "leaf",
            "difficulty": "medium",
            "cost": 5000
        }
        parent_node = tree.find_node("gain_physical_access")
        new_node = self.framework.attack_trees.add_attack_node(tree, parent_node, node_data)
        self.assertEqual(new_node.name, "exploit_cve_2023")

        analysis = self.framework.attack_trees.analyze_attack_paths(tree, "feasibility")
        feasible_paths = analysis.get_feasible_paths(0.7)
        self.assertEqual(len(feasible_paths), 2)

        critical_nodes = self.framework.attack_trees.identify_critical_nodes(tree, {})
        self.assertEqual(len(critical_nodes), 1)

    def test_game_theory(self):
        attacker_data = {"name": "org_crime", "skill_level": "advanced"}
        attacker = self.framework.game_theory.create_attacker_profile(attacker_data)
        self.assertEqual(attacker.name, "org_crime")

        defender_data = {"name": "auto_mfg", "budget": 1000000}
        defender = self.framework.game_theory.create_defender_profile(defender_data)
        self.assertEqual(defender.budget, 1000000)

        assets = self.framework.tara.identify_assets({"boundaries": "powertrain_ecu"}, [])
        target_asset = assets.get_asset("powertrain_ecu")
        scenario = ThreatScenario("compromise", "attacker", "remote")
        tree = self.framework.attack_trees.construct_attack_tree(target_asset, scenario)

        game = self.framework.game_theory.create_game_model(tree, attacker, defender)

        strategies = {
            "attacker": ["exploit_known_vulnerability", "no_attack"],
            "defender": ["deploy_all_countermeasures", "no_action"]
        }
        payoffs = self.framework.game_theory.calculate_payoffs(game, strategies)
        self.assertEqual(payoffs.get_payoff("attack", "defend").attacker_payoff, 10)

        equilibrium = self.framework.game_theory.find_nash_equilibrium(game)
        self.assertEqual(equilibrium.attacker_strategy, "exploit_known_vulnerability")

        scenarios = [{"name": "budget_inc", "description": "budget increase"}]
        analysis = self.framework.game_theory.analyze_strategic_interactions(game, scenarios)
        self.assertEqual(len(analysis.scenarios), 1)
        self.assertEqual(analysis.scenarios[0].name, "budget_inc")

    def test_integration(self):
        system_def = {"scope": "auto", "boundaries": "powertrain_ecu"}
        result = self.framework.run_comprehensive_analysis(system_def)

        self.assertEqual(len(result.asset_inventory), 5)
        self.assertTrue(len(result.risk_assessment.risks) > 0)
        self.assertEqual(len(result.attack_trees), 5)
        self.assertEqual(len(result.game_theory_results), 2)

        recommendations = self.framework.generate_recommendations(result)
        self.assertEqual(len(recommendations), 3)
        self.assertEqual(recommendations[0].priority, "high")

        pdf_file = self.framework.export_results(result, "pdf")
        self.assertEqual(pdf_file, "export_pdf.pdf")

        summary = self.framework.generate_executive_summary(result)
        self.assertTrue(len(summary.key_findings) > 0)

if __name__ == '__main__':
    unittest.main()
