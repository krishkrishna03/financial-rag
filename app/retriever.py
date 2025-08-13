import chromadb
from chromadb.utils import embedding_functions

# Force DuckDB + Parquet backend (avoids SQLite)
client = chromadb.Client(
    persist_directory=".chromadb",
    settings=chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=".chromadb"
    )
)

collection = client.get_or_create_collection(name="financial_data")

def add_documents(docs, metadatas):
    collection.add(
        documents=docs,
        metadatas=metadatas,
        ids=[str(i) for i in range(len(docs))]
    )

def query(text, top_k=5):
    return collection.query(query_texts=[text], n_results=top_k)
