import os
import gradio as gr
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize vectorstore (empty initially)
vectordb = None

# Initialize embeddings and LLM
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature": 0})

def upload_docs(files):
    global vectordb
    docs = []
    for f in files:
        content = f.read().decode("utf-8", errors="ignore")
        docs.append({"text": content, "metadata": {"source": f.name}})
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    
    vectordb = Chroma.from_documents(chunks, embeddings)
    return f"{len(chunks)} chunks uploaded and indexed."

def ask_query(query):
    if vectordb is None:
        return "Please upload documents first."
    
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())
    answer = qa.run(query)
    return answer

with gr.Blocks() as demo:
    gr.Markdown("## 📊 Financial Analysis RAG System (Gradio)")

    with gr.Tab("Upload Documents"):
        file_input = gr.File(file_types=[".txt"], file_types_label="Upload Financial Reports", file_multiple=True)
        upload_btn = gr.Button("Upload & Index")
        output_text = gr.Textbox(label="Status")
        upload_btn.click(upload_docs, inputs=file_input, outputs=output_text)

    with gr.Tab("Ask Query"):
        query_input = gr.Textbox(label="Enter your financial query")
        query_btn = gr.Button("Get Answer")
        answer_output = gr.Textbox(label="Answer")
        query_btn.click(ask_query, inputs=query_input, outputs=answer_output)

# Render requires these settings
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))

