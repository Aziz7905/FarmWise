import os
import pickle
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever  # ✅ This line fixed
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

def load_ensemble_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # ✅ Add `allow_dangerous_deserialization=True` because FAISS uses pickle
    vectorstore = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

    with open("bm25.pkl", "rb") as f:
        bm25 = pickle.load(f)
        bm25.k = 8

    return EnsembleRetriever(retrievers=[bm25, vector_retriever], weights=[0.5, 0.5])
