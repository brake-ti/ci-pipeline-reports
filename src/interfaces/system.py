from fastapi import APIRouter
from src.domain.models import VersionResponse
import os

router = APIRouter()

@router.get("/version", response_model=VersionResponse)
async def get_version():
    try:
        with open("VERSION", "r") as f:
            version = f.read().strip()
    except FileNotFoundError:
        version = "0.0.0"
        
    response = VersionResponse(
        version=version,
        branch=os.getenv("GIT_BRANCH", "unknown"),
        commit=os.getenv("GIT_COMMIT", "unknown")
    )
    response.add_link("self", "/version", "GET")
    return response
