from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_explain_semgrep():
    payload = {"runs": [{"results": [{"ruleId": "test-rule", "message": {"text": "test msg"}, "locations": [{"physicalLocation": {"artifactLocation": {"uri": "test.py"}, "region": {"startLine": 1}}}]}]}]}
    
    # Test JSON
    response = client.post("/v1/explain/semgrep?output=json", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Semgrep analysis found 1 issues" in data["summary"]
    
    # Test Table
    response = client.post("/v1/explain/semgrep?output=table", json=payload)
    assert response.status_code == 200
    assert "test-rule" in response.text
    assert "test.py" in response.text

def test_explain_gitleaks():
    payload = [{"RuleID": "aws-key", "File": "config.py", "StartLine": 10, "Secret": "SECRET123", "Commit": "abc"}]
    
    # Test JSON
    response = client.post("/v1/explain/gitleaks?output=json", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Gitleaks found 1 secrets" in data["summary"]
    
    # Test Text
    response = client.post("/v1/explain/gitleaks?output=text", json=payload)
    assert response.status_code == 200
    assert "Gitleaks Analysis Report" in response.text
    assert "aws-key" in response.text
