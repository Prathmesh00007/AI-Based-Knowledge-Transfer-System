# app/connectors/documentation.py

import requests
from bs4 import BeautifulSoup
from app.config import settings

def fetch_documentation_page(page_id: str) -> dict:
    """
    Fetch a Confluence page by its ID and return a dictionary containing:
      - id: the Confluence page ID.
      - title: the page title.
      - version: the current version number of the page.
      - labels: a list of labels (if any) attached to the page.
      - text: plain text extracted from the page's HTML content.
    
    This data can then be processed by your NLP pipeline for further enrichment.
    """
    url = f"{settings.CONFLUENCE_BASE_URL}/wiki/rest/api/content/{page_id}?expand=body.storage,version,metadata.labels"
    auth = (settings.CONFLUENCE_USER, settings.CONFLUENCE_API_TOKEN)
    headers = {"Accept": "application/json"}

    response = requests.get(url, auth=auth, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page {page_id}: {response.status_code} - {response.text}")
    
    data = response.json()
    # Extract the HTML content from the 'storage' representation.
    html_content = data.get("body", {}).get("storage", {}).get("value", "")
    # Use BeautifulSoup to strip out the HTML tags and extract raw text.
    soup = BeautifulSoup(html_content, "html.parser")
    text_content = soup.get_text(separator=" ", strip=True)

    page_info = {
        "id": data.get("id"),
        "title": data.get("title"),
        "version": data.get("version", {}).get("number", 1),
        "labels": [lbl.get("name") for lbl in data.get("metadata", {}).get("labels", {}).get("results", [])],
        "text": text_content
    }
    return page_info

# Example usage:
if __name__ == "__main__":
    # Replace '123456' with a valid Confluence page ID from your project.
    try:
        page_data = fetch_documentation_page("123456")
        print("Fetched Documentation Page:")
        print(f"Title: {page_data['title']}")
        print(f"Version: {page_data['version']}")
        print(f"Labels: {page_data['labels']}")
        print(f"Text: {page_data['text'][:300]}...")  # Print the first 300 characters
    except Exception as e:
        print("Error:", str(e))
