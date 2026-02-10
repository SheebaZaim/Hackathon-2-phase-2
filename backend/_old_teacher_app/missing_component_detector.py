from typing import Dict, List, Any
from datetime import datetime
from uuid import uuid4

from ..utils.component_detector import ComponentDetector, ComponentType
from ..models.verification_report import ComponentStatus, StatusEnum
from ..utils.logger import verification_logger


class MissingComponentDetector:
    """
    Service to detect missing components in the project
    """
    
    def __init__(self, project_root: str = "."):
        self.component_detector = ComponentDetector(project_root)
    
    async def detect_missing_components(self) -> List[ComponentStatus]:
        """
        Detect components that are expected but missing from the project
        """
        try:
            missing_components = self.component_detector.find_missing_expected_components()
            
            results = []
            for comp in missing_components:
                results.append(ComponentStatus(
                    name=comp["name"],
                    status=StatusEnum.MISSING,
                    details=f"Expected component '{comp['name']}' is missing: {comp['reason']}",
                    compliant=False,
                    errors=[comp["reason"]],
                    warnings=[]
                ))
            
            verification_logger.info(f"Detected {len(results)} missing components")
            return results
        except Exception as e:
            verification_logger.error(f"Error detecting missing components: {str(e)}")
            raise e
    
    async def detect_all_components_with_status(self) -> List[ComponentStatus]:
        """
        Detect all components and return their status (present/missing)
        """
        try:
            all_detected = self.component_detector.detect_all_components()
            missing_components = self.component_detector.find_missing_expected_components()
            
            results = []
            
            # Add all detected components as present
            for comp_type, components in all_detected.items():
                for comp in components:
                    results.append(ComponentStatus(
                        name=comp["name"],
                        status=StatusEnum.PASS,
                        details=f"Component '{comp['name']}' is present at {comp['path']}",
                        compliant=True,
                        errors=[],
                        warnings=[]
                    ))
            
            # Add missing components
            for comp in missing_components:
                results.append(ComponentStatus(
                    name=comp["name"],
                    status=StatusEnum.MISSING,
                    details=f"Expected component '{comp['name']}' is missing: {comp['reason']}",
                    compliant=False,
                    errors=[comp["reason"]],
                    warnings=[]
                ))
            
            verification_logger.info(f"Detected {len(all_detected)} component types and {len(missing_components)} missing components")
            return results
        except Exception as e:
            verification_logger.error(f"Error detecting all components: {str(e)}")
            raise e
    
    async def get_component_summary(self) -> Dict[str, Any]:
        """
        Get a summary of detected components
        """
        try:
            summary = self.component_detector.get_component_summary()
            missing = self.component_detector.find_missing_expected_components()
            
            result = {
                "detected": summary,
                "missing_count": len(missing),
                "missing_details": missing,
                "total_detected": sum(summary.values()),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return result
        except Exception as e:
            verification_logger.error(f"Error getting component summary: {str(e)}")
            raise e
    
    def get_expected_components(self) -> Dict[str, List[str]]:
        """
        Get a list of components expected in a typical web application
        """
        expected = {
            ComponentType.FRONTEND.value: [
                "package.json",
                "src/",
                "public/",
                "index.html",
                "styles.css"
            ],
            ComponentType.BACKEND.value: [
                "requirements.txt",
                "src/",
                "tests/",
                "main.py",
                "app.py"
            ],
            ComponentType.CONFIGURATION.value: [
                ".env",
                "config/",
                "settings.py",
                "environment variables"
            ],
            ComponentType.TEST.value: [
                "tests/",
                "test_*.py",
                "*_test.py",
                "jest.config.js",
                "pytest.ini"
            ],
            ComponentType.DEPENDENCY.value: [
                "package.json",
                "requirements.txt",
                "yarn.lock",
                "Pipfile"
            ],
            ComponentType.DOCUMENTATION.value: [
                "README.md",
                "LICENSE",
                "CHANGELOG.md",
                "CONTRIBUTING.md"
            ]
        }
        
        return expected


# Global instance of the missing component detector
missing_component_detector = MissingComponentDetector()