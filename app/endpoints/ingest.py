# app/endpoints/ingest.py
from fastapi import APIRouter, HTTPException
from connectors.jira import fetch_jira_issues
from pipeline import run_pipeline
from config import settings
from pymongo import MongoClient

router = APIRouter()

def insert_to_mongo(data: list):
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]
    collection = db[settings.COLLECTION_NAME]
    collection.insert_many(data)

@router.get("/ingest/jira")
def ingest_jira():
    try:
        issues = fetch_jira_issues()
        if not issues:
            raise Exception("No issues retrieved from Jira.")

        all_units = []
        for issue in issues:
            issue_key = issue.get("key", "unknown")
            fields = issue.get("fields", {})
            summary = fields.get("summary", "")
            description = fields.get("description", "")
            raw_text = f"Summary: {summary}\nDescription: {description}"
            knowledge_units = run_pipeline(raw_text, source_id=issue_key)
            # Optionally tag each unit with its source (here, Jira issue key)
            for unit in knowledge_units:
                unit["source_audio_id"] = issue_key
            all_units.extend(knowledge_units)

        insert_to_mongo(all_units)
        return {"status": "success", "inserted_count": len(all_units)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
