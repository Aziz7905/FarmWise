import os
import pickle
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers import BM25Retriever

# Load environment variables (.env for HuggingFace token)
load_dotenv()

# Supported document files (put them in a folder called "docs")
DOCUMENTS = [
    "docs/crop rotation qa.txt",  # ✅ correct
    "docs/crop-rotation.pdf",
    "docs/researchgatepaper.docx"
]

def process_and_store(files, faiss_path="vectorstore", bm25_path="bm25.pkl"):
    all_docs = []

    for path in files:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        elif ext == ".txt":
            loader = TextLoader(path)
        elif ext in [".docx", ".doc"]:
            loader = UnstructuredWordDocumentLoader(path)
        else:
            print(f"Unsupported file type: {path}")
            continue

        try:
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = os.path.basename(path)
            all_docs.extend(docs)
        except Exception as e:
            print(f"Error loading {path}: {e}")

    # Chunking
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(all_docs)

    # Deduplication
    unique = {}
    for doc in chunks:
        text = doc.page_content.strip()
        if text not in unique:
            unique[text] = doc
    unique_chunks = list(unique.values())
    print(f"📦 {len(unique_chunks)} unique chunks extracted")

    # Create FAISS
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    faiss_store = FAISS.from_documents(unique_chunks, embeddings)
    faiss_store.save_local(faiss_path)
    print(f"✅ FAISS index saved to '{faiss_path}/'")

    # Create BM25
    bm25 = BM25Retriever.from_documents(unique_chunks)
    bm25.k = 8
    with open(bm25_path, "wb") as f:
        pickle.dump(bm25, f)
    print(f"✅ BM25 retriever saved to '{bm25_path}'")

if __name__ == "__main__":
    process_and_store(DOCUMENTS)
