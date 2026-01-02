from src.domain.models import SemgrepRequest, GitleaksRequest, ExplanationResponse
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def process_semgrep_sarif(request: SemgrepRequest, output_format: str) -> ExplanationResponse:
    # Mock logic for processing SARIF
    # In a real implementation, this would parse the SARIF JSON structure
    runs = request.sarif_content.get("runs", [])
    issue_count = 0
    for run in runs:
        issue_count += len(run.get("results", []))
    
    response = ExplanationResponse(
        summary=f"Semgrep analysis found {issue_count} issues.",
        details=runs,
        format=output_format
    )
    response.add_link("self", "/v1/explain/semgrep", "POST")
    return response

@circuit(failure_threshold=5, recovery_timeout=60)
def process_gitleaks_report(request: GitleaksRequest, output_format: str) -> ExplanationResponse:
    # Determine if payload is SARIF (dict) or Native (list)
    content = request.report_content
    details = []
    leak_count = 0

    if isinstance(content, dict) and "runs" in content:
        # Handle SARIF format - Normalize to Native format
        runs = content.get("runs", [])
        for run in runs:
            results = run.get("results", [])
            for res in results:
                locations = res.get("locations", [])
                location = locations[0] if locations else {}
                physical_loc = location.get("physicalLocation", {})
                artifact_loc = physical_loc.get("artifactLocation", {})
                region = physical_loc.get("region", {})
                snippet = region.get("snippet", {})
                fingerprints = res.get("partialFingerprints", {})

                normalized_item = {
                    "RuleID": res.get("ruleId", "N/A"),
                    "File": artifact_loc.get("uri", "N/A"),
                    "StartLine": region.get("startLine", 0),
                    "EndLine": region.get("endLine", 0),
                    "StartColumn": region.get("startColumn", 0),
                    "EndColumn": region.get("endColumn", 0),
                    "Secret": snippet.get("text", "***"),
                    "Commit": fingerprints.get("commitSha", "N/A"),
                    "Message": res.get("message", {}).get("text", "N/A"),
                    "Author": fingerprints.get("author", "N/A"),
                    "Email": fingerprints.get("email", "N/A"),
                    "Date": fingerprints.get("date", "N/A")
                }
                details.append(normalized_item)
                leak_count += 1
                
    elif isinstance(content, list):
        # Handle Native JSON format
        leak_count = len(content)
        details = content
    else:
        # Fallback or empty
        details = []

    response = ExplanationResponse(
        summary=f"Gitleaks found {leak_count} secrets.",
        details=details,
        format=output_format
    )
    response.add_link("self", "/v1/explain/gitleaks", "POST")
    return response
