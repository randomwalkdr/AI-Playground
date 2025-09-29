# TARA-Attack Trees-Game Theory Framework

A comprehensive framework for automotive cybersecurity risk analysis that integrates Threat Analysis and Risk Assessment (TARA), Attack Trees, and Game Theory.

## Overview

The TARA framework provides a systematic approach to understanding, assessing, and mitigating cybersecurity risks in complex automotive systems. It combines three complementary methodologies:

- **TARA (Threat Analysis and Risk Assessment)**: Foundation for asset identification and initial risk assessment
- **Attack Trees**: Detailed attack path modeling and vulnerability analysis  
- **Game Theory**: Strategic interaction modeling between attackers and defenders

## Key Features

- **Dynamic Risk Assessment**: Incorporates strategic attacker behavior
- **Cost-Benefit Analysis**: Optimizes security investments
- **Proactive Defense**: Enables "what-if" scenario analysis
- **Stakeholder Communication**: Clear visualization of risks and defenses
- **Standards Compliance**: Aligns with ISO 21434 and UNECE WP.29 regulations

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/tara-framework/tara-framework.git
cd tara-framework

# Install dependencies
pip install -r requirements.txt

# Install the framework
pip install -e .
```

### Install Dependencies Only

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from tara_framework import TARAFramework

# Initialize the framework
framework = TARAFramework(
    scope="telematics_ecu",
    analysis_type="comprehensive",
    output_format="structured"
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
    }
}

# Run comprehensive analysis
result = framework.run_comprehensive_analysis(system_definition)

# Display results
print(f"Assets analyzed: {len(result.asset_inventory)}")
print(f"Threats identified: {len(result.threat_assessment)}")
print(f"Recommendations: {len(result.recommendations)}")
```

### Advanced Usage

```python
# Custom configuration
custom_config = {
    "tara": {
        "asset_valuation_method": "weighted_scoring",
        "risk_tolerance": "low"
    },
    "attack_trees": {
        "max_tree_depth": 10,
        "path_analysis_method": "comprehensive"
    },
    "game_theory": {
        "equilibrium_concept": "nash",
        "sensitivity_analysis": True
    }
}

# Initialize with custom configuration
framework = TARAFramework(config=custom_config)

# Run analysis with custom parameters
result = framework.run_comprehensive_analysis(system_definition)

# Export results
json_file = framework.export_results(result, "json")
pdf_file = framework.export_results(result, "pdf")

# Generate executive summary
summary = framework.generate_executive_summary(result)
```

## Framework Components

### 1. TARA Component

The TARA component handles asset identification and threat assessment:

```python
# Asset identification
assets = framework.tara.identify_assets(system_scope, asset_types)

# Threat assessment
threats = framework.tara.identify_threats(assets, threat_intelligence)

# Risk assessment
risk = framework.tara.assess_risk_level(threat, vulnerability, impact)
```

### 2. Attack Trees Component

The Attack Trees component constructs and analyzes attack paths:

```python
# Construct attack tree
tree = framework.attack_trees.construct_attack_tree(target_asset, threat_scenario)

# Analyze attack paths
analysis = framework.attack_trees.analyze_attack_paths(tree, "feasibility")

# Identify critical nodes
critical_nodes = framework.attack_trees.identify_critical_nodes(tree, criteria)
```

### 3. Game Theory Component

The Game Theory component models strategic interactions:

```python
# Create player profiles
attacker = framework.game_theory.create_attacker_profile(attacker_data)
defender = framework.game_theory.create_defender_profile(defender_data)

# Create game model
game = framework.game_theory.create_game_model(attack_tree, attacker, defender)

# Find Nash equilibrium
equilibrium = framework.game_theory.find_nash_equilibrium(game)

# Scenario analysis
scenarios = [{"budget_increase": 0.2}, {"new_vulnerability": True}]
analysis = framework.game_theory.analyze_strategic_interactions(game, scenarios)
```

## Examples

### Basic Example

See `examples/basic_usage.py` for a simple example that demonstrates:
- Framework initialization
- Basic system definition
- Comprehensive analysis
- Results display and export

### Advanced Example

See `examples/advanced_usage.py` for an advanced example that demonstrates:
- Custom configuration
- Multiple attacker profiles
- Scenario analysis
- Detailed component usage

### Running Examples

