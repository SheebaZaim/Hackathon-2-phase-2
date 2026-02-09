import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import csv

from ..models.verification_report import VerificationReport, ComponentStatus
from ..utils.logger import verification_logger


class ReportGenerator:
    """
    Service to generate various types of verification reports
    """
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_json_report(self, report: VerificationReport, filename: str = None) -> str:
        """
        Generate a JSON report from a VerificationReport object
        """
        if not filename:
            filename = f"verification_report_{report.id}.json"
        
        filepath = self.output_dir / filename
        
        # Convert the report to a dictionary
        report_dict = {
            "id": report.id,
            "timestamp": report.timestamp,
            "version": report.version,
            "components_checked": [
                {
                    "name": comp.name,
                    "status": comp.status,
                    "details": comp.details,
                    "compliant": comp.compliant,
                    "errors": comp.errors,
                    "warnings": comp.warnings
                } for comp in report.components_checked
            ],
            "total_components": report.total_components,
            "passed_components": report.passed_components,
            "failed_components": report.failed_components,
            "missing_components": report.missing_components,
            "compliance_score": report.compliance_score,
            "overall_status": report.overall_status
        }
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        verification_logger.info(f"JSON report generated: {filepath}")
        return str(filepath)
    
    def generate_text_report(self, report: VerificationReport, filename: str = None) -> str:
        """
        Generate a human-readable text report
        """
        if not filename:
            filename = f"verification_report_{report.id}.txt"
        
        filepath = self.output_dir / filename
        
        # Create the text report
        lines = [
            f"VERIFICATION REPORT",
            f"==================",
            f"",
            f"Report ID: {report.id}",
            f"Generated: {report.timestamp}",
            f"Version: {report.version}",
            f"",
            f"SUMMARY:",
            f"--------",
            f"- Total Components: {report.total_components}",
            f"- Passed: {report.passed_components}",
            f"- Failed: {report.failed_components}",
            f"- Missing: {report.missing_components}",
            f"- Compliance Score: {report.compliance_score:.2f}%",
            f"- Overall Status: {report.overall_status}",
            f"",
            f"DETAILED RESULTS:",
            f"----------------",
        ]
        
        for component in report.components_checked:
            lines.append(f"")
            lines.append(f"Component: {component.name}")
            lines.append(f"  Status: {component.status}")
            lines.append(f"  Details: {component.details}")
            lines.append(f"  Compliant: {'Yes' if component.compliant else 'No'}")
            
            if component.errors:
                lines.append(f"  Errors: {', '.join(component.errors)}")
            
            if component.warnings:
                lines.append(f"  Warnings: {', '.join(component.warnings)}")
        
        # Add a specific section for missing components
        missing_components = [comp for comp in report.components_checked if comp.status == "missing"]
        if missing_components:
            lines.append(f"")
            lines.append(f"MISSING COMPONENTS DETAILS:")
            lines.append(f"---------------------------")
            for comp in missing_components:
                lines.append(f"- {comp.name}: {comp.details}")
                if comp.errors:
                    for error in comp.errors:
                        lines.append(f"    Error: {error}")
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        verification_logger.info(f"Text report generated: {filepath}")
        return str(filepath)
    
    def generate_csv_report(self, report: VerificationReport, filename: str = None) -> str:
        """
        Generate a CSV report
        """
        if not filename:
            filename = f"verification_report_{report.id}.csv"
        
        filepath = self.output_dir / filename
        
        # Prepare data for CSV
        rows = []
        rows.append([
            "Component Name", 
            "Status", 
            "Details", 
            "Compliant", 
            "Errors", 
            "Warnings"
        ])
        
        for component in report.components_checked:
            rows.append([
                component.name,
                component.status,
                component.details,
                component.compliant,
                '; '.join(component.errors) if component.errors else '',
                '; '.join(component.warnings) if component.warnings else ''
            ])
        
        # Write to CSV file
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
        
        verification_logger.info(f"CSV report generated: {filepath}")
        return str(filepath)
    
    def generate_summary_report(self, reports: List[VerificationReport], filename: str = None) -> str:
        """
        Generate a summary report comparing multiple verification reports
        """
        if not filename:
            filename = f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = self.output_dir / filename
        
        # Create the summary report
        lines = [
            f"VERIFICATION SUMMARY REPORT",
            f"===========================",
            f"",
            f"Generated: {datetime.now().isoformat()}",
            f"Total Reports: {len(reports)}",
            f"",
            f"REPORT COMPARISON:",
            f"-----------------",
        ]
        
        for i, report in enumerate(reports):
            lines.append(f"")
            lines.append(f"Report {i+1}: {report.id}")
            lines.append(f"  Date: {report.timestamp}")
            lines.append(f"  Version: {report.version}")
            lines.append(f"  Passed: {report.passed_components}/{report.total_components}")
            lines.append(f"  Compliance: {report.compliance_score:.2f}%")
            lines.append(f"  Status: {report.overall_status}")
        
        # Add trend analysis if we have multiple reports
        if len(reports) > 1:
            lines.append(f"")
            lines.append(f"TREND ANALYSIS:")
            lines.append(f"---------------")
            
            # Sort reports by timestamp
            sorted_reports = sorted(reports, key=lambda r: r.timestamp)
            
            first_report = sorted_reports[0]
            latest_report = sorted_reports[-1]
            
            lines.append(f"Initial Compliance: {first_report.compliance_score:.2f}%")
            lines.append(f"Latest Compliance: {latest_report.compliance_score:.2f}%")
            
            improvement = latest_report.compliance_score - first_report.compliance_score
            lines.append(f"Improvement: {improvement:+.2f}%")
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        verification_logger.info(f"Summary report generated: {filepath}")
        return str(filepath)
    
    def generate_html_report(self, report: VerificationReport, filename: str = None) -> str:
        """
        Generate an HTML report
        """
        if not filename:
            filename = f"verification_report_{report.id}.html"
        
        filepath = self.output_dir / filename
        
        # Create the HTML report
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verification Report - {report.id}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007acc;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .component {{
            border: 1px solid #ddd;
            margin: 10px 0;
            border-radius: 5px;
            overflow: hidden;
        }}
        .component-header {{
            padding: 10px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .status-pass {{
            background-color: #d4edda;
            color: #155724;
        }}
        .status-fail {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .status-missing {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .status-warning {{
            background-color: #cce7ff;
            color: #004085;
        }}
        .component-details {{
            padding: 10px;
            background-color: #fafafa;
        }}
        .errors {{
            color: #dc3545;
            font-size: 0.9em;
        }}
        .warnings {{
            color: #ffc107;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Verification Report</h1>
        
        <div class="summary">
            <h2>Summary</h2>
            <p><strong>Report ID:</strong> {report.id}</p>
            <p><strong>Generated:</strong> {report.timestamp}</p>
            <p><strong>Version:</strong> {report.version}</p>
            <p><strong>Total Components:</strong> {report.total_components}</p>
            <p><strong>Passed:</strong> {report.passed_components}</p>
            <p><strong>Failed:</strong> {report.failed_components}</p>
            <p><strong>Missing:</strong> {report.missing_components}</p>
            <p><strong>Compliance Score:</strong> {report.compliance_score:.2f}%</p>
            <p><strong>Overall Status:</strong> {report.overall_status}</p>
        </div>
        
        <h2>Detailed Results</h2>
"""
        
        for component in report.components_checked:
            # Determine status class
            status_class = f"status-{component.status}"
            
            html_content += f"""
        <div class="component">
            <div class="component-header {status_class}">
                <span>{component.name}</span>
                <span>Status: {component.status.upper()}</span>
            </div>
            <div class="component-details">
                <p><strong>Details:</strong> {component.details}</p>
                <p><strong>Compliant:</strong> {'Yes' if component.compliant else 'No'}</p>
"""
            
            if component.errors:
                html_content += f"""                <div class="errors"><strong>Errors:</strong> {', '.join(component.errors)}</div>\n"""
            
            if component.warnings:
                html_content += f"""                <div class="warnings"><strong>Warnings:</strong> {', '.join(component.warnings)}</div>\n"""
            
            html_content += """            </div>
        </div>
"""
        
        html_content += """    </div>
</body>
</html>"""
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        verification_logger.info(f"HTML report generated: {filepath}")
        return str(filepath)


# Global instance of the report generator
report_generator = ReportGenerator()