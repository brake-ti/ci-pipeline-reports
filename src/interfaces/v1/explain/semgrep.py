from fastapi import APIRouter, Query, Body
from fastapi.responses import PlainTextResponse
from src.domain.models import SemgrepRequest, ExplanationResponse
from src.use_cases.explain import process_semgrep_sarif
from src.interfaces.formatters import format_semgrep_text, format_semgrep_table
from typing import Dict, Any, Union

router = APIRouter()

@router.post("/semgrep", response_model=Union[ExplanationResponse, str])
async def explain_semgrep(
    payload: Dict[str, Any] = Body(...),
    output: str = Query("json", pattern="^(text|table|json)$")
):
    """
    Analyzes a Semgrep SARIF report.
    """
    request = SemgrepRequest(sarif_content=payload)
    response_data = process_semgrep_sarif(request, output)
    
    if output == "text":
        return PlainTextResponse(format_semgrep_text(response_data))
    elif output == "table":
        return PlainTextResponse(format_semgrep_table(response_data))
    
    return response_data
