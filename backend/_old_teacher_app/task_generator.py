import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4

from ..models.task_template import TaskTemplate, TaskPriority, TaskStatus
from ..utils.logger import verification_logger
from ..services.verification_service import verification_service


class TaskGenerator:
    """
    Service to generate implementation tasks based on verification results
    """
    
    def __init__(self):
        self.task_templates: List[TaskTemplate] = []
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """
        Initialize default task templates for common verification issues
        """
        # Template for missing components
        self.task_templates.append(TaskTemplate(
            id=str(uuid4()),
            title="Implement Missing Component",
            description="Implement a component that was identified as missing during verification",
            priority=TaskPriority.HIGH,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            acceptance_criteria=[
                "Component is implemented according to specifications",
                "Component passes all relevant tests",
                "Component integrates properly with existing system"
            ],
            test_scenarios=[
                "Component can be instantiated and configured",
                "Component performs its intended function",
                "Component handles edge cases appropriately"
            ]
        ))
        
        # Template for configuration issues
        self.task_templates.append(TaskTemplate(
            id=str(uuid4()),
            title="Fix Configuration Issue",
            description="Address configuration issues identified during verification",
            priority=TaskPriority.HIGH,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            acceptance_criteria=[
                "Configuration values are properly set",
                "Configuration is validated and secure",
                "Application starts without configuration errors"
            ],
            test_scenarios=[
                "Application starts with new configuration",
                "Configuration values are properly loaded",
                "Security-sensitive configurations are protected"
            ]
        ))
        
        # Template for security vulnerabilities
        self.task_templates.append(TaskTemplate(
            id=str(uuid4()),
            title="Address Security Vulnerability",
            description="Fix security vulnerability identified during verification",
            priority=TaskPriority.CRITICAL,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            acceptance_criteria=[
                "Vulnerability is patched",
                "Security tests pass",
                "No regression in functionality"
            ],
            test_scenarios=[
                "Vulnerability is no longer exploitable",
                "Normal functionality still works",
                "Security scanning tools pass"
            ]
        ))
        
        # Template for performance issues
        self.task_templates.append(TaskTemplate(
            id=str(uuid4()),
            title="Optimize Performance",
            description="Address performance issues identified during verification",
            priority=TaskPriority.MEDIUM,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            acceptance_criteria=[
                "Performance metrics meet requirements",
                "Response times are improved",
                "Resource usage is optimized"
            ],
            test_scenarios=[
                "Load testing shows improved performance",
                "Response times are within acceptable limits",
                "Memory usage is optimized"
            ]
        ))
    
    def generate_tasks_from_verification_report(self, report_id: str) -> List[TaskTemplate]:
        """
        Generate implementation tasks based on a verification report
        """
        report = verification_service.get_report(report_id)
        if not report:
            raise ValueError(f"Verification report with ID {report_id} not found")
        
        tasks = []
        
        for component in report.components_checked:
            if component.status == "fail":
                # Create a task for each failed component
                task = self._create_task_for_failed_component(component, report)
                tasks.append(task)
            elif component.status == "missing":
                # Create a task for each missing component
                task = self._create_task_for_missing_component(component, report)
                tasks.append(task)
            elif component.status == "warning":
                # Create a task for each warning component
                task = self._create_task_for_warning_component(component, report)
                tasks.append(task)
        
        # Log the task generation
        verification_logger.info(f"Generated {len(tasks)} tasks from verification report {report_id}")
        
        return tasks
    
    def _create_task_for_failed_component(self, component, report) -> TaskTemplate:
        """
        Create a task for a failed component
        """
        # Determine priority based on component importance
        priority = TaskPriority.HIGH if component.name.lower() in ["authentication", "database", "security"] else TaskPriority.MEDIUM
        
        title = f"Fix {component.name} Issue"
        description = f"Address the issues with {component.name} identified in verification report {report.id}. {component.details}"
        
        # Find a suitable template
        template = self._find_template_by_title("Fix Configuration Issue") or self.task_templates[0]
        
        return TaskTemplate(
            id=str(uuid4()),
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.TODO,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            acceptance_criteria=template.acceptance_criteria,
            test_scenarios=template.test_scenarios,
            related_user_story=self._determine_related_user_story(component.name)
        )
    
    def _create_task_for_missing_component(self, component, report) -> TaskTemplate:
        """
        Create a task for a missing component
        """
        title = f"Implement {component.name}"
        description = f"Implement the missing {component.name} component identified in verification report {report.id}. {component.details}"
        
        # Find a suitable template
        template = self._find_template_by_title("Implement Missing Component") or self.task_templates[0]
        
        return TaskTemplate(
            id=str(uuid4()),
            title=title,
            description=description,
            priority=TaskPriority.HIGH,
            status=TaskStatus.TODO,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            acceptance_criteria=template.acceptance_criteria,
            test_scenarios=template.test_scenarios,
            related_user_story=self._determine_related_user_story(component.name)
        )
    
    def _create_task_for_warning_component(self, component, report) -> TaskTemplate:
        """
        Create a task for a component with warnings
        """
        title = f"Address {component.name} Warnings"
        description = f"Address the warnings with {component.name} identified in verification report {report.id}. {component.details}"
        
        # Find a suitable template
        template = self._find_template_by_title("Fix Configuration Issue") or self.task_templates[0]
        
        return TaskTemplate(
            id=str(uuid4()),
            title=title,
            description=description,
            priority=TaskPriority.LOW,
            status=TaskStatus.TODO,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            acceptance_criteria=template.acceptance_criteria,
            test_scenarios=template.test_scenarios,
            related_user_story=self._determine_related_user_story(component.name)
        )
    
    def _find_template_by_title(self, title: str) -> Optional[TaskTemplate]:
        """
        Find a task template by its title
        """
        for template in self.task_templates:
            if title.lower() in template.title.lower():
                return template
        return None
    
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
    
    def generate_tasks_for_constitution_issues(self) -> List[TaskTemplate]:
        """
        Generate tasks for constitution compliance issues
        """
        # This would typically run constitution checks and create tasks for non-compliant items
        # For now, we'll return an empty list as this would require integration with the constitution checker
        tasks = []
        
        # In a real implementation, we would:
        # 1. Run constitution compliance checks
        # 2. Identify non-compliant items
        # 3. Create tasks to address each non-compliance
        
        verification_logger.info(f"Generated {len(tasks)} tasks for constitution compliance issues")
        return tasks
    
    def create_custom_task(self, title: str, description: str, priority: TaskPriority = TaskPriority.MEDIUM, 
                          acceptance_criteria: List[str] = None, test_scenarios: List[str] = None) -> TaskTemplate:
        """
        Create a custom task with specified parameters
        """
        if acceptance_criteria is None:
            acceptance_criteria = ["Task requirements are fulfilled", "Task passes relevant tests"]
        
        if test_scenarios is None:
            test_scenarios = ["Task completion can be verified"]
        
        task = TaskTemplate(
            id=str(uuid4()),
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.TODO,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            acceptance_criteria=acceptance_criteria,
            test_scenarios=test_scenarios
        )
        
        return task


# Global instance of the task generator
task_generator = TaskGenerator()