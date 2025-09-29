"""
Game Theory component implementation.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    # Fallback for basic operations without numpy
    class np:
        @staticmethod
        def zeros(shape):
            if len(shape) == 2:
                return [[0.0 for _ in range(shape[1])] for _ in range(shape[0])]
            return [0.0 for _ in range(shape[0])]
        
        @staticmethod
        def argmax(arr):
            if isinstance(arr[0], list):
                return [max(range(len(row)), key=lambda i: row[i]) for row in arr]
            return max(range(len(arr)), key=lambda i: arr[i])
        
        @staticmethod
        def mean(arr):
            return sum(arr) / len(arr) if arr else 0.0

from ..core.models import (
    AttackTree, AttackerProfile, DefenderProfile, GameModel, PayoffMatrix,
    EquilibriumResult
)
from ..core.exceptions import GameTheoryAnalysisError


class GameTheoryComponent:
    """Game Theory component for strategic interaction analysis."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Game Theory component with configuration."""
        self.config = config or {}
        self.equilibrium_concept = self.config.get("equilibrium_concept", "nash")
        self.information_set = self.config.get("information_set", "incomplete")
        self.sensitivity_analysis = self.config.get("sensitivity_analysis", True)
        
        # Default payoff calculation parameters
        self.payoff_parameters = {
            "attacker_success_reward": 100000,
            "attacker_failure_cost": 50000,
            "defender_success_reward": 50000,
            "defender_failure_cost": 100000,
            "detection_penalty": 25000,
            "countermeasure_cost": 10000
        }
    
    def create_attacker_profile(self, profile_data: Dict[str, Any]) -> AttackerProfile:
        """
        Create an attacker profile for game theory analysis.
        
        Args:
            profile_data: Attacker characteristics and capabilities
            
        Returns:
            Structured attacker profile
        """
        try:
            return AttackerProfile(
                name=profile_data.get("name", "Unknown Attacker"),
                skill_level=profile_data.get("skill_level", "medium"),
                resources=profile_data.get("resources", "moderate"),
                motivation=profile_data.get("motivation", "financial_gain"),
                risk_tolerance=profile_data.get("risk_tolerance", "medium"),
                time_horizon=profile_data.get("time_horizon", "short_term"),
                capabilities=profile_data.get("capabilities", []),
                budget=profile_data.get("budget", 0),
                team_size=profile_data.get("team_size", 1),
                attack_preferences=profile_data.get("attack_preferences", [])
            )
        except Exception as e:
            raise GameTheoryAnalysisError(f"Failed to create attacker profile: {str(e)}")
    
    def create_defender_profile(self, profile_data: Dict[str, Any]) -> DefenderProfile:
        """
        Create a defender profile for game theory analysis.
        
        Args:
            profile_data: Defender characteristics and capabilities
            
        Returns:
            Structured defender profile
        """
        try:
            return DefenderProfile(
                name=profile_data.get("name", "Organization"),
                budget=profile_data.get("budget", 1000000),
                expertise_level=profile_data.get("expertise_level", "high"),
                response_time=profile_data.get("response_time", "fast"),
                available_countermeasures=profile_data.get("available_countermeasures", []),
                risk_tolerance=profile_data.get("risk_tolerance", "low"),
                compliance_requirements=profile_data.get("compliance_requirements", []),
                organizational_capabilities=profile_data.get("organizational_capabilities", [])
            )
        except Exception as e:
            raise GameTheoryAnalysisError(f"Failed to create defender profile: {str(e)}")
    
    def create_game_model(self, attack_tree: AttackTree, attacker: AttackerProfile, 
                         defender: DefenderProfile) -> GameModel:
        """
        Create a game theory model for the given attack tree and player profiles.
        
        Args:
            attack_tree: Attack tree to model
            attacker: Attacker profile
            defender: Defender profile
            
        Returns:
            Game theory model ready for analysis
        """
        try:
            # Determine game type based on attack tree structure
            game_type = self._determine_game_type(attack_tree)
            
            # Create payoff matrix
            payoff_matrix = self._create_payoff_matrix(attack_tree, attacker, defender)
            
            return GameModel(
                attack_tree=attack_tree,
                attacker=attacker,
                defender=defender,
                game_type=game_type,
                information_set=self.information_set,
                equilibrium_concept=self.equilibrium_concept,
                payoff_matrix=payoff_matrix
            )
        except Exception as e:
            raise GameTheoryAnalysisError(f"Failed to create game model: {str(e)}")
    
    def _determine_game_type(self, attack_tree: AttackTree) -> str:
        """Determine the appropriate game type based on attack tree structure."""
        if len(attack_tree.attack_paths) > 5:
            return "sequential"
        elif len(attack_tree.leaf_nodes) > 10:
            return "repeated"
        else:
            return "simultaneous"
    
    def _create_payoff_matrix(self, attack_tree: AttackTree, attacker: AttackerProfile, 
                            defender: DefenderProfile) -> PayoffMatrix:
        """Create payoff matrix for the game."""
        # Define strategies
        attacker_strategies = self._get_attacker_strategies(attack_tree, attacker)
        defender_strategies = self._get_defender_strategies(attack_tree, defender)
        
        # Calculate payoffs for each strategy combination
        payoffs = {}
        for attacker_strategy in attacker_strategies:
            for defender_strategy in defender_strategies:
                key = (attacker_strategy, defender_strategy)
                payoffs[key] = self._calculate_payoffs(
                    attacker_strategy, defender_strategy, attack_tree, attacker, defender
                )
        
        return PayoffMatrix(
            attacker_strategies=attacker_strategies,
            defender_strategies=defender_strategies,
            payoffs=payoffs
        )
    
    def _get_attacker_strategies(self, attack_tree: AttackTree, attacker: AttackerProfile) -> List[str]:
        """Get available attacker strategies."""
        strategies = []
        
        # Add strategies based on attack paths
        for i, path in enumerate(attack_tree.attack_paths[:3]):  # Limit to top 3 paths
            strategies.append(f"attack_path_{i+1}")
        
        # Add no-attack strategy
        strategies.append("no_attack")
        
        return strategies
    
    def _get_defender_strategies(self, attack_tree: AttackTree, defender: DefenderProfile) -> List[str]:
        """Get available defender strategies."""
        strategies = []
        
        # Add countermeasure strategies
        if "encryption" in defender.available_countermeasures:
            strategies.append("deploy_encryption")
        
        if "authentication" in defender.available_countermeasures:
            strategies.append("deploy_authentication")
        
        if "monitoring" in defender.available_countermeasures:
            strategies.append("deploy_monitoring")
        
        # Add combined strategy
        if len(defender.available_countermeasures) > 1:
            strategies.append("deploy_all_countermeasures")
        
        # Add no-action strategy
        strategies.append("no_action")
        
        return strategies
    
    def _calculate_payoffs(self, attacker_strategy: str, defender_strategy: str,
                          attack_tree: AttackTree, attacker: AttackerProfile, 
                          defender: DefenderProfile) -> Dict[str, float]:
        """Calculate payoffs for a strategy combination."""
        # Base payoffs
        attacker_payoff = 0.0
        defender_payoff = 0.0
        
        if attacker_strategy == "no_attack":
            # No attack - no payoffs
            return {"attacker_payoff": 0.0, "defender_payoff": 0.0}
        
        # Get attack path for attacker strategy
        path_index = int(attacker_strategy.split("_")[-1]) - 1
        if path_index < len(attack_tree.attack_paths):
            attack_path = attack_tree.attack_paths[path_index]
            
            # Calculate success probability
            success_prob = attack_path.success_probability
            detection_prob = attack_path.detection_probability
            
            # Adjust based on defender strategy
            if defender_strategy != "no_action":
                success_prob *= 0.5  # Reduce success probability
                detection_prob *= 1.5  # Increase detection probability
            
            # Calculate attacker payoff
            if success_prob > 0.5:  # Successful attack
                attacker_payoff = self.payoff_parameters["attacker_success_reward"] * success_prob
                if detection_prob > 0.3:
                    attacker_payoff -= self.payoff_parameters["detection_penalty"] * detection_prob
            else:  # Failed attack
                attacker_payoff = -self.payoff_parameters["attacker_failure_cost"] * (1 - success_prob)
            
            # Calculate defender payoff
            if success_prob > 0.5:  # Attack successful
                defender_payoff = -self.payoff_parameters["defender_failure_cost"] * success_prob
            else:  # Attack failed
                defender_payoff = self.payoff_parameters["defender_success_reward"] * (1 - success_prob)
            
            # Subtract countermeasure costs
            if defender_strategy != "no_action":
                defender_payoff -= self.payoff_parameters["countermeasure_cost"]
        
        return {
            "attacker_payoff": attacker_payoff,
            "defender_payoff": defender_payoff
        }
    
    def calculate_payoffs(self, game_model: GameModel, strategies: Dict[str, List[str]]) -> PayoffMatrix:
        """
        Calculate payoffs for different strategy combinations.
        
        Args:
            game_model: Game model to analyze
            strategies: Strategy combinations to evaluate
            
        Returns:
            Payoff matrix for all strategy combinations
        """
        try:
            # Use provided strategies or default from game model
            attacker_strategies = strategies.get("attacker", game_model.payoff_matrix.attacker_strategies)
            defender_strategies = strategies.get("defender", game_model.payoff_matrix.defender_strategies)
            
            # Calculate payoffs
            payoffs = {}
            for attacker_strategy in attacker_strategies:
                for defender_strategy in defender_strategies:
                    key = (attacker_strategy, defender_strategy)
                    payoffs[key] = self._calculate_payoffs(
                        attacker_strategy, defender_strategy,
                        game_model.attack_tree, game_model.attacker, game_model.defender
                    )
            
            return PayoffMatrix(
                attacker_strategies=attacker_strategies,
                defender_strategies=defender_strategies,
                payoffs=payoffs
            )
        except Exception as e:
            raise GameTheoryAnalysisError(f"Failed to calculate payoffs: {str(e)}")
    
    def find_nash_equilibrium(self, game_model: GameModel) -> EquilibriumResult:
        """
        Find Nash equilibrium for the game model.
        
        Args:
            game_model: Game model to analyze
            
        Returns:
            Nash equilibrium solution
        """
        try:
            payoff_matrix = game_model.payoff_matrix
            
            # Convert to arrays for analysis
            attacker_payoffs = np.zeros((len(payoff_matrix.attacker_strategies), 
                                       len(payoff_matrix.defender_strategies)))
            defender_payoffs = np.zeros((len(payoff_matrix.attacker_strategies), 
                                       len(payoff_matrix.defender_strategies)))
            
            for i, attacker_strategy in enumerate(payoff_matrix.attacker_strategies):
                for j, defender_strategy in enumerate(payoff_matrix.defender_strategies):
                    payoffs = payoff_matrix.get_payoff(attacker_strategy, defender_strategy)
                    attacker_payoffs[i][j] = payoffs["attacker_payoff"]
                    defender_payoffs[i][j] = payoffs["defender_payoff"]
            
            # Find Nash equilibrium
            equilibrium = self._find_nash_equilibrium_numerical(attacker_payoffs, defender_payoffs)
            
            # Get equilibrium strategies
            attacker_strategy = payoff_matrix.attacker_strategies[equilibrium["attacker_strategy"]]
            defender_strategy = payoff_matrix.defender_strategies[equilibrium["defender_strategy"]]
            
            # Get equilibrium payoffs
            equilibrium_payoffs = payoff_matrix.get_payoff(attacker_strategy, defender_strategy)
            
            # Calculate stability
            stability = self._calculate_equilibrium_stability(
                equilibrium, attacker_payoffs, defender_payoffs
            )
            
            # Determine expected outcome
            expected_outcome = self._determine_expected_outcome(
                attacker_strategy, defender_strategy, game_model
            )
            
            # Calculate attack success probability
            attack_success_probability = self._calculate_attack_success_probability(
                attacker_strategy, defender_strategy, game_model
            )
            
            return EquilibriumResult(
                equilibrium_type="nash",
                attacker_strategy=attacker_strategy,
                defender_strategy=defender_strategy,
                attacker_payoff=equilibrium_payoffs["attacker_payoff"],
                defender_payoff=equilibrium_payoffs["defender_payoff"],
                stability=stability,
                expected_outcome=expected_outcome,
                attack_success_probability=attack_success_probability
            )
        except Exception as e:
            raise GameTheoryAnalysisError(f"Failed to find Nash equilibrium: {str(e)}")
    
    def _find_nash_equilibrium_numerical(self, attacker_payoffs, 
                                       defender_payoffs) -> Dict[str, int]:
        """Find Nash equilibrium using numerical methods."""
        # Simple best response analysis
        best_responses = {}
        
        # Find best response for each player
        for i in range(len(attacker_payoffs)):
            best_defender_response = np.argmax(defender_payoffs[i])
            best_responses[f"attacker_{i}"] = best_defender_response
        
        for j in range(len(defender_payoffs[0])):
            best_attacker_response = np.argmax([row[j] for row in attacker_payoffs])
            best_responses[f"defender_{j}"] = best_attacker_response
        
        # Find Nash equilibrium (where both players' best responses align)
        for i in range(len(attacker_payoffs)):
            for j in range(len(defender_payoffs[0])):
                if (best_responses[f"attacker_{i}"] == j and 
                    best_responses[f"defender_{j}"] == i):
                    return {"attacker_strategy": i, "defender_strategy": j}
        
        # If no pure strategy equilibrium, return mixed strategy approximation
        return {"attacker_strategy": 0, "defender_strategy": 0}
    
    def _calculate_equilibrium_stability(self, equilibrium: Dict[str, int], 
                                       attacker_payoffs, 
                                       defender_payoffs) -> float:
        """Calculate equilibrium stability."""
        i, j = equilibrium["attacker_strategy"], equilibrium["defender_strategy"]
        
        # Calculate how much better the equilibrium is compared to alternatives
        attacker_equilibrium_payoff = attacker_payoffs[i][j]
        defender_equilibrium_payoff = defender_payoffs[i][j]
        
        # Check if either player has incentive to deviate
        attacker_best_alternative = max([row[j] for row in attacker_payoffs])
        defender_best_alternative = max(defender_payoffs[i])
        
        attacker_incentive = attacker_best_alternative - attacker_equilibrium_payoff
        defender_incentive = defender_best_alternative - defender_equilibrium_payoff
        
        # Stability is inverse of incentive to deviate
        stability = 1.0 / (1.0 + abs(attacker_incentive) + abs(defender_incentive))
        
        return min(stability, 1.0)
    
    def _determine_expected_outcome(self, attacker_strategy: str, defender_strategy: str, 
                                  game_model: GameModel) -> str:
        """Determine expected outcome of the equilibrium."""
        if attacker_strategy == "no_attack":
            return "No attack - system remains secure"
        
        # Get attack path
        if "attack_path" in attacker_strategy:
            path_index = int(attacker_strategy.split("_")[-1]) - 1
            if path_index < len(game_model.attack_tree.attack_paths):
                attack_path = game_model.attack_tree.attack_paths[path_index]
                
                if defender_strategy == "no_action":
                    if attack_path.success_probability > 0.7:
                        return "Attack likely to succeed - system compromised"
                    else:
                        return "Attack may succeed - system at risk"
                else:
                    if attack_path.success_probability > 0.5:
                        return "Attack may succeed despite defenses"
                    else:
                        return "Defenses effective - attack likely to fail"
        
        return "Uncertain outcome"
    
    def _calculate_attack_success_probability(self, attacker_strategy: str, defender_strategy: str, 
                                            game_model: GameModel) -> float:
        """Calculate attack success probability for the equilibrium."""
        if attacker_strategy == "no_attack":
            return 0.0
        
        # Get attack path
        if "attack_path" in attacker_strategy:
            path_index = int(attacker_strategy.split("_")[-1]) - 1
            if path_index < len(game_model.attack_tree.attack_paths):
                attack_path = game_model.attack_tree.attack_paths[path_index]
                
                # Adjust based on defender strategy
                success_prob = attack_path.success_probability
                if defender_strategy != "no_action":
                    success_prob *= 0.5  # Reduce success probability
                
                return success_prob
        
        return 0.0
    
    def analyze_strategic_interactions(self, game_model: GameModel, 
                                     scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze strategic interactions under different scenarios.
        
        Args:
            game_model: Game model to analyze
            scenarios: Different scenarios to evaluate
            
        Returns:
            Analysis results for all scenarios
        """
        try:
            scenario_results = []
            
            for scenario in scenarios:
                # Create modified game model for scenario
                modified_model = self._create_scenario_model(game_model, scenario)
                
                # Find equilibrium for scenario
                equilibrium = self.find_nash_equilibrium(modified_model)
                
                # Analyze scenario
                scenario_result = {
                    "scenario_name": scenario.get("name", "Unknown Scenario"),
                    "scenario_parameters": scenario,
                    "optimal_attacker_strategy": equilibrium.attacker_strategy,
                    "optimal_defender_strategy": equilibrium.defender_strategy,
                    "expected_attacker_payoff": equilibrium.attacker_payoff,
                    "expected_defender_payoff": equilibrium.defender_payoff,
                    "attack_success_probability": equilibrium.attack_success_probability,
                    "equilibrium_stability": equilibrium.stability,
                    "expected_outcome": equilibrium.expected_outcome
                }
                
                scenario_results.append(scenario_result)
            
            return {
                "scenario_analysis": scenario_results,
                "total_scenarios": len(scenario_results),
                "summary": self._summarize_scenario_analysis(scenario_results)
            }
        except Exception as e:
            raise GameTheoryAnalysisError(f"Failed to analyze strategic interactions: {str(e)}")
    
    def _create_scenario_model(self, base_model: GameModel, scenario: Dict[str, Any]) -> GameModel:
        """Create a modified game model for a specific scenario."""
        # Create copies of profiles
        attacker = AttackerProfile(
            name=base_model.attacker.name,
            skill_level=base_model.attacker.skill_level,
            resources=base_model.attacker.resources,
            motivation=base_model.attacker.motivation,
            risk_tolerance=base_model.attacker.risk_tolerance,
            time_horizon=base_model.attacker.time_horizon,
            capabilities=base_model.attacker.capabilities,
            budget=base_model.attacker.budget,
            team_size=base_model.attacker.team_size,
            attack_preferences=base_model.attacker.attack_preferences
        )
        
        defender = DefenderProfile(
            name=base_model.defender.name,
            budget=base_model.defender.budget,
            expertise_level=base_model.defender.expertise_level,
            response_time=base_model.defender.response_time,
            available_countermeasures=base_model.defender.available_countermeasures,
            risk_tolerance=base_model.defender.risk_tolerance,
            compliance_requirements=base_model.defender.compliance_requirements,
            organizational_capabilities=base_model.defender.organizational_capabilities
        )
        
        # Apply scenario modifications
        if "budget_increase" in scenario:
            defender.budget *= (1 + scenario["budget_increase"])
        
        if "budget_decrease" in scenario:
            defender.budget *= (1 - scenario["budget_decrease"])
        
        if "new_vulnerability" in scenario:
            # Add new countermeasure
            defender.available_countermeasures.append("new_vulnerability_patch")
        
        # Create new game model
        return GameModel(
            attack_tree=base_model.attack_tree,
            attacker=attacker,
            defender=defender,
            game_type=base_model.game_type,
            information_set=base_model.information_set,
            equilibrium_concept=base_model.equilibrium_concept
        )
    
    def _summarize_scenario_analysis(self, scenario_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize scenario analysis results."""
        if not scenario_results:
            return {}
        
        # Calculate averages
        avg_attacker_payoff = np.mean([r["expected_attacker_payoff"] for r in scenario_results])
        avg_defender_payoff = np.mean([r["expected_defender_payoff"] for r in scenario_results])
        avg_attack_success_prob = np.mean([r["attack_success_probability"] for r in scenario_results])
        avg_stability = np.mean([r["equilibrium_stability"] for r in scenario_results])
        
        # Find best and worst scenarios
        best_defender_scenario = max(scenario_results, key=lambda x: x["expected_defender_payoff"])
        worst_defender_scenario = min(scenario_results, key=lambda x: x["expected_defender_payoff"])
        
        return {
            "average_attacker_payoff": avg_attacker_payoff,
            "average_defender_payoff": avg_defender_payoff,
            "average_attack_success_probability": avg_attack_success_prob,
            "average_equilibrium_stability": avg_stability,
            "best_defender_scenario": best_defender_scenario["scenario_name"],
            "worst_defender_scenario": worst_defender_scenario["scenario_name"],
            "recommendations": self._generate_scenario_recommendations(scenario_results)
        }
    
    def _generate_scenario_recommendations(self, scenario_results: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on scenario analysis."""
        recommendations = []
        
        # Analyze attack success probabilities
        high_success_scenarios = [r for r in scenario_results if r["attack_success_probability"] > 0.7]
        if high_success_scenarios:
            recommendations.append("Implement additional countermeasures to reduce attack success probability")
        
        # Analyze defender payoffs
        low_payoff_scenarios = [r for r in scenario_results if r["expected_defender_payoff"] < 0]
        if low_payoff_scenarios:
            recommendations.append("Consider increasing security budget to improve defender outcomes")
        
        # Analyze stability
        unstable_scenarios = [r for r in scenario_results if r["equilibrium_stability"] < 0.5]
        if unstable_scenarios:
            recommendations.append("Focus on strategies that lead to more stable equilibria")
        
        return recommendations