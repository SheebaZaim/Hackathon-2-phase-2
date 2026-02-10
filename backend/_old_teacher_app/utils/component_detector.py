import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum


class ComponentType(Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    CONFIGURATION = "configuration"
    DOCUMENTATION = "documentation"
    TEST = "test"
    DEPENDENCY = "dependency"


class ComponentDetector:
    """
    Utility class to detect various components in the project
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.frontend_extensions = ['.js', '.jsx', '.ts', '.tsx', '.vue', '.html', '.css', '.scss']
        self.backend_extensions = ['.py', '.java', '.cs', '.rb', '.php']
        self.config_extensions = ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.env']
        self.test_extensions = ['.test.js', '.spec.js', '_test.py', 'test_', 'spec.rb']
    
    def detect_frontend_components(self) -> List[Dict[str, Any]]:
        """
        Detect frontend components in the project
        """
        components = []
        
        # Look for frontend directories
        frontend_dirs = ['frontend', 'client', 'public', 'static', 'assets']
        
        for directory in frontend_dirs:
            dir_path = self.project_root / directory
            if dir_path.exists():
                files = []
                for ext in self.frontend_extensions:
                    files.extend(list(dir_path.rglob(f"*{ext}")))
                
                for file_path in files:
                    components.append({
                        "name": file_path.name,
                        "path": str(file_path.relative_to(self.project_root)),
                        "type": ComponentType.FRONTEND.value,
                        "size": file_path.stat().st_size,
                        "last_modified": file_path.stat().st_mtime
                    })
        
        return components
    
    def detect_backend_components(self) -> List[Dict[str, Any]]:
        """
        Detect backend components in the project
        """
        components = []
        
        # Look for backend directories
        backend_dirs = ['backend', 'server', 'api', 'src']
        
        for directory in backend_dirs:
            dir_path = self.project_root / directory
            if dir_path.exists():
                files = []
                for ext in self.backend_extensions:
                    files.extend(list(dir_path.rglob(f"*{ext}")))
                
                for file_path in files:
                    components.append({
                        "name": file_path.name,
                        "path": str(file_path.relative_to(self.project_root)),
                        "type": ComponentType.BACKEND.value,
                        "size": file_path.stat().st_size,
                        "last_modified": file_path.stat().st_mtime
                    })
        
        return components
    
    def detect_configurations(self) -> List[Dict[str, Any]]:
        """
        Detect configuration files in the project
        """
        components = []
        
        # Look for config directories and files
        config_patterns = ['*.json', '*.yaml', '*.yml', '*.toml', '*.ini', '*.cfg', '*.env', '*config*', '*setting*']
        
        for pattern in config_patterns:
            files = list(self.project_root.rglob(pattern))
            for file_path in files:
                # Skip node_modules and other irrelevant directories
                if 'node_modules' in str(file_path) or '.git' in str(file_path):
                    continue
                
                components.append({
                    "name": file_path.name,
                    "path": str(file_path.relative_to(self.project_root)),
                    "type": ComponentType.CONFIGURATION.value,
                    "size": file_path.stat().st_size,
                    "last_modified": file_path.stat().st_mtime
                })
        
        return components
    
    def detect_tests(self) -> List[Dict[str, Any]]:
        """
        Detect test files in the project
        """
        components = []
        
        # Look for test directories and files
        test_dirs = ['tests', 'test', 'spec']
        test_patterns = ['*_test.py', 'test_*.py', '*.test.js', '*.spec.js', '*_spec.rb', 'spec/*']
        
        # Check test directories
        for directory in test_dirs:
            dir_path = self.project_root / directory
            if dir_path.exists():
                # Get all files in test directories
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        components.append({
                            "name": file_path.name,
                            "path": str(file_path.relative_to(self.project_root)),
                            "type": ComponentType.TEST.value,
                            "size": file_path.stat().st_size,
                            "last_modified": file_path.stat().st_mtime
                        })
        
        # Check for test files using patterns
        for pattern in test_patterns:
            files = list(self.project_root.rglob(pattern))
            for file_path in files:
                # Skip node_modules and other irrelevant directories
                if 'node_modules' in str(file_path) or '.git' in str(file_path):
                    continue
                
                # Check if it's not already added from test directories
                if not any(comp['path'] == str(file_path.relative_to(self.project_root)) for comp in components):
                    components.append({
                        "name": file_path.name,
                        "path": str(file_path.relative_to(self.project_root)),
                        "type": ComponentType.TEST.value,
                        "size": file_path.stat().st_size,
                        "last_modified": file_path.stat().st_mtime
                    })
        
        return components
    
    def detect_dependencies(self) -> List[Dict[str, Any]]:
        """
        Detect dependency files in the project
        """
        components = []
        
        # Look for common dependency files
        dep_files = [
            'requirements.txt', 'package.json', 'yarn.lock', 'Gemfile', 'Gemfile.lock',
            'Pipfile', 'Pipfile.lock', 'poetry.lock', 'go.mod', 'go.sum', 'Cargo.toml',
            'Cargo.lock', 'composer.json', 'composer.lock'
        ]
        
        for file_name in dep_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                components.append({
                    "name": file_path.name,
                    "path": str(file_path.relative_to(self.project_root)),
                    "type": ComponentType.DEPENDENCY.value,
                    "size": file_path.stat().st_size,
                    "last_modified": file_path.stat().st_mtime
                })
        
        return components
    
    def detect_documentation(self) -> List[Dict[str, Any]]:
        """
        Detect documentation files in the project
        """
        components = []
        
        # Look for documentation files
        doc_patterns = ['*.md', '*.rst', '*.txt', 'README*', 'CHANGELOG*', 'CONTRIBUTING*', 'LICENSE*']
        
        for pattern in doc_patterns:
            files = list(self.project_root.rglob(pattern))
            for file_path in files:
                # Skip node_modules and other irrelevant directories
                if 'node_modules' in str(file_path) or '.git' in str(file_path):
                    continue
                
                components.append({
                    "name": file_path.name,
                    "path": str(file_path.relative_to(self.project_root)),
                    "type": ComponentType.DOCUMENTATION.value,
                    "size": file_path.stat().st_size,
                    "last_modified": file_path.stat().st_mtime
                })
        
        return components
    
    def detect_all_components(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Detect all types of components in the project
        """
        all_components = {}
        
        all_components[ComponentType.FRONTEND.value] = self.detect_frontend_components()
        all_components[ComponentType.BACKEND.value] = self.detect_backend_components()
        all_components[ComponentType.CONFIGURATION.value] = self.detect_configurations()
        all_components[ComponentType.TEST.value] = self.detect_tests()
        all_components[ComponentType.DEPENDENCY.value] = self.detect_dependencies()
        all_components[ComponentType.DOCUMENTATION.value] = self.detect_documentation()
        
        return all_components
    
    def get_component_summary(self) -> Dict[str, int]:
        """
        Get a summary of detected components by type
        """
        all_components = self.detect_all_components()
        summary = {}
        
        for comp_type, components in all_components.items():
            summary[comp_type] = len(components)
        
        return summary
    
    def find_missing_expected_components(self) -> List[Dict[str, str]]:
        """
        Find components that are expected but missing from the project
        """
        missing = []
        
        # Expected components for a typical web application
        expected_components = {
            ComponentType.FRONTEND: ["package.json", "src/", "public/"],
            ComponentType.BACKEND: ["requirements.txt", "src/", "tests/"],
            ComponentType.CONFIGURATION: [".env", "config/", "settings.py"],
            ComponentType.TEST: ["tests/", "jest.config.js", "pytest.ini"],
            ComponentType.DEPENDENCY: ["package.json", "requirements.txt"],
            ComponentType.DOCUMENTATION: ["README.md", "LICENSE"]
        }
        
        # Check for each expected component
        for comp_type, expected_files in expected_components.items():
            for expected in expected_files:
                if expected.endswith('/'):
                    # It's a directory
                    expected_path = self.project_root / expected.rstrip('/')
                    if not expected_path.exists():
                        missing.append({
                            "name": expected,
                            "type": comp_type.value,
                            "reason": "Expected directory does not exist"
                        })
                else:
                    # It's a file - look for it anywhere in the project
                    found = False
                    for file_path in self.project_root.rglob(expected):
                        if file_path.is_file():
                            found = True
                            break
                    
                    if not found:
                        missing.append({
                            "name": expected,
                            "type": comp_type.value,
                            "reason": "Expected file does not exist"
                        })
        
        return missing


# Global instance of the component detector
component_detector = ComponentDetector()