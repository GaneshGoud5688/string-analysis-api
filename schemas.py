from pydantic import BaseModel
from typing import Dict, Any

class AnalysisResponse(BaseModel):
    """
    Response model containing the results of the analysis.
    """
    results: Dict[str, Any]
