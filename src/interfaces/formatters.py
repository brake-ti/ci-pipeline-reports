from typing import List, Dict, Any
from tabulate import tabulate
from src.domain.models import ExplanationResponse

def _extract_semgrep_issues(details: List[Dict[str, Any]]) -> List[List[str]]:
    issues = []
    # details is a list of "runs" (SARIF)
    for run in details:
        results = run.get("results", [])
        for res in results:
            rule_id = res.get("ruleId", "N/A")
            message = res.get("message", {}).get("text", "N/A")
            
            locs = res.get("locations", [])
            if locs:
                phy_loc = locs[0].get("physicalLocation", {})
                file_path = phy_loc.get("artifactLocation", {}).get("uri", "N/A")
                line = phy_loc.get("region", {}).get("startLine", "N/A")
            else:
                file_path = "N/A"
                line = "N/A"
            
            issues.append([rule_id, file_path, str(line), message])
    return issues

def format_semgrep_text(response: ExplanationResponse) -> str:
    issues = _extract_semgrep_issues(response.details)
    lines = ["Semgrep Analysis Report", "=" * 23, f"{response.summary}", ""]
    
    for idx, issue in enumerate(issues, 1):
        lines.append(f"Issue #{idx}:")
        lines.append(f"  Rule: {issue[0]}")
        lines.append(f"  File: {issue[1]}:{issue[2]}")
        lines.append(f"  Message: {issue[3]}")
        lines.append("")
        
    return "\n".join(lines)

def format_semgrep_table(response: ExplanationResponse) -> str:
    issues = _extract_semgrep_issues(response.details)
    headers = ["Rule ID", "File", "Line", "Message"]
    return tabulate(issues, headers=headers, tablefmt="grid")

def _extract_gitleaks_issues(details: List[Dict[str, Any]]) -> List[List[str]]:
    issues = []
    # details is a flat list of secrets (normalized in Use Case)
    for secret in details:
        rule_id = secret.get("RuleID", "N/A")
        file_path = secret.get("File", "N/A")
        line = secret.get("StartLine", "N/A")
        commit = secret.get("Commit", "N/A")
        secret_val = secret.get("Secret", "***")
        # Mask secret for display
        if len(secret_val) > 4:
            masked_secret = f"{secret_val[:2]}...{secret_val[-2:]}"
        else:
            masked_secret = "***"
            
        issues.append([rule_id, file_path, str(line), commit, masked_secret])
    return issues

def format_gitleaks_text(response: ExplanationResponse) -> str:
    issues = _extract_gitleaks_issues(response.details)
    lines = ["Gitleaks Analysis Report", "=" * 24, f"{response.summary}", ""]
    
    for idx, issue in enumerate(issues, 1):
        lines.append(f"Secret #{idx}:")
        lines.append(f"  Rule: {issue[0]}")
        lines.append(f"  Location: {issue[1]}:{issue[2]}")
        lines.append(f"  Commit: {issue[3]}")
        lines.append(f"  Secret: {issue[4]}")
        lines.append("")
        
    return "\n".join(lines)

def format_gitleaks_table(response: ExplanationResponse) -> str:
    issues = _extract_gitleaks_issues(response.details)
    headers = ["Rule ID", "File", "Line", "Commit", "Secret"]
    return tabulate(issues, headers=headers, tablefmt="grid")
