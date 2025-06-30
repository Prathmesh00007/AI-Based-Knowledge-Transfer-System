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

🚀 How It Works
Data Ingestion
Connect to Jira & Confluence using OAuth or API tokens to fetch issue tickets, documentation, and discussions.

Chunking & Embedding
Use spaCy for sentence tokenization. Apply MiniLM/Sentence-BERT to embed each sentence.

Clustering & Summarization
Use Agglomerative Clustering to group semantically similar chunks. Summarize each cluster using BART.

NER Tagging
Apply BERT-based Named Entity Recognition to enrich summaries with relevant tags.

Semantic Indexing
Store summaries and their embeddings in FAISS index and MongoDB for fast semantic retrieval.

Frontend Display
Show categorized knowledge cards in the dashboard, filterable by tags and searchable by text.

Chatbot Q&A
Accept user queries, perform semantic search on the index, pass retrieved context to an LLM (e.g., LLaMA or GPT wrapper), and return relevant answers.

⚙️ Tech Stack
Layer	Tools/Technologies
Language	Python, JavaScript
Backend	FastAPI, MongoDB
AI/NLP	spaCy, MiniLM, Sentence-BERT, BART, BERT, FAISS
Frontend	React.js or Streamlit
Deployment	Docker, Nginx, Gunicorn, Heroku/Vercel
APIs	Atlassian Jira, Atlassian Confluence

🔧 Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/ai-knowledge-transfer.git
cd ai-knowledge-transfer
2. Create and Activate Virtual Environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Up Environment Variables
Copy .env.example to .env and fill in:

bash
Copy
Edit
CONFLUENCE_BASE_URL=
JIRA_BASE_URL=
API_TOKEN=
USERNAME=
MONGODB_URI=
5. Run the FastAPI Backend
bash
Copy
Edit
uvicorn backend.main:app --reload
6. Run the Frontend
If using React:

bash
Copy
Edit
cd dashboard/frontend
npm install
npm start
If using Streamlit:

bash
Copy
Edit
streamlit run dashboard/frontend/app.py
💬 Sample Prompt to Chatbot
pgsql
Copy
Edit
Q: What decisions were made regarding the database schema in Project X?
A: Based on extracted Confluence discussions, the schema was shifted from MySQL to MongoDB due to scalability issues. Refer to Summary #3.
📊 Example Use Cases
🚀 Onboarding a new backend engineer into a microservices project

🔁 Transferring domain knowledge from a resigning team member

🧠 Keeping documentation synchronized with actual task discussions

🤖 Integrating internal project data into a Slack chatbot or search box

✅ Future Enhancements
✅ LangChain-based orchestrator for chaining summaries and Q&A

🔐 Role-based access & SSO integration

🌐 Multilingual support for documentation

📅 Time-aware indexing and document aging

🧑‍💻 Contributors
Prathmesh Abhay Ranade
GitHub · LinkedIn

📄 License
MIT License. See LICENSE for details.

📢 Acknowledgements
Atlassian for Jira & Confluence API documentation

HuggingFace for pre-trained models

FAISS for scalable semantic search

OpenAI & Meta for open LLMs
