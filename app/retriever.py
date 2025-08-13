import chromadb
from chromadb.utils import embedding_functions

# Use DuckDB + Parquet backend to avoid SQLite issues
client = chromadb.Client(
    persist_directory=".chromadb",
    settings=chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=".chromadb"
    )
)

# Create or get a collection
collection = client.get_or_create_collection(name="financial_data")

# Function to add documents
def add_documents(docs, metadatas):
    collection.add(
        documents=docs,
        metadatas=metadatas,
        ids=[str(i) for i in range(len(docs))]
    )

# Function to query documents
def query(text, top_k=5):
    return collection.query(query_texts=[text], n_results=top_k)
