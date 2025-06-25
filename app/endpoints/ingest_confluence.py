# app/endpoints/ingest_confluence_bulk.py

from fastapi import APIRouter, HTTPException, Query
from connectors.documentation import fetch_documentation_page, list_confluence_pages
from pipeline import run_pipeline

router = APIRouter()

@router.get("/ingest/confluence/bulk")
def ingest_confluence_bulk(
    space_key: str = Query(..., description="The Confluence space key to ingest"),
    limit: int = Query(10, description="Number of pages to ingest")
):
    """
    Ingest Confluence documentation in bulk by space.
    Instead of entering a single page ID, we search for pages within a space.
    For each page found, we invoke the pipeline to generate enriched documents.
    """
    try:
        pages = list_confluence_pages(space_key, limit)
        if not pages:
            raise HTTPException(status_code=404, detail=f"No pages found in space {space_key}.")
        
        all_documents = []
        for page in pages:
            page_id = page.get("id")
            if page_id:
                page_data = fetch_documentation_page(page_id)
                # Combine title and text (this helps provide context to the pipeline)
                raw_text = f"{page_data['title']}: {page_data['text']}"
                processed_docs = run_pipeline(raw_text, source_id=page_data['id'])
                all_documents.extend(processed_docs)
        return {"status": "success", "data": all_documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
