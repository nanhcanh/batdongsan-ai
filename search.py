import openai
from pinecone import Pinecone
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("real-estate")

def search(query):
    embedding = openai.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    results = index.query(
        vector=embedding,
        top_k=5,
        include_metadata=True
    )

    return results['matches']
