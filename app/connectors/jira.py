# app/connectors/jira.py
import requests
from config import settings

def fetch_jira_issues():
    api_endpoint = f"{settings.JIRA_BASE_URL}/rest/api/3/search"
    params = {
        "jql": settings.JQL_QUERY,
        "maxResults": 50,
        "fields": "summary,description,created,updated,reporter,issuetype"
    }
    response = requests.get(
        api_endpoint,
        params=params,
        auth=(settings.JIRA_USERNAME, settings.JIRA_API_TOKEN),  # using JIRA_EMAIL for clarity
        headers={"Accept": "application/json"}
    )
    # Debug logging:
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    
    if response.status_code != 200:
        raise Exception(f"Error from Jira: {response.status_code} - {response.text}")
    return response.json().get("issues", [])
