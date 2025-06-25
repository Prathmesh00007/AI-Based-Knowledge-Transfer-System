import numpy as np
import faiss
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

router = APIRouter()

def get_mongo_documents(uri="mongodb://localhost:27017", db_name="kt_platform", collection_name="knowledge_chunks"):
    """
    Connect to MongoDB and retrieve all documents from the specified collection.
    Each document should already have an "embedding" field.
    """
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    docs = list(collection.find())
    if not docs:
        print("No documents found in the MongoDB collection.")
    return docs

def build_faiss_index(documents, embedding_dim=384):
    """
    Build a FAISS index over the embeddings from the retrieved documents.
    Embeddings are normalized for cosine similarity search.
    """
    embeddings = []
    valid_docs = []  # store only documents that have embeddings

    for doc in documents:
        emb = doc.get("embedding", None)
        if emb is None:
            continue
        embeddings.append(emb)
        valid_docs.append(doc)

    if not embeddings:
        raise ValueError("No valid embeddings were found in the documents.")

    # Convert to NumPy array with type float32
    embeddings_np = np.array(embeddings).astype('float32')
    # Normalize the embeddings if you plan to use Inner Product for cosine similarity
    faiss.normalize_L2(embeddings_np)

    # Create a FAISS index for inner product (cosine similarity when vectors are normalized)
    index = faiss.IndexFlatIP(embedding_dim)
    index.add(embeddings_np)

    return index, valid_docs

def search_faiss(query, model, faiss_index, documents, top_k=3):
    """
    Encode the query, search the FAISS index, and return the top_k matching documents.
    """
    # Compute the query embedding
    query_embedding = model.encode(query)
    query_embedding = np.array(query_embedding, dtype='float32').reshape(1, -1)
    # Normalize the query embedding for cosine similarity
    faiss.normalize_L2(query_embedding)

    # Search the FAISS index
    distances, indices = faiss_index.search(query_embedding, top_k)

    results = []
    scores = distances[0]  # similarity scores
    for idx in indices[0]:
        results.append(documents[idx])
    return results, scores

if __name__ == "__main__":
    # Initialize your SentenceTransformer model. This should match what was used to generate embeddings.
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Retrieve your stored documents (knowledge chunks) from MongoDB
    documents = get_mongo_documents()
    if not documents:
        exit("No documents to search. Please ensure your KUs are inserted in MongoDB with embeddings.")

    # Build a FAISS index over the document embeddings. 
    # For "all-MiniLM-L6-v2", the embedding dimension is 384.
    index, valid_documents = build_faiss_index(documents, embedding_dim=384)
    
    # Prompt the user for a natural language query
    query = input("Enter your search query: ")

    # Perform the FAISS search
    results, scores = search_faiss(query, model, index, valid_documents, top_k=24)
    
    # Display results
    print("\nTop search results:")
    for res, score in zip(results, scores):
        print("-" * 50)
        print(f"Score      : {score:.4f}")
        print(f"ID         : {res.get('id', 'N/A')}")
        print(f"Chunk Text : {res.get('chunk_text', 'N/A')}")
        print(f"Summary    : {res.get('summary', 'N/A')}")
        print(f"Tags       : {res.get('tags', [])}")
        print(f"Timestamp  : {res.get('timestamp', 'N/A')}")
