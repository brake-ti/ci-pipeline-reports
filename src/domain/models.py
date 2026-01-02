from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Link(BaseModel):
    rel: str
    href: str
    method: str

class HateoasModel(BaseModel):
    links: List[Link] = Field(default_factory=list, alias="_links")

    def add_link(self, rel: str, href: str, method: str = "GET"):
        self.links.append(Link(rel=rel, href=href, method=method))

class SemgrepRequest(BaseModel):
    sarif_content: Dict[str, Any]

class GitleaksRequest(BaseModel):
    report_content: Any  # Can be List[Dict] (native) or Dict (SARIF)

class ExplanationResponse(HateoasModel):
    summary: str
    details: List[Dict[str, Any]]
    format: str

class VersionResponse(HateoasModel):
    version: str
    branch: Optional[str] = None
    commit: Optional[str] = None