```bash
# Run basic example
python examples/basic_usage.py

# Run advanced example
python examples/advanced_usage.py
```

## Configuration

The framework can be configured using a configuration dictionary:

```python
config = {
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

framework = TARAFramework(config=config)
```

## Data Models

### Core Models

- **Asset**: Represents system assets (physical, software, data, functions)
- **Threat**: Represents potential threats to the system
- **Vulnerability**: Represents system vulnerabilities
- **RiskAssessment**: Risk assessment results
- **AttackTree**: Attack tree structure with nodes and paths
- **GameModel**: Game theory model for strategic analysis
- **AnalysisResult**: Comprehensive analysis results

### Example Asset Definition

```python
from tara_framework.core.models import Asset, AssetType

asset = Asset(
    name="Powertrain ECU",
    asset_type=AssetType.PHYSICAL,
    description="Engine control unit managing powertrain functions",
    location="engine_compartment",
    value=8.0,
    impact_safety=9.0,
    impact_financial=7.0,
    impact_operational=8.0,
    impact_privacy=2.0
)
```

## Export and Reporting

The framework supports multiple export formats:

```python
# Export to different formats
json_file = framework.export_results(result, "json")
xml_file = framework.export_results(result, "xml")
pdf_file = framework.export_results(result, "pdf")
excel_file = framework.export_results(result, "excel")

# Generate executive summary
summary = framework.generate_executive_summary(result)
```

## Standards Compliance

The framework aligns with automotive cybersecurity standards:

- **ISO 21434**: Road vehicles — Cybersecurity engineering
- **UNECE WP.29**: UN Regulation on Cybersecurity and Software Updates
- **SAE J3061**: Cybersecurity Guidebook for Cyber-Physical Vehicle Systems

## Best Practices

### 1. Scope Definition

- Define clear system boundaries
- Focus on critical assets and functions
- Exclude irrelevant components

### 2. Asset Identification

- Use systematic asset categorization
- Include all asset types (physical, software, data, functions)
- Assess asset values consistently

### 3. Threat Assessment

- Use multiple threat intelligence sources
- Model different threat actor profiles
- Consider evolving threat landscape

### 4. Attack Tree Construction

- Start with high-level attack goals
- Decompose into specific attack steps
- Validate tree completeness and logic

### 5. Game Theory Analysis

- Create realistic player profiles
- Use appropriate game models
- Perform sensitivity analysis

## Performance Optimization

For large-scale analyses:

```python
# Configure for performance
performance_config = {
    "parallel_processing": True,
    "max_workers": 4,
    "memory_limit": "8GB",
    "cache_intermediate_results": True
}

framework.optimize_performance(performance_config)
```

## Error Handling

The framework provides comprehensive error handling:

```python
from tara_framework.core.exceptions import TARAFrameworkError

try:
    result = framework.run_comprehensive_analysis(system_definition)
except TARAFrameworkError as e:
    print(f"Framework error: {e.message}")
    print(f"Error code: {e.code}")
    print(f"Suggestion: {e.suggestion}")
```

## Contributing

Contributions are welcome! Please see the contribution guidelines for:

- Code submission standards
- Documentation requirements
- Testing procedures
- Review processes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- **Documentation**: See the comprehensive API documentation
- **Examples**: Check the examples directory for practical usage
- **Issues**: Report issues on GitHub
- **Discussions**: Join discussions on GitHub

## Changelog

### Version 1.0.0

- Initial release
- Complete TARA, Attack Trees, and Game Theory integration
- Comprehensive API and documentation
- Example usage scripts
- Export and reporting capabilities

## Roadmap

### Version 1.1.0 (Planned)

- Enhanced visualization capabilities
- Web-based interface
- Additional game theory models
- Machine learning integration

### Version 1.2.0 (Planned)

- Real-time threat intelligence integration
- Advanced scenario modeling
- Collaborative analysis features
- Cloud deployment support

## Citation

If you use this framework in your research, please cite:

```bibtex
@software{tara_framework,
  title={TARA-Attack Trees-Game Theory Framework for Automotive Cybersecurity},
  author={TARA Framework Team},
  year={2024},
  url={https://github.com/tara-framework/tara-framework}
}
```

## Acknowledgments

- Automotive cybersecurity community
- ISO 21434 working group
- UNECE WP.29 cybersecurity experts
- Open source contributors