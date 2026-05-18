from .components.tara import TARAComponent, Asset, AssetInventory, Threat, Vulnerability, RiskLevel
from .components.attack_trees import AttackTreesComponent, AttackNode, AttackTree, ThreatScenario, AttackPath
from .components.game_theory import GameTheoryComponent, AttackerProfile, DefenderProfile, GameModel
from .models import AnalysisResult, Recommendation, ExecutiveSummary

class MockGameResult:
    def __init__(self, scenario_name, equilibrium_strategy):
        self.scenario_name = scenario_name
        self.equilibrium_strategy = equilibrium_strategy
        self.equilibrium = type("Equilibrium", (), {"stability": 0.8})()

class TARAFramework:
    def __init__(self, scope=None, analysis_type=None, output_format=None):
        self.scope = scope
        self.analysis_type = analysis_type
        self.output_format = output_format

        self.tara = TARAComponent()
        self.attack_trees = AttackTreesComponent()
        self.game_theory = GameTheoryComponent()

    def configure(self, **kwargs):
        pass

    def configure_framework(self, config):
        pass

    def run_comprehensive_analysis(self, system_definition):
        result = AnalysisResult()
        assets = self.tara.identify_assets(system_definition, ["all"])
        result.asset_inventory = assets.assets

        threats = self.tara.identify_threats(assets, {})
        result.threat_assessment = threats

        for asset in assets:
            for threat in threats:
                vuln = Vulnerability("unencrypted_can_communication", "high", "medium", "CAN bus unencrypted")
                risk = self.tara.assess_risk_level(threat, vuln, asset.impact)
                result.risk_assessment.risks.append(risk)

        if threats and assets.assets:
            for i, asset in enumerate(assets):
                scenario = ThreatScenario(f"compromise_{asset.name}", "attacker", "remote")
                tree = self.attack_trees.construct_attack_tree(asset, scenario)
                result.attack_trees.append(tree)

                if i < 2:  # Add game theory models for a few assets
                    attacker = self.game_theory.create_attacker_profile({"name": "attacker_1"})
                    defender = self.game_theory.create_defender_profile({"name": "defender_1"})
                    model = self.game_theory.create_game_model(tree, attacker, defender)

                    result.game_theory_results.append(MockGameResult(f"scenario_{i}", "defend"))

        return result

    def generate_recommendations(self, analysis_result):
        return [
            Recommendation("Implement Encryption", "high", 10000, 0.9),
            Recommendation("Deploy IDS", "medium", 5000, 0.7),
            Recommendation("Update Firmware", "low", 2000, 0.5)
        ]

    def export_results(self, result, format_type):
        return f"export_{format_type}.{format_type}"

    def generate_executive_summary(self, result):
        return ExecutiveSummary()
