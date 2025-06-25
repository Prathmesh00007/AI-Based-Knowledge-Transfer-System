import os
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import requests
import json
from pathlib import Path

class LocalRAGSystem:
    def __init__(self):
        # Initialize the embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="chroma_db",
            anonymized_telemetry=False
        ))
        
        # Create or get the collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Ollama API endpoint
        self.ollama_endpoint = "http://localhost:11434/api/generate"
        
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        return self.embedding_model.encode(texts).tolist()
    
    def add_documents(self, texts: List[str], metadata: List[Dict] = None):
        """Add documents to the vector database."""
        if metadata is None:
            metadata = [{"source": f"doc_{i}"} for i in range(len(texts))]
            
        embeddings = self.create_embeddings(texts)
        ids = [f"doc_{i}" for i in range(len(texts))]
        
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadata,
            ids=ids
        )
    
    def query_llm(self, prompt: str) -> str:
        """Query the local LLM using Ollama."""
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(self.ollama_endpoint, json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            raise Exception(f"Error querying LLM: {response.text}")
    
    def retrieve_relevant_documents(self, query: str, n_results: int = 3) -> List[str]:
        """Retrieve relevant documents for a query."""
        query_embedding = self.create_embeddings([query])[0]
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results["documents"][0]
    
    def answer_question(self, question: str) -> str:
        """Answer a question using RAG."""
        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_documents(question)
        
        # Construct the prompt
        context = "\n".join(relevant_docs)
        prompt = f"""Based on the following context, please answer the question. If the context doesn't contain relevant information, say so.

Context:
{context}

Question: {question}

Answer:"""
        
        # Get answer from LLM
        return self.query_llm(prompt)

def main():
    # Initialize the RAG system
    rag = LocalRAGSystem()
    
    # Example documents (you can replace these with your own)
    sample_documents = [
        "Python is a high-level programming language known for its simplicity and readability.",
        "Machine learning is a subset of artificial intelligence that focuses on training models to make predictions.",
        "Vector databases are specialized databases designed to store and search vector embeddings efficiently."
    ]
    
    # Add documents to the system
    rag.add_documents(sample_documents)
    
    # Interactive question answering
    print("Welcome to the Local RAG System!")
    print("Type 'quit' to exit.")
    
    while True:
        question = input("\nEnter your question: ")
        if question.lower() == 'quit':
            break
            
        try:
            answer = rag.answer_question(question)
            print("\nAnswer:", answer)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 