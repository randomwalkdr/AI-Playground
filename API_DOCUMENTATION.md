# TARA-Attack Trees-Game Theory Framework API Documentation

## Table of Contents

1. [Framework Overview](#framework-overview)
2. [TARA Component API](#tara-component-api)
3. [Attack Trees Component API](#attack-trees-component-api)
4. [Game Theory Component API](#game-theory-component-api)
5. [Integration API](#integration-api)
6. [Data Models](#data-models)
7. [Error Handling](#error-handling)
8. [Configuration](#configuration)

## Framework Overview

The TARA-Attack Trees-Game Theory framework provides a comprehensive approach to automotive cybersecurity risk analysis through three integrated components:

- **TARA (Threat Analysis and Risk Assessment)**: Asset identification and initial risk assessment
- **Attack Trees**: Detailed attack path modeling
- **Game Theory**: Strategic interaction analysis

### Framework Initialization

```python
# Framework initialization example
from tara_framework import TARAFramework

# Initialize the framework
framework = TARAFramework(
    scope="vehicle_system",
    analysis_type="comprehensive",
    output_format="structured"
)

# Configure analysis parameters
framework.configure(
    risk_tolerance="medium",
    analysis_depth="detailed",
    game_theory_model="nash_equilibrium"
)
```

## TARA Component API

### Asset Identification

#### `identify_assets(system_scope, asset_types)`

Identifies and catalogs critical assets within the defined system scope.

**Parameters:**
- `system_scope` (dict): System boundaries and scope definition
- `asset_types` (list): Types of assets to identify (physical, software, data, functions)

**Returns:**
- `AssetInventory`: Structured inventory of identified assets

**Example:**
```python
# Define system scope
scope = {
    "boundaries": "entire_vehicle",
    "focus_areas": ["powertrain", "infotainment", "telematics"],
    "exclusions": ["mechanical_components"]
}

# Identify assets
assets = framework.tara.identify_assets(
    system_scope=scope,
    asset_types=["physical", "software", "data", "functions"]
)

# Access identified assets
for asset in assets:
    print(f"Asset: {asset.name}, Type: {asset.type}, Value: {asset.value}")
```

#### `assess_asset_value(asset, criteria)`

Assesses the value of an identified asset based on multiple criteria.

**Parameters:**
- `asset` (Asset): Asset object to evaluate
- `criteria` (dict): Valuation criteria (safety, financial, operational, privacy)

**Returns:**
- `AssetValue`: Comprehensive asset valuation

**Example:**
```python
# Define valuation criteria
criteria = {
    "safety_impact": "critical",
    "financial_impact": "high",
    "operational_impact": "medium",
    "privacy_impact": "low"
}

# Assess asset value
value = framework.tara.assess_asset_value(asset, criteria)
print(f"Asset value score: {value.total_score}")
```

### Threat Assessment

#### `identify_threats(assets, threat_intelligence)`

Identifies potential threats targeting the identified assets.

**Parameters:**
- `assets` (AssetInventory): Previously identified assets
- `threat_intelligence` (dict): Threat intelligence data and profiles

**Returns:**
- `ThreatList`: List of identified threats with associated metadata

**Example:**
```python
# Load threat intelligence
threat_intel = {
    "threat_actors": ["script_kiddies", "organized_crime", "state_actors"],
    "attack_vectors": ["wireless", "physical", "supply_chain"],
    "motivations": ["financial", "espionage", "disruption"]
}

# Identify threats
threats = framework.tara.identify_threats(assets, threat_intel)

# Analyze threat characteristics
for threat in threats:
    print(f"Threat: {threat.name}, Likelihood: {threat.likelihood}, Impact: {threat.impact}")
```

#### `assess_risk_level(threat, vulnerability, impact)`

Calculates risk level for a specific threat-vulnerability-impact combination.

**Parameters:**
- `threat` (Threat): Threat object
- `vulnerability` (Vulnerability): Associated vulnerability
- `impact` (Impact): Potential impact assessment

**Returns:**
- `RiskLevel`: Calculated risk level (high, medium, low)

**Example:**
```python
# Assess risk for specific threat
risk = framework.tara.assess_risk_level(threat, vulnerability, impact)
print(f"Risk level: {risk.level}, Score: {risk.score}")

# Get risk justification
print(f"Risk factors: {risk.justification}")
```

## Attack Trees Component API

### Tree Construction

#### `construct_attack_tree(target_asset, threat_scenario)`

Constructs an attack tree for a specific target asset and threat scenario.

**Parameters:**
- `target_asset` (Asset): Target asset for the attack
- `threat_scenario` (ThreatScenario): Specific threat scenario to model

**Returns:**
- `AttackTree`: Structured attack tree with nodes and paths

**Example:**
```python
# Define threat scenario
scenario = ThreatScenario(
    goal="compromise_powertrain_ecu",
    attacker_profile="skilled_insider",
    attack_vector="remote_exploitation"
)

# Construct attack tree
tree = framework.attack_trees.construct_attack_tree(target_asset, scenario)

# Access tree structure
print(f"Root node: {tree.root_node}")
print(f"Leaf nodes: {len(tree.leaf_nodes)}")
print(f"Attack paths: {len(tree.attack_paths)}")
```

#### `add_attack_node(tree, parent_node, node_data)`

Adds a new attack node to an existing attack tree.

**Parameters:**
- `tree` (AttackTree): Target attack tree
- `parent_node` (AttackNode): Parent node for the new node
- `node_data` (dict): Node information (name, type, prerequisites, etc.)

**Returns:**
- `AttackNode`: Newly created attack node

**Example:**
```python
# Define new node data
node_data = {
    "name": "exploit_cve_2023_1234",
    "type": "leaf",
    "prerequisites": ["physical_access", "known_vulnerability"],
    "difficulty": "medium",
    "cost": 5000
}

# Add node to tree
new_node = framework.attack_trees.add_attack_node(tree, parent_node, node_data)
```

### Path Analysis

#### `analyze_attack_paths(tree, analysis_type)`

Analyzes all possible attack paths in the tree.

**Parameters:**
- `tree` (AttackTree): Attack tree to analyze
- `analysis_type` (str): Type of analysis ("feasibility", "cost", "probability")

**Returns:**
- `PathAnalysis`: Analysis results for all attack paths

**Example:**
```python
# Analyze attack paths
analysis = framework.attack_trees.analyze_attack_paths(tree, "feasibility")

# Get most feasible paths
feasible_paths = analysis.get_feasible_paths(threshold=0.7)
for path in feasible_paths:
    print(f"Path feasibility: {path.feasibility_score}")
    print(f"Path steps: {[node.name for node in path.nodes]}")
```

#### `identify_critical_nodes(tree, criteria)`

Identifies critical nodes that are most important for attack success.

**Parameters:**
- `tree` (AttackTree): Attack tree to analyze
- `criteria` (dict): Criteria for identifying critical nodes

**Returns:**
- `list`: List of critical nodes with importance scores

**Example:**
```python
# Define criteria for critical nodes
criteria = {
    "path_frequency": 0.8,  # Appears in 80% of paths
    "difficulty_threshold": "low",
    "cost_threshold": 10000
}

# Identify critical nodes
critical_nodes = framework.attack_trees.identify_critical_nodes(tree, criteria)

# Prioritize countermeasures
for node in critical_nodes:
    print(f"Critical node: {node.name}, Importance: {node.importance_score}")
```

## Game Theory Component API

### Player Modeling

#### `create_attacker_profile(profile_data)`

Creates an attacker profile for game theory analysis.

**Parameters:**
- `profile_data` (dict): Attacker characteristics and capabilities

**Returns:**
- `AttackerProfile`: Structured attacker profile

**Example:**
```python
# Define attacker profile
profile_data = {
    "skill_level": "advanced",
    "resources": "high",
    "motivation": "financial_gain",
    "risk_tolerance": "medium",
    "time_horizon": "short_term",
    "capabilities": ["social_engineering", "technical_exploitation"]
}

# Create attacker profile
attacker = framework.game_theory.create_attacker_profile(profile_data)
```

#### `create_defender_profile(profile_data)`

Creates a defender profile for game theory analysis.

**Parameters:**
- `profile_data` (dict): Defender characteristics and capabilities

**Returns:**
- `DefenderProfile`: Structured defender profile

**Example:**
```python
# Define defender profile
profile_data = {
    "budget": 1000000,
    "expertise_level": "high",
    "response_time": "fast",
    "available_countermeasures": ["encryption", "authentication", "monitoring"],
    "risk_tolerance": "low"
}

# Create defender profile
defender = framework.game_theory.create_defender_profile(profile_data)
```

### Game Modeling

#### `create_game_model(attack_tree, attacker, defender)`

Creates a game theory model for the given attack tree and player profiles.

**Parameters:**
- `attack_tree` (AttackTree): Attack tree to model
- `attacker` (AttackerProfile): Attacker profile
- `defender` (DefenderProfile): Defender profile

**Returns:**
- `GameModel`: Game theory model ready for analysis

**Example:**
```python
# Create game model
game = framework.game_theory.create_game_model(attack_tree, attacker, defender)

# Configure game parameters
game.configure(
    game_type="sequential",
    information_set="incomplete",
    equilibrium_concept="nash"
)
```

#### `calculate_payoffs(game_model, strategies)`

Calculates payoffs for different strategy combinations.

**Parameters:**
- `game_model` (GameModel): Game model to analyze
- `strategies` (dict): Strategy combinations to evaluate

**Returns:**
- `PayoffMatrix`: Payoff matrix for all strategy combinations

**Example:**
```python
# Define strategies to evaluate
strategies = {
    "attacker": ["attack_path_1", "attack_path_2", "no_attack"],
    "defender": ["deploy_countermeasure", "monitor_only", "no_action"]
}

# Calculate payoffs
payoffs = framework.game_theory.calculate_payoffs(game_model, strategies)

# Analyze results
for attacker_strategy in strategies["attacker"]:
    for defender_strategy in strategies["defender"]:
        payoff = payoffs.get_payoff(attacker_strategy, defender_strategy)
        print(f"Attacker: {attacker_strategy}, Defender: {defender_strategy}, Payoff: {payoff}")
```

### Equilibrium Analysis

#### `find_nash_equilibrium(game_model)`

Finds Nash equilibrium for the game model.

**Parameters:**
- `game_model` (GameModel): Game model to analyze

**Returns:**
- `EquilibriumResult`: Nash equilibrium solution

**Example:**
```python
# Find Nash equilibrium
equilibrium = framework.game_theory.find_nash_equilibrium(game_model)

# Analyze equilibrium
print(f"Equilibrium strategies: {equilibrium.strategies}")
print(f"Equilibrium payoffs: {equilibrium.payoffs}")
print(f"Stability: {equilibrium.stability}")
```

#### `analyze_strategic_interactions(game_model, scenarios)`

Analyzes strategic interactions under different scenarios.

**Parameters:**
- `game_model` (GameModel): Game model to analyze
- `scenarios` (list): Different scenarios to evaluate

**Returns:**
- `ScenarioAnalysis`: Analysis results for all scenarios

**Example:**
```python
# Define scenarios
scenarios = [
    {"budget_increase": 0.2, "threat_level": "high"},
    {"budget_decrease": 0.1, "threat_level": "medium"},
    {"new_vulnerability": True, "threat_level": "high"}
]

# Analyze scenarios
analysis = framework.game_theory.analyze_strategic_interactions(game_model, scenarios)

# Compare scenario outcomes
for scenario in analysis.scenarios:
    print(f"Scenario: {scenario.name}")
    print(f"Optimal strategy: {scenario.optimal_strategy}")
    print(f"Expected payoff: {scenario.expected_payoff}")
```

## Integration API

### Framework Orchestration

#### `run_comprehensive_analysis(system_definition)`

Runs a comprehensive analysis using all framework components.

**Parameters:**
- `system_definition` (dict): Complete system definition and analysis parameters

**Returns:**
- `AnalysisResult`: Comprehensive analysis results

**Example:**
```python
# Define system for analysis
system_definition = {
    "scope": "telematics_ecu",
    "assets": ["firmware", "communication_stack", "user_data"],
    "threats": ["remote_exploitation", "physical_tampering"],
    "analysis_depth": "detailed",
    "output_format": "structured"
}

# Run comprehensive analysis
result = framework.run_comprehensive_analysis(system_definition)

# Access results
print(f"Risk assessment: {result.risk_assessment}")
print(f"Attack trees: {len(result.attack_trees)}")
print(f"Game theory analysis: {result.game_theory_results}")
```

#### `generate_recommendations(analysis_result)`

Generates security recommendations based on analysis results.

**Parameters:**
- `analysis_result` (AnalysisResult): Results from comprehensive analysis

**Returns:**
- `Recommendations`: Prioritized security recommendations

**Example:**
```python
# Generate recommendations
recommendations = framework.generate_recommendations(result)

# Access recommendations
for rec in recommendations:
    print(f"Recommendation: {rec.title}")
    print(f"Priority: {rec.priority}")
    print(f"Cost: {rec.estimated_cost}")
    print(f"Effectiveness: {rec.effectiveness_score}")
```

### Data Export and Reporting

#### `export_results(analysis_result, format_type)`

Exports analysis results in various formats.

**Parameters:**
- `analysis_result` (AnalysisResult): Analysis results to export
- `format_type` (str): Export format ("json", "xml", "pdf", "excel")

**Returns:**
- `str`: Path to exported file

**Example:**
```python
# Export to different formats
json_file = framework.export_results(result, "json")
pdf_file = framework.export_results(result, "pdf")
excel_file = framework.export_results(result, "excel")

print(f"Results exported to: {json_file}, {pdf_file}, {excel_file}")
```

#### `generate_executive_summary(analysis_result)`

Generates an executive summary of the analysis.

**Parameters:**
- `analysis_result` (AnalysisResult): Analysis results to summarize

**Returns:**
- `ExecutiveSummary`: Executive summary document

**Example:**
```python
# Generate executive summary
summary = framework.generate_executive_summary(result)

# Access summary sections
print(f"Key findings: {summary.key_findings}")
print(f"Risk overview: {summary.risk_overview}")
print(f"Recommendations: {summary.recommendations}")
print(f"Investment priorities: {summary.investment_priorities}")
```

## Data Models

### Core Data Structures

#### Asset
```python
class Asset:
    def __init__(self, name, type, value, location, dependencies):
        self.name = name
        self.type = type  # physical, software, data, function
        self.value = value
        self.location = location
        self.dependencies = dependencies
        self.security_controls = []
        self.vulnerabilities = []
```

#### Threat
```python
class Threat:
    def __init__(self, name, type, likelihood, impact, description):
        self.name = name
        self.type = type
        self.likelihood = likelihood
        self.impact = impact
        self.description = description
        self.attack_vectors = []
        self.mitigations = []
```

#### AttackNode
```python
class AttackNode:
    def __init__(self, name, type, prerequisites, difficulty, cost):
        self.name = name
        self.type = type  # root, intermediate, leaf
        self.prerequisites = prerequisites
        self.difficulty = difficulty
        self.cost = cost
        self.children = []
        self.parent = None
        self.countermeasures = []
```

#### GameModel
```python
class GameModel:
    def __init__(self, players, strategies, payoffs):
        self.players = players
        self.strategies = strategies
        self.payoffs = payoffs
        self.equilibrium = None
        self.sensitivity_analysis = None
```

## Error Handling

### Common Exceptions

#### `TARAFrameworkError`
Base exception for all framework errors.

```python
try:
    result = framework.run_comprehensive_analysis(system_definition)
except TARAFrameworkError as e:
    print(f"Framework error: {e.message}")
    print(f"Error code: {e.code}")
    print(f"Suggested action: {e.suggestion}")
```

#### `AssetIdentificationError`
Raised when asset identification fails.

```python
try:
    assets = framework.tara.identify_assets(scope, asset_types)
except AssetIdentificationError as e:
    print(f"Asset identification failed: {e.message}")
    print(f"Missing information: {e.missing_info}")
```

#### `AttackTreeConstructionError`
Raised when attack tree construction fails.

```python
try:
    tree = framework.attack_trees.construct_attack_tree(asset, scenario)
except AttackTreeConstructionError as e:
    print(f"Attack tree construction failed: {e.message}")
    print(f"Invalid nodes: {e.invalid_nodes}")
```

#### `GameTheoryAnalysisError`
Raised when game theory analysis fails.

```python
try:
    equilibrium = framework.game_theory.find_nash_equilibrium(game_model)
except GameTheoryAnalysisError as e:
    print(f"Game theory analysis failed: {e.message}")
    print(f"Model issues: {e.model_issues}")
```

## Configuration

### Framework Configuration

#### `configure_framework(config_file)`

Configures the framework using a configuration file.

**Parameters:**
- `config_file` (str): Path to configuration file

**Example Configuration File (JSON):**
```json
{
    "framework": {
        "version": "1.0",
        "analysis_depth": "detailed",
        "output_format": "structured"
    },
    "tara": {
        "risk_tolerance": "medium",
        "asset_valuation_method": "weighted_scoring",
        "threat_intelligence_sources": ["cve", "mitre", "custom"]
    },
    "attack_trees": {
        "max_tree_depth": 10,
        "node_validation": true,
        "path_analysis_method": "feasibility_based"
    },
    "game_theory": {
        "equilibrium_concept": "nash",
        "information_set": "incomplete",
        "sensitivity_analysis": true
    }
}
```

#### `validate_configuration(config)`

Validates framework configuration.

**Parameters:**
- `config` (dict): Configuration to validate

**Returns:**
- `bool`: True if configuration is valid

**Example:**
```python
# Load and validate configuration
with open('config.json', 'r') as f:
    config = json.load(f)

if framework.validate_configuration(config):
    framework.configure_framework(config)
else:
    print("Invalid configuration. Please check the configuration file.")
```

### Performance Tuning

#### `optimize_performance(performance_profile)`

Optimizes framework performance based on usage profile.

**Parameters:**
- `performance_profile` (dict): Performance requirements and constraints

**Example:**
```python
# Define performance profile
performance_profile = {
    "max_analysis_time": 3600,  # 1 hour
    "memory_limit": "8GB",
    "cpu_cores": 4,
    "parallel_processing": True
}

# Optimize performance
framework.optimize_performance(performance_profile)
```

## Best Practices

### Framework Usage

1. **Start with TARA**: Always begin with comprehensive asset identification and threat assessment
2. **Prioritize High-Risk Assets**: Focus attack tree construction on high-value, high-risk assets
3. **Use Multiple Attacker Profiles**: Model different types of attackers for comprehensive analysis
4. **Validate Game Theory Models**: Ensure game models accurately represent real-world scenarios
5. **Regular Updates**: Keep threat intelligence and vulnerability data current

### Performance Optimization

1. **Scope Management**: Limit analysis scope to critical systems initially
2. **Parallel Processing**: Use parallel processing for large-scale analyses
3. **Caching**: Cache intermediate results for repeated analyses
4. **Incremental Analysis**: Build upon previous analyses rather than starting from scratch

### Quality Assurance

1. **Peer Review**: Have analysis results reviewed by domain experts
2. **Sensitivity Analysis**: Test analysis robustness with parameter variations
3. **Documentation**: Maintain detailed documentation of analysis assumptions and methods
4. **Validation**: Validate results against known attack scenarios and historical data

## Support and Maintenance

### Getting Help

- **Documentation**: Refer to this API documentation for detailed usage instructions
- **Examples**: Check the [Usage Examples](USAGE_EXAMPLES.md) for practical implementation guidance
- **Best Practices**: Review the [Best Practices Guide](BEST_PRACTICES.md) for recommended approaches

### Framework Updates

The framework is regularly updated to incorporate:
- New threat intelligence and attack patterns
- Enhanced game theory models
- Improved analysis algorithms
- Additional export formats and reporting capabilities

### Contributing

Contributions to the framework are welcome. Please refer to the contribution guidelines for:
- Code submission standards
- Documentation requirements
- Testing procedures
- Review processes