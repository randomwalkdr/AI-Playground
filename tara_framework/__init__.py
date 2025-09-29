"""
TARA-Attack Trees-Game Theory Framework

A comprehensive framework for automotive cybersecurity risk analysis that integrates
Threat Analysis and Risk Assessment (TARA), Attack Trees, and Game Theory.

This framework provides a systematic approach to understanding, assessing, and
mitigating cybersecurity risks in complex automotive systems.
"""

from .core.models import (
    Asset, Threat, Vulnerability, RiskLevel, AssetValue,
    AttackNode, AttackTree, AttackPath,
    AttackerProfile, DefenderProfile, GameModel, PayoffMatrix,
    AnalysisResult, Recommendation
)

from .components.tara import TARAComponent
from .components.attack_trees import AttackTreesComponent
from .components.game_theory import GameTheoryComponent
from .framework import TARAFramework

__version__ = "1.0.0"
__author__ = "TARA Framework Team"

__all__ = [
    # Core models
    'Asset', 'Threat', 'Vulnerability', 'RiskLevel', 'AssetValue',
    'AttackNode', 'AttackTree', 'AttackPath',
    'AttackerProfile', 'DefenderProfile', 'GameModel', 'PayoffMatrix',
    'AnalysisResult', 'Recommendation',
    
    # Components
    'TARAComponent', 'AttackTreesComponent', 'GameTheoryComponent',
    
    # Main framework
    'TARAFramework'
]