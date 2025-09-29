"""
Custom exceptions for the TARA framework.
"""


class TARAFrameworkError(Exception):
    """Base exception for all TARA framework errors."""
    
    def __init__(self, message: str, code: str = None, suggestion: str = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.suggestion = suggestion


class AssetIdentificationError(TARAFrameworkError):
    """Raised when asset identification fails."""
    
    def __init__(self, message: str, missing_info: list = None):
        super().__init__(message, "ASSET_ID_ERROR")
        self.missing_info = missing_info or []


class ThreatAssessmentError(TARAFrameworkError):
    """Raised when threat assessment fails."""
    
    def __init__(self, message: str, invalid_threats: list = None):
        super().__init__(message, "THREAT_ASSESSMENT_ERROR")
        self.invalid_threats = invalid_threats or []


class AttackTreeConstructionError(TARAFrameworkError):
    """Raised when attack tree construction fails."""
    
    def __init__(self, message: str, invalid_nodes: list = None):
        super().__init__(message, "ATTACK_TREE_ERROR")
        self.invalid_nodes = invalid_nodes or []


class GameTheoryAnalysisError(TARAFrameworkError):
    """Raised when game theory analysis fails."""
    
    def __init__(self, message: str, model_issues: list = None):
        super().__init__(message, "GAME_THEORY_ERROR")
        self.model_issues = model_issues or []


class ConfigurationError(TARAFrameworkError):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str, invalid_config: dict = None):
        super().__init__(message, "CONFIG_ERROR")
        self.invalid_config = invalid_config or {}


class ValidationError(TARAFrameworkError):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, validation_errors: list = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.validation_errors = validation_errors or []


class ExportError(TARAFrameworkError):
    """Raised when export operations fail."""
    
    def __init__(self, message: str, export_format: str = None):
        super().__init__(message, "EXPORT_ERROR")
        self.export_format = export_format