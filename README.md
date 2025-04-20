
# 🧠 RAG-based Historical Question Answering with Timeline Visualization

This is a **Retrieval-Augmented Generation (RAG)** based Question Answering system focused on historical content. Users can ask questions from a custom knowledge base and visualize all historical dates mentioned in the queries and answers on a timeline.

Built using:
- Sentence Transformers (`all-MiniLM-L6-v2`)
- HuggingFace Transformers (`T5`)
- FAISS for similarity search
- Streamlit for frontend
- Plotly for timeline visualization

---

## 📦 Features

- 📚 Chunked knowledge base stored in a FAISS index for semantic retrieval.
- 🧠 Fine-tuned T5 model generates contextual answers based on retrieved chunks.
- 📅 Timeline view of historical events extracted from questions and answers.
- 🔍 Inspect retrieved context passages used by the model.

---

# Steps to Run
Clone this project
Download FineTuned T5 model ----> https://drive.google.com/file/d/1R7s4tkkQoixKiFn90KrVHXsTTyKiqCPT/view?usp=sharing (Github doesn't support >25MB). Download, Extract it and keep in the project folder

To download all the dependencies
`pip install -r requirements.txt`

 To run the project 
 `streamlit run rag_app.py`
