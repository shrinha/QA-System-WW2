from sentence_transformers import SentenceTransformer
import os
import faiss
import numpy as np
import re
import plotly.express as px
import pandas as pd
import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# =================== Helper Functions ===================

def extract_dates_from_text(text, label):
    """Extracts dates from a single string and tags them with a label (e.g. 'Answer', 'Question')."""
    date_pattern = r"\b(?:\d{1,2}\s)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|" \
                   r"May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|" \
                   r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[ ,\-]*\d{2,4}|\b\d{4}\b"

    matches = re.findall(date_pattern, text)
    return [{"Date": match, "Context": label, "Text": text} for match in matches]

def render_timeline(timeline_data):
    df = pd.DataFrame(timeline_data)
    if df.empty:
        st.warning("⚠️ No valid dates found.")
        return

    df["Parsed Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna()

    fig = px.timeline(df, x_start="Parsed Date", x_end="Parsed Date", y="Context", hover_data=["Text"],
                      title="📅 Timeline of Events")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)

# =================== Load Knowledge Base and Embeddings ===================

# Load tokenizer first for chunking
model_path = "./finetuned_model/"
tokenizer = T5Tokenizer.from_pretrained(model_path)

def chunk_text_by_tokens(text, tokenizer, max_tokens=200):
    """Chunk text into pieces of up to `max_tokens` using tokenizer."""
    tokens = tokenizer.encode(text, truncation=False)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
    return chunks

def load_knowledge_base(folder_path, max_tokens=200):
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                full_text = f.read()
                chunks = chunk_text_by_tokens(full_text, tokenizer, max_tokens)
                docs.extend(chunks)
    return docs

docs = load_knowledge_base("./wiki_sections/", max_tokens=200)
model_embed = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model_embed.encode(docs, convert_to_numpy=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Load Fine-tuned T5
model = T5ForConditionalGeneration.from_pretrained(model_path)

def retrieve_context(query, k=3):
    query_embedding = model_embed.encode([query])
    D, I = index.search(query_embedding, k)
    return [docs[i] for i in I[0]]

def generate_answer(query):
    context_passages = retrieve_context(query)
    context = " ".join(context_passages)
    input_text = f"question: {query} context: {context}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=512)

    outputs = model.generate(input_ids, max_length=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True), context_passages

# =================== Streamlit App ===================

st.title("🧠 RAG-based Historical QA with Timeline")

# Initialize session state timeline
if "timeline_data" not in st.session_state:
    st.session_state.timeline_data = []

query = st.text_input("Ask a question based on the knowledge base:", key="q")

retrieved_contexts = []

if query:
    with st.spinner("Generating answer..."):
        answer, retrieved_contexts = generate_answer(query)
        st.success(f"Answer: {answer}")

        # Extract and store dates from question and answer
        question_dates = extract_dates_from_text(query, "Question")
        answer_dates = extract_dates_from_text(answer, "Answer")
        st.session_state.timeline_data.extend(question_dates + answer_dates)

if st.button("🔍 Show Retrieved Contexts"):
    st.markdown("### Retrieved Contexts")
    for i, context in enumerate(retrieved_contexts, 1):
        with st.expander(f"Context {i}"):
            st.write(context)

if st.button("📅 Show Timeline"):
    st.markdown("### Timeline of Mentioned Dates")
    render_timeline(st.session_state.timeline_data)

if st.button("🗑️ Clear Timeline"):
    st.session_state.timeline_data = []
    st.success("Timeline has been cleared.")
