# Knowledge Transfer System

This project implements a full-stack Knowledge Transfer System with a FastAPI backend and a React frontend. It supports semantic search, audio transcription, Jira/Confluence ingestion, and a custom NLP pipeline.

## Features

- **Semantic Search:** Search knowledge units using semantic similarity (FAISS + Sentence Transformers).
- **Jira Ingestion:** Import Jira issues and process them into knowledge units.
- **Confluence Ingestion:** Bulk ingest Confluence documentation by space key.
- **Audio Recording & Transcription:** Record audio and transcribe using Whisper.
- **Pipeline Testing:** Test the NLP pipeline (summarization, NER, embeddings) on custom text.
- **OAuth Login:** Atlassian OAuth2 login for secure access.

## Backend (FastAPI)

- Located in the [`app/`](app/) directory.
- Uses MongoDB for storage, FAISS for vector search, and HuggingFace models for NLP.
- Main entrypoint: [`app/main.py`](app/main.py)
- Endpoints:
  - `/search` — Semantic search
  - `/ingest/jira` — Ingest Jira issues
  - `/ingest/confluence/bulk` — Ingest Confluence docs
  - `/record` — Record and transcribe audio
  - `/test/pipeline` — Test the NLP pipeline
  - `/login` — Atlassian OAuth login

## Frontend (React)

- Located in the [`my-kt-frontend/`](my-kt-frontend/) directory.
- Built with Vite and React.
- Components for search, ingestion, recording, and pipeline testing.

## Setup

### Backend

1. Create a virtual environment and install dependencies:
    ```sh
    cd app
    python -m venv whisper-env
    source whisper-env/bin/activate  # On Windows: whisper-env\Scripts\activate
    pip install -r requirements.txt
    ```

2. Configure credentials in [`app/config.py`](app/config.py).

3. Start MongoDB locally.

4. Run the FastAPI server:
    ```sh
    uvicorn app.main:app --reload
    ```

### Frontend

1. Install dependencies:
    ```sh
    cd my-kt-frontend
    npm install
    ```

2. Start the development server:
    ```sh
    npm run dev
    ```

3. Access the frontend at [http://localhost:5173](http://localhost:5173).

## Project Structure

```
.
├── app/
│   ├── main.py
│   ├── pipeline.py
│   ├── endpoints/
│   ├── connectors/
│   └── ...
├── my-kt-frontend/
│   ├── src/
│   ├── package.json
│   └── ...
├── faiss_search.py
├── rag_system.py
└── README.md
```

## License

MIT License