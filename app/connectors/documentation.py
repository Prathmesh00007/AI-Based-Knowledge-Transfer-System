# app/connectors/documentation.py

import requests
from config import settings

def fetch_documentation_page(page_id: str) -> dict:
    """
    Fetch a Confluence page by its ID using Confluence REST API and the export view,
    so we don't need to perform HTML scraping.
    Reuses Jira credentials since they share the same Atlassian workspace.
    """
    url = f"{settings.JIRA_BASE_URL}/wiki/rest/api/content/{page_id}?expand=body.export_view,version,metadata.labels"
    auth = (settings.JIRA_USERNAME, settings.JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, auth=auth, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page {page_id}: {response.status_code} - {response.text}")
    
    data = response.json()
    text_content = data.get("body", {}).get("export_view", {}).get("value", "")
    
    page_info = {
        "id": data.get("id"),
        "title": data.get("title"),
        "version": data.get("version", {}).get("number", 1),
        "labels": [lbl.get("name") for lbl in data.get("metadata", {}).get("labels", {}).get("results", [])],
        "text": text_content
    }
    print(f"Fetched page {page_info['id']} - {page_info['title']}")
    return page_info

def list_confluence_pages(space_key: str, limit: int = 10) -> list:
    """
    List Confluence pages in a given space using a CQL query.
    Uses the search API endpoint which returns a list of results.
    """
    url = f"{settings.JIRA_BASE_URL}/wiki/rest/api/content/search"
    # CQL: list pages in the given space that are of type 'page'
    params = {
        "cql": f"space = \"{space_key}\" AND type = page",
        "limit": limit,
        "expand": "body.export_view,version,metadata.labels"
    }
    auth = (settings.JIRA_USERNAME, settings.JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, auth=auth, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list pages for space {space_key}: {response.status_code} - {response.text}")
    
    data = response.json()
    print(f"Found {len(data.get('results', []))} pages in space '{space_key}'")
    return data.get("results", [])
