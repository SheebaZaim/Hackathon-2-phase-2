from typing import Dict, List, Any, Optional
from enum import Enum
import asyncio

from ..models.verification_report import ComponentStatus
from ..utils.logger import verification_logger


class RecommendationPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationType(Enum):
    IMPLEMENTATION = "implementation"
    FIX = "fix"
    CONFIGURATION = "configuration"
    OPTIMIZATION = "optimization"
    SECURITY = "security"


class UpdateRecommendation:
    """
    Represents a recommendation for updating a component
    """
    def __init__(self, 
                 component_name: str, 
                 recommendation_type: RecommendationType, 
                 priority: RecommendationPriority, 
                 description: str, 
                 implementation_steps: List[str],
                 estimated_time_hours: float,
                 potential_risks: List[str] = None,
                 dependencies: List[str] = None):
        self.component_name = component_name
        self.recommendation_type = recommendation_type
        self.priority = priority
        self.description = description
        self.implementation_steps = implementation_steps
        self.estimated_time_hours = estimated_time_hours
        self.potential_risks = potential_risks or []
        self.dependencies = dependencies or []
        # Use a default value for created_at since we can't get event loop in constructor
        import time
        self.created_at = time.time()


class UpdateRecommendationEngine:
    """
    Engine to generate recommendations for updating components based on verification results
    """
    
    def __init__(self):
        self.recommendations: List[UpdateRecommendation] = []
    
    async def generate_recommendations_from_report(self, components: List[ComponentStatus]) -> List[UpdateRecommendation]:
        """
        Generate update recommendations based on verification results
        """
        recommendations = []
        
        for component in components:
            if component.status == "fail":
                rec = await self._generate_recommendation_for_failed_component(component)
                if rec:
                    recommendations.append(rec)
            elif component.status == "missing":
                rec = await self._generate_recommendation_for_missing_component(component)
                if rec:
                    recommendations.append(rec)
            elif component.status == "warning":
                rec = await self._generate_recommendation_for_warning_component(component)
                if rec:
                    recommendations.append(rec)
        
        # Sort recommendations by priority
        recommendations.sort(key=lambda x: self._priority_to_int(x.priority), reverse=True)
        
        verification_logger.info(f"Generated {len(recommendations)} update recommendations")
        return recommendations
    
    def _priority_to_int(self, priority: RecommendationPriority) -> int:
        """
        Convert priority enum to integer for sorting
        """
        mapping = {
            RecommendationPriority.CRITICAL: 4,
            RecommendationPriority.HIGH: 3,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.LOW: 1
        }
        return mapping.get(priority, 0)
    
    async def _generate_recommendation_for_failed_component(self, component: ComponentStatus) -> Optional[UpdateRecommendation]:
        """
        Generate a recommendation for a failed component
        """
        # Determine the type of recommendation based on the component name
        rec_type = RecommendationType.FIX
        priority = RecommendationPriority.HIGH
        
        # Special handling for critical components
        if any(critical_term in component.name.lower() for critical_term in 
               ["authentication", "security", "database", "auth"]):
            priority = RecommendationPriority.CRITICAL
        
        # Create implementation steps based on the component details
        implementation_steps = [
            f"Investigate the cause of failure in {component.name}",
            f"Review logs and error messages for {component.name}",
            f"Fix the underlying issue causing the failure",
            f"Test the component after applying fixes",
            f"Verify the component passes all tests"
        ]
        
        # Add specific steps based on component type
        if "database" in component.name.lower():
            implementation_steps.insert(2, "Check database connection settings")
            implementation_steps.insert(3, "Verify database schema is correct")
        elif "authentication" in component.name.lower():
            implementation_steps.insert(2, "Check authentication configuration")
            implementation_steps.insert(3, "Verify token generation/verification")
        elif "security" in component.name.lower():
            implementation_steps.insert(2, "Review security configuration")
            implementation_steps.insert(3, "Apply security patches if needed")
        
        # Estimate time based on complexity
        estimated_time = 4.0  # 4 hours for a typical fix
        if priority == RecommendationPriority.CRITICAL:
            estimated_time = 8.0  # More time for critical issues
        
        return UpdateRecommendation(
            component_name=component.name,
            recommendation_type=rec_type,
            priority=priority,
            description=f"Fix the failing {component.name} component: {component.details}",
            implementation_steps=implementation_steps,
            estimated_time_hours=estimated_time,
            potential_risks=["System instability if not fixed", "Security vulnerability"],
            dependencies=[]
        )
    
    async def _generate_recommendation_for_missing_component(self, component: ComponentStatus) -> Optional[UpdateRecommendation]:
        """
        Generate a recommendation for a missing component
        """
        rec_type = RecommendationType.IMPLEMENTATION
        priority = RecommendationPriority.HIGH
        
        # Special handling for critical components
        if any(critical_term in component.name.lower() for critical_term in 
               ["authentication", "database", "security"]):
            priority = RecommendationPriority.CRITICAL
        
        # Create implementation steps for missing component
        implementation_steps = [
            f"Determine requirements for {component.name}",
            f"Design the architecture for {component.name}",
            f"Implement the {component.name} component",
            f"Integrate {component.name} with existing system",
            f"Test the {component.name} component thoroughly"
        ]
        
        # Estimate time based on complexity
        estimated_time = 8.0  # 8 hours for implementing a missing component
        if priority == RecommendationPriority.CRITICAL:
            estimated_time = 16.0  # More time for critical components
        
        return UpdateRecommendation(
            component_name=component.name,
            recommendation_type=rec_type,
            priority=priority,
            description=f"Implement the missing {component.name} component: {component.details}",
            implementation_steps=implementation_steps,
            estimated_time_hours=estimated_time,
            potential_risks=["Feature incompleteness", "System instability"],
            dependencies=[]
        )
    
    async def _generate_recommendation_for_warning_component(self, component: ComponentStatus) -> Optional[UpdateRecommendation]:
        """
        Generate a recommendation for a component with warnings
        """
        rec_type = RecommendationType.OPTIMIZATION
        priority = RecommendationPriority.LOW
        
        # Create implementation steps for addressing warnings
        implementation_steps = [
            f"Review the warnings for {component.name}",
            f"Determine if warnings indicate potential issues",
            f"Address warnings if they represent real problems",
            f"Update {component.name} to resolve warnings",
            f"Verify that changes don't introduce new issues"
        ]
        
        # Estimate time for addressing warnings
        estimated_time = 2.0  # 2 hours for addressing warnings
        
        return UpdateRecommendation(
            component_name=component.name,
            recommendation_type=rec_type,
            priority=priority,
            description=f"Address warnings in {component.name}: {component.details}",
            implementation_steps=implementation_steps,
            estimated_time_hours=estimated_time,
            potential_risks=["Performance degradation", "Future compatibility issues"],
            dependencies=[]
        )
    
    async def get_recommendations_by_priority(self, priority: RecommendationPriority) -> List[UpdateRecommendation]:
        """
        Get recommendations filtered by priority
        """
        return [rec for rec in self.recommendations if rec.priority == priority]
    
    async def get_recommendations_by_type(self, rec_type: RecommendationType) -> List[UpdateRecommendation]:
        """
        Get recommendations filtered by type
        """
        return [rec for rec in self.recommendations if rec.recommendation_type == rec_type]
    
    def _determine_related_user_story(self, component_name: str) -> Optional[str]:
        """
        Determine which user story a component is related to
        """
        # Map component names to user stories
        component_to_story_map = {
            "authentication": "US1 - Complete Technical Planning",
            "database": "US1 - Complete Technical Planning",
            "api health": "US5 - Ensure Frontend and Backend Run Without Error",
            "logging system": "US5 - Ensure Frontend and Backend Run Without Error",
            "security headers": "US5 - Ensure Frontend and Backend Run Without Error",
            "rate limiting": "US5 - Ensure Frontend and Backend Run Without Error",
            "environment variables": "US3 - Verify Missing Components",
        }
        
        for key, story in component_to_story_map.items():
            if key.lower() in component_name.lower():
                return story
        
        # Default to the most common user story
        return "US1 - Complete Technical Planning"

    async def get_top_recommendations(self, count: int = 5) -> List[UpdateRecommendation]:
        """
        Get the top N recommendations by priority
        """
        sorted_recs = sorted(self.recommendations, key=lambda x: self._priority_to_int(x.priority), reverse=True)
        return sorted_recs[:count]


# Global instance of the update recommendation engine
update_recommendation_engine = UpdateRecommendationEngine()