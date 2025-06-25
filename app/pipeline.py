# app/pipeline.py
import re
import uuid
import datetime
import spacy
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from sklearn.cluster import AgglomerativeClustering

# Cache models — load these once on startup.
nlp = spacy.load("en_core_web_sm")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialize the NER pipeline.
# Using aggregation_strategy="simple" groups tokens into one entity.
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def extract_tags(text: str) -> list:
    """
    Extract and normalize NER tags from the provided text.
    
    Args:
        text (str): The input text.
        
    Returns:
        list: A list of unique, lowercase NER tags (e.g., 'org', 'per', etc.).
    """
    entities = ner_pipeline(text)
    print("NER Entities:", entities)  # Debug: Check what entities are detected
    tags = []
    for entity in entities:
        # Use the aggregated entity group if available
        tag = entity.get("entity_group") or entity.get("entity")
        if tag:
            tags.append(tag.lower())
    return list(set(tags))


def preprocess_text(text: str) -> str:
    """Clean up and normalize whitespace."""
    return re.sub(r'\s+', ' ', text).strip()

def spacy_sentence_tokenize(text: str) -> list:
    """Tokenize text into sentences using spaCy."""
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

def cluster_chunks(sentences: list, distance_threshold: float = 0.35) -> list:
    if not sentences:
        return []
    embeddings = embed_model.encode(sentences)
    if len(sentences) == 1:
        return sentences
    clustering_model = AgglomerativeClustering(
        n_clusters=None,
        metric="cosine",
        linkage="average",
        distance_threshold=distance_threshold,
    )
    cluster_labels = clustering_model.fit_predict(embeddings)
    chunks = {}
    for idx, label in enumerate(cluster_labels):
        chunks.setdefault(label, []).append(sentences[idx])
    sorted_labels = sorted(chunks.keys(), key=lambda lab: next(i for i, l in enumerate(cluster_labels) if l == lab))
    chunk_list = [" ".join(chunks[label]) for label in sorted_labels]
    return chunk_list

def summarize_chunks(chunks: list) -> list:
    results = []
    for chunk in chunks:
        if len(chunk.split()) < 30:
            summary = chunk  # Too short to summarize
        else:
            summary_res = summarizer_pipeline(chunk, max_length=60, min_length=15, do_sample=False)
            summary = summary_res[0]['summary_text']
        results.append({
            "chunk_text": chunk,
            "summary": summary
        })
    return results

def package_for_db(summaries: list, source_id: str, source: str = "Jira") -> list:
    """
    Package each summarized chunk into a document suitable for database storage.
    Now enriched with NER tags extracted from the chunk's text.
    """
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    output = []
    for item in summaries:
        ner_tags = extract_tags(item["chunk_text"])
        output.append({
            "id": str(uuid.uuid4()),
            "chunk_text": item["chunk_text"],
            "summary": item["summary"],
            "timestamp": timestamp,
            "speaker": source,
            "tags": ner_tags,  # NER-derived tags
            "source_audio_id": source_id
        })
    return output

def add_embeddings(data: list) -> list:
    """Compute and insert semantic embeddings into each document."""
    for item in data:
        item["embedding"] = embed_model.encode(item["chunk_text"]).tolist()
    return data

def run_pipeline(raw_text: str, source_id: str) -> list:
    """
    Run the entire ingestion pipeline:
      - Clean and preprocess input text.
      - Tokenize into sentences.
      - Cluster sentences into chunks.
      - Summarize each chunk.
      - Package results for the database (including extracting NER tags).
    """
    clean_text = preprocess_text(raw_text)
    sentences = spacy_sentence_tokenize(clean_text)
    chunks = cluster_chunks(sentences)
    summaries = summarize_chunks(chunks)
    packaged_data = package_for_db(summaries, source_id)
    packaged_data = add_embeddings(packaged_data)
    return packaged_data
