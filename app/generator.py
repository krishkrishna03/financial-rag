from transformers import pipeline

# Load a local model for text generation
generator = pipeline("text-generation", model="gpt2")

def generate_insight(context, query):
    prompt = f"""You are a financial analyst. Based on the following context, answer the query:
Context:
{context}

Query:
{query}

Answer:"""
    result = generator(prompt, max_length=200, do_sample=True)[0]['generated_text']
    return result.split("Answer:")[-1].strip()