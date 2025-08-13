import streamlit as st
from retriever import query, add_documents
from generator import generate_insight
from time_series import analyze_trends
from embedder import embed_text

# Load sample documents
docs = ["Company A reported strong earnings growth...", "Market volatility increased due to global tensions..."]
metadatas = [{"source": "report"}, {"source": "news"}]
add_documents(docs, metadatas)

st.title("📊 Financial RAG System")

query_text = st.text_input("Enter your financial query")

if st.button("Analyze"):
    results = query(query_text)
    context = "\n".join(results['documents'][0])
    answer = generate_insight(context, query_text)
    st.subheader("Generated Insight")
    st.write(answer)

    st.subheader("Trend Analysis")
    analyze_trends("data/market_data.csv")
    st.image("app/trend_plot.svg")