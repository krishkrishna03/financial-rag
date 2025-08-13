import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
collection = client.get_or_create_collection(name="financial_data")

def add_documents(docs, metadatas):
    collection.add(documents=docs, metadatas=metadatas, ids=[str(i) for i in range(len(docs))])

def query(text, top_k=5):
    return collection.query(query_texts=[text], n_results=top_k)