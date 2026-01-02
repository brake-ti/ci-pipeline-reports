from fastapi import APIRouter, Query, Body
from fastapi.responses import PlainTextResponse
from src.domain.models import GitleaksRequest, ExplanationResponse
from src.use_cases.explain import process_gitleaks_report
from src.interfaces.formatters import format_gitleaks_text, format_gitleaks_table
from typing import List, Dict, Any, Union

router = APIRouter()

@router.post("/gitleaks", response_model=Union[ExplanationResponse, str])
async def explain_gitleaks(
    payload: Union[List[Dict[str, Any]], Dict[str, Any]] = Body(...),
    output: str = Query("json", pattern="^(text|table|json)$")
):
    """
    Analyzes a Gitleaks JSON report (Native or SARIF).
    """
    request = GitleaksRequest(report_content=payload)
    response_data = process_gitleaks_report(request, output)
    
    if output == "text":
        return PlainTextResponse(format_gitleaks_text(response_data))
    elif output == "table":
        return PlainTextResponse(format_gitleaks_table(response_data))
        
    return response_data
