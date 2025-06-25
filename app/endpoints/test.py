# app/endpoints/test.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pipeline import run_pipeline

router = APIRouter()

class PipelineTestRequest(BaseModel):
    raw_text: str
    source_id: str = "manual_test"  # default source_id for testing

@router.post("/test/pipeline")
def test_pipeline(request: PipelineTestRequest):
    """
    Endpoint to test the complete pipeline.
    Expects a JSON payload with 'raw_text' (required) and 'source_id' (optional),
    then processes the text through the pipeline (including summarization and NER tagging)
    and returns the enriched documents.
    """
    if not request.raw_text:
        raise HTTPException(status_code=400, detail="raw_text is required")
    try:
        result = run_pipeline(request.raw_text, request.source_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
