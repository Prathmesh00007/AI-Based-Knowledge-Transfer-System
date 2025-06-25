from fastapi import APIRouter, HTTPException
import numpy as np
import faiss
from pymongo import MongoClient
from config import settings
from pipeline import embed_model  # This is the SentenceTransformer model loaded in your pipeline

router = APIRouter()

def get_mongo_documents() -> list:
    """
    Retrieve all knowledge units from MongoDB.
    """
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]
    collection = db[settings.COLLECTION_NAME]
    docs = list(collection.find())
    client.close()
    return docs

def build_faiss_index(documents: list, embedding_dim: int = 384):
    """
    Build a FAISS index from the 'embedding' arrays stored in the documents.
    Returns the index along with a list of the valid documents.
    """
    embeddings = []
    valid_docs = []
    for doc in documents:
        # Only include documents that have an embedding
        if "embedding" in doc:
            embeddings.append(doc["embedding"])
            valid_docs.append(doc)
    if not embeddings:
        raise ValueError("No valid embeddings found in documents.")
    
    embeddings_np = np.array(embeddings).astype("float32")
    # Normalize vectors to unit length for cosine similarity via inner product.
    faiss.normalize_L2(embeddings_np)
    index = faiss.IndexFlatIP(embedding_dim)
    index.add(embeddings_np)
    return index, valid_docs

def search_faiss(query: str, top_k: int = 3):
    """
    Perform semantic search for the given query string.
    This function encodes the query, builds a FAISS index from stored documents,
    and then retrieves the top_k closest documents.
    """
    # Encode the query into an embedding vector.
    query_embedding = embed_model.encode(query)
    query_embedding = np.array(query_embedding, dtype="float32").reshape(1, -1)
    faiss.normalize_L2(query_embedding)

    # Fetch all documents from MongoDB.
    documents = get_mongo_documents()
    if not documents:
        return [], []

    # Build the FAISS index over the stored embeddings.
    index, valid_docs = build_faiss_index(documents, embedding_dim=384)
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    scores = distances[0].tolist()
    for idx in indices[0]:
        # Check that the index is within range
        if idx < len(valid_docs):
            results.append(valid_docs[idx])
    return results, scores

@router.get("/search")
def search_endpoint(query: str, top_k: int = 3):
    """
    API Endpoint to perform semantic search.
    It accepts a query string and an optional parameter top_k to control
    the number of search results.
    Returns the status and a list of matching knowledge units with their scores.
    """
    try:
        results, scores = search_faiss(query, top_k=top_k)
        response = []
        for doc, score in zip(results, scores):
            response.append({
                "id": doc.get("id"),
                "chunk_text": doc.get("chunk_text"),
                "summary": doc.get("summary"),
                "tags": doc.get("tags"),
                "timestamp": doc.get("timestamp"),
                "score": score,
            })
        response.sort(key=lambda x: x["score"], reverse=True)
        return {"status": "success", "results": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
