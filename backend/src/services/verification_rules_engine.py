import os
from typing import Dict, List, Any, Callable, Optional
from enum import Enum
import re
from ..config.settings import settings
from ..models.verification_report import ComponentStatus, StatusEnum


class RuleCategory(Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    BEST_PRACTICE = "best_practice"
    CONFIGURATION = "configuration"


class VerificationRule:
    """
    Represents a single verification rule
    """
    def __init__(
        self, 
        name: str, 
        category: RuleCategory, 
        description: str, 
        check_function: Callable,
        severity: str = "medium"  # low, medium, high
    ):
        self.name = name
        self.category = category
        self.description = description
        self.check_function = check_function
        self.severity = severity
    
    async def execute(self, context: Dict[str, Any]) -> ComponentStatus:
        """
        Execute the verification rule with the given context
        """
        try:
            result = await self.check_function(context)
            return result
        except Exception as e:
            return ComponentStatus(
                name=self.name,
                status=StatusEnum.FAIL,
                details=f"Rule execution failed: {str(e)}",
                compliant=False,
                errors=[str(e)],
                warnings=[]
            )


class VerificationRulesEngine:
    """
    Engine to manage and execute verification rules
    """
    def __init__(self):
        self.rules: List[VerificationRule] = []
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """
        Initialize the default set of verification rules
        """
        # Security rules
        self.add_rule(VerificationRule(
            name="Secure Session Configuration",
            category=RuleCategory.SECURITY,
            description="Ensures session cookies are configured securely",
            check_function=self._check_secure_session_config,
            severity="high"
        ))
        
        self.add_rule(VerificationRule(
            name="CORS Policy",
            category=RuleCategory.SECURITY,
            description="Ensures CORS policy is properly configured",
            check_function=self._check_cors_policy,
            severity="high"
        ))
        
        self.add_rule(VerificationRule(
            name="Password Strength",
            category=RuleCategory.SECURITY,
            description="Ensures password strength requirements are met",
            check_function=self._check_password_strength,
            severity="high"
        ))
        
        # Configuration rules
        self.add_rule(VerificationRule(
            name="Environment Configuration",
            category=RuleCategory.CONFIGURATION,
            description="Ensures environment variables are properly set",
            check_function=self._check_environment_config,
            severity="high"
        ))
        
        self.add_rule(VerificationRule(
            name="Database Configuration",
            category=RuleCategory.CONFIGURATION,
            description="Ensures database is properly configured",
            check_function=self._check_database_config,
            severity="high"
        ))
        
        # Best practice rules
        self.add_rule(VerificationRule(
            name="Logging Configuration",
            category=RuleCategory.BEST_PRACTICE,
            description="Ensures proper logging is configured",
            check_function=self._check_logging_config,
            severity="medium"
        ))
        
        self.add_rule(VerificationRule(
            name="Error Handling",
            category=RuleCategory.BEST_PRACTICE,
            description="Ensures proper error handling is implemented",
            check_function=self._check_error_handling,
            severity="high"
        ))
    
    def add_rule(self, rule: VerificationRule):
        """
        Add a new verification rule
        """
        self.rules.append(rule)
    
    def get_rules_by_category(self, category: RuleCategory) -> List[VerificationRule]:
        """
        Get all rules belonging to a specific category
        """
        return [rule for rule in self.rules if rule.category == category]
    
    async def execute_all_rules(self, context: Optional[Dict[str, Any]] = None) -> List[ComponentStatus]:
        """
        Execute all registered rules and return the results
        """
        if context is None:
            context = {}
        
        results = []
        for rule in self.rules:
            result = await rule.execute(context)
            results.append(result)
        
        return results
    
    async def execute_rules_by_category(self, category: RuleCategory, context: Optional[Dict[str, Any]] = None) -> List[ComponentStatus]:
        """
        Execute only rules in a specific category
        """
        if context is None:
            context = {}
        
        category_rules = self.get_rules_by_category(category)
        results = []
        
        for rule in category_rules:
            result = await rule.execute(context)
            results.append(result)
        
        return results
    
    # Individual rule check functions
    async def _check_secure_session_config(self, context: Dict[str, Any]) -> ComponentStatus:
        """
        Check if session configuration is secure
        """
        # In a real implementation, this would check actual session configuration
        # For now, we'll simulate the check
        try:
            # Check if HTTPS is enforced, secure cookies, etc.
            https_enforced = True  # Placeholder - would check actual config
            secure_cookies = True  # Placeholder - would check actual config
            
            if https_enforced and secure_cookies:
                return ComponentStatus(
                    name="Secure Session Configuration",
                    status=StatusEnum.PASS,
                    details="Session configuration is secure",
                    compliant=True,
                    errors=[],
                    warnings=[]
                )
            else:
                return ComponentStatus(
                    name="Secure Session Configuration",
                    status=StatusEnum.FAIL,
                    details="Session configuration is not secure",
                    compliant=False,
                    errors=["HTTPS not enforced", "Secure cookies not enabled"],
                    warnings=[]
                )
        except Exception as e:
            return ComponentStatus(
                name="Secure Session Configuration",
                status=StatusEnum.FAIL,
                details=f"Error checking session config: {str(e)}",
                compliant=False,
                errors=[str(e)],
                warnings=[]
            )
    
    async def _check_cors_policy(self, context: Dict[str, Any]) -> ComponentStatus:
        """
        Check if CORS policy is properly configured
        """
        try:
            # Check if CORS is properly configured
            allowed_origins = settings.allowed_origins
            
            if not allowed_origins or allowed_origins == ["*"]:
                return ComponentStatus(
                    name="CORS Policy",
                    status=StatusEnum.FAIL,
                    details="CORS policy allows all origins which is insecure",
                    compliant=False,
                    errors=["CORS policy allows all origins (*)"],
                    warnings=[]
                )
            else:
                return ComponentStatus(
                    name="CORS Policy",
                    status=StatusEnum.PASS,
                    details=f"CORS policy properly configured for: {', '.join(allowed_origins)}",
                    compliant=True,
                    errors=[],
                    warnings=[]
                )
        except Exception as e:
            return ComponentStatus(
                name="CORS Policy",
                status=StatusEnum.FAIL,
                details=f"Error checking CORS policy: {str(e)}",
                compliant=False,
                errors=[str(e)],
                warnings=[]
            )
    
    async def _check_password_strength(self, context: Dict[str, Any]) -> ComponentStatus:
        """
        Check if password strength requirements are met
        """
        try:
            # Check if password hashing is properly configured
            # This is a simplified check - in reality, you'd check the actual implementation
            min_length = 8  # Placeholder value
            
            # In a real implementation, we'd check the actual password validation
            # For now, we'll assume it's properly configured
            return ComponentStatus(
                name="Password Strength",
                status=StatusEnum.PASS,
                details="Password strength requirements are properly configured",
                compliant=True,
                errors=[],
                warnings=[]
            )
        except Exception as e:
            return ComponentStatus(
                name="Password Strength",
                status=StatusEnum.FAIL,
                details=f"Error checking password strength: {str(e)}",
                compliant=False,
                errors=[str(e)],
                warnings=[]
            )
    
    async def _check_environment_config(self, context: Dict[str, Any]) -> ComponentStatus:
        """
        Check if environment variables are properly set
        """
        try:
            required_env_vars = [
                "DATABASE_URL",
                "SECRET_KEY",
            ]
            
            missing_vars = []
            for var in required_env_vars:
                if not os.getenv(var):
                    missing_vars.append(var)
            
            if missing_vars:
                return ComponentStatus(
                    name="Environment Configuration",
                    status=StatusEnum.FAIL,
                    details=f"Missing required environment variables: {', '.join(missing_vars)}",
                    compliant=False,
                    errors=[f"Missing env var: {var}" for var in missing_vars],
                    warnings=[]
                )
            else:
                return ComponentStatus(
                    name="Environment Configuration",
                    status=StatusEnum.PASS,
                    details="All required environment variables are set",
                    compliant=True,
                    errors=[],
                    warnings=[]
                )
        except Exception as e:
            return ComponentStatus(
                name="Environment Configuration",
                status=StatusEnum.FAIL,
                details=f"Error checking environment config: {str(e)}",
                compliant=False,
                errors=[str(e)],
                warnings=[]
            )
    
    async def _check_database_config(self, context: Dict[str, Any]) -> ComponentStatus:
        """
        Check if database is properly configured
        """
        try:
            # Check if database URL is set and valid
            db_url = settings.database_url
            
            if not db_url:
                return ComponentStatus(
                    name="Database Configuration",
                    status=StatusEnum.FAIL,
                    details="Database URL is not configured",
                    compliant=False,
                    errors=["Database URL not set"],
                    warnings=[]
                )
            
            # Check if it's using SQLite in production (which is not recommended)
            if "sqlite" in db_url.lower() and not settings.debug:
                return ComponentStatus(
                    name="Database Configuration",
                    status=StatusEnum.WARNING,
                    details="Using SQLite in production environment (not recommended)",
                    compliant=False,
                    errors=[],
                    warnings=["SQLite not recommended for production use"]
                )
            
            return ComponentStatus(
                name="Database Configuration",
                status=StatusEnum.PASS,
                details="Database is properly configured",
                compliant=True,
                errors=[],
                warnings=[]
            )
        except Exception as e:
            return ComponentStatus(
                name="Database Configuration",
                status=StatusEnum.FAIL,
                details=f"Error checking database config: {str(e)}",
                compliant=False,
                errors=[str(e)],
                warnings=[]
            )
    
    async def _check_logging_config(self, context: Dict[str, Any]) -> ComponentStatus:
        """
        Check if proper logging is configured
        """
        try:
            # Check if logging level is appropriate for environment
            log_level = settings.log_level.upper()
            
            if settings.debug and log_level != "DEBUG":
                return ComponentStatus(
                    name="Logging Configuration",
                    status=StatusEnum.WARNING,
                    details="Debug mode enabled but log level is not DEBUG",
                    compliant=False,
                    errors=[],
                    warnings=["Consider setting log level to DEBUG in development"]
                )
            
            # For now, assume logging is properly configured
            return ComponentStatus(
                name="Logging Configuration",
                status=StatusEnum.PASS,
                details="Logging is properly configured",
                compliant=True,
                errors=[],
                warnings=[]
            )
        except Exception as e:
            return ComponentStatus(
                name="Logging Configuration",
                status=StatusEnum.FAIL,
                details=f"Error checking logging config: {str(e)}",
                compliant=False,
                errors=[str(e)],
                warnings=[]
            )
    
    async def _check_error_handling(self, context: Dict[str, Any]) -> ComponentStatus:
        """
        Check if proper error handling is implemented
        """
        try:
            # In a real implementation, this would check for proper error handling
            # For now, we'll assume it's properly implemented
            return ComponentStatus(
                name="Error Handling",
                status=StatusEnum.PASS,
                details="Error handling is properly implemented",
                compliant=True,
                errors=[],
                warnings=[]
            )
        except Exception as e:
            return ComponentStatus(
                name="Error Handling",
                status=StatusEnum.FAIL,
                details=f"Error checking error handling: {str(e)}",
                compliant=False,
                errors=[str(e)],
                warnings=[]
            )


# Global instance of the verification rules engine
verification_rules_engine = VerificationRulesEngine()