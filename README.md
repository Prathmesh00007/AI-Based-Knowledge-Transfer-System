# Local RAG System

This project implements a local Retrieval Augmented Generation (RAG) system that runs entirely on your machine. It uses local models for both text generation and embeddings, combined with a vector database for efficient information retrieval.

## Prerequisites

1. Python 3.8 or higher
2. Ollama installed (for running local LLMs)
   - Download from: https://ollama.ai/
   - Install and run the Ollama service
   - Pull the Mistral model: `ollama pull mistral`

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a data directory and add your text documents:
```bash
mkdir data
```

## Usage

1. Start the Ollama service (if not already running)
2. Run the main script:
```bash
python rag_system.py
```

## Components

- **Local LLM**: Uses Ollama with Mistral model
- **Embedding Model**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB
- **RAG Implementation**: Custom implementation using LangChain

## Project Structure

```
.
├── README.md
├── requirements.txt
├── rag_system.py
└── data/
    └── sample_documents/
``` 