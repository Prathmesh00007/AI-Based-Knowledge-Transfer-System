# 🧠 AI-Driven Knowledge Transfer Assistant

A production-ready AI-based knowledge transfer system designed to automate the onboarding and handover process by extracting, summarizing, organizing, and making searchable key project knowledge from tools like **Jira** and **Confluence**.

---

## 📌 Overview

Knowledge transfer during employee onboarding or transition periods is often time-consuming and error-prone. This system leverages **Natural Language Processing (NLP)** and **LLMs** to streamline this process, ensuring that vital institutional knowledge is **captured, categorized, and queryable** — all from one central dashboard.

> 🔍 Connect. Extract. Summarize. Search. Ask.

---

## 🧪 Key Features

- 🔗 **Integration with Jira & Confluence APIs**
- 🧠 **AI Pipeline** for:
  - Sentence Tokenization
  - MiniLM Embeddings
  - Agglomerative Clustering
  - BART-based Summarization
  - BERT-based NER Tagging
  - Sentence-BERT for Semantic Search
- 📊 **Dashboard** with categorized, searchable summaries
- 💬 **Chatbot** interface for Q&A on internal knowledge base
- ⚙️ **Modular Backend** using FastAPI & MongoDB
- 🔎 **FAISS Vector Indexing** for semantic retrieval

---

## 🧠 Research Motivation

Enterprises face major friction during transitions due to lack of structured documentation. Often, tribal knowledge is lost with team movement. By integrating LLMs and retrieval systems, this project ensures:

- **Structured retention** of critical knowledge.
- **Efficient onboarding** through contextual access.
- **Semantic similarity** search over large document corpora.

This approach is inspired by academic principles in **semantic information retrieval**, **extractive & abstractive summarization**, and **contextual entity extraction**.

---

## 📂 Project Structure

```bash
├── ai_pipeline/
│   ├── tokenizer.py         # spaCy sentence tokenizer
│   ├── embedder.py          # MiniLM/Sentence-BERT embedding generation
│   ├── clusterer.py         # Agglomerative clustering
│   ├── summarizer.py        # BART-based summarizer
│   ├── ner.py               # BERT-based NER tagging
│   └── indexer.py           # FAISS vector index builder
│
├── connectors/
│   ├── jira_fetcher.py      # Jira REST API integration
│   ├── confluence_fetcher.py# Confluence API integration
│
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── routes/
│   │   ├── summarize.py     # Endpoint for processing knowledge
│   │   └── chatbot.py       # Endpoint for Q&A
│   └── db.py                # MongoDB models
│
├── dashboard/
│   └── frontend/            # React-based UI (or Streamlit alternative)
│       ├── App.js
│       ├── components/
│       └── pages/
│
├── chatbot/
│   └── qna_agent.py         # Semantic search + LLM response
│
├── requirements.txt
├── README.md
└── .env.example
