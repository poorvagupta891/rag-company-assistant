#!/usr/bin/env python3
# ============ IMPORTS ============
import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama  # ✅ CORRECT IMPORT
from langchain.chains import RetrievalQA

# ============ CONFIGURATION ============
PERSIST_DIRECTORY = '/Users/poorvagupta/chroma_db/'
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
DOCUMENT_PATH = "/Users/poorvagupta/Downloads/Company_Documents for RAG/"

# ============ STEP 1: LOAD DOCUMENTS ============
def load_and_process_documents():
    """Load text documents from the directory."""
    print(f"📂 Loading documents from: {DOCUMENT_PATH}")
    
    # Check if path exists
    if not os.path.exists(DOCUMENT_PATH):
        print(f"❌ Path does not exist: {DOCUMENT_PATH}")
        return []
    
    # List files to debug
    files = os.listdir(DOCUMENT_PATH)
    print(f"📋 Files in directory: {files}")
    
    loader = DirectoryLoader(
        DOCUMENT_PATH,
        glob="**/*.txt",  # ✅ Changed from *.pdf to *.txt
        loader_cls=TextLoader
    )
    
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} documents")
    return docs

# ============ STEP 2: SPLIT DOCUMENTS ============
def split_documents(docs):
    """Split loaded documents into smaller overlapping chunks."""
    if not docs:
        print("❌ No documents to split!")
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True
    )
    
    splits = text_splitter.split_documents(docs)
    print(f"✅ Created {len(splits)} chunks from {len(docs)} documents")
    
    return splits

# ============ STEP 3: INITIALIZE EMBEDDINGS MODEL ============
print("🔄 Initializing embedding model...")
embeddings_model = OllamaEmbeddings(
    model="nomic-embed-text"
)
print("✅ Embedding model initialized")

# ============ STEP 4: CREATE VECTOR DATABASE ============
def vector_database(splits, embeddings_model):
    """Create a Chroma vector database from document chunks."""
    if not splits:
        print("❌ No splits to vectorize!")
        return None
    
    print("🔄 Creating vector database...")
    
    # Clean up old database if it exists
    if os.path.exists(PERSIST_DIRECTORY):
        shutil.rmtree(PERSIST_DIRECTORY)
    
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embeddings_model,
        persist_directory=PERSIST_DIRECTORY,
        collection_name="company_documents"
    )
    
    print("✅ Vector store created and saved successfully")
    return vectordb

# ============ STEP 5: CREATE RETRIEVER (MMR) ============
def create_mmr_retriever(vectordb, k=3, fetch_k=20, lambda_mult=0.7):
    """Create a retriever using Maximum Marginal Relevance (MMR)."""
    if not vectordb:
        print("❌ No vector database!")
        return None
    
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": fetch_k,
            "lambda_mult": lambda_mult
        }
    )
    return retriever

# ============ STEP 6: CREATE QA CHAIN ============
def create_qa_chain(retriever):
    """Create a RetrievalQA chain that combines a retriever with an LLM."""
    if not retriever:
        print("❌ No retriever!")
        return None
    
    print("🔄 Creating QA chain...")
    
    # ✅ CORRECT IMPORT FOR OLLAMA
    llm = Ollama(model="llama3", temperature=0)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    
    print("✅ QA chain created")
    return qa_chain

# ============ EXECUTION ============
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 RAG Pipeline Starting...")
    print("="*50 + "\n")
    
    # Step 1: Load documents
    docs = load_and_process_documents()
    
    if not docs:
        print("⚠️ No documents loaded. Exiting.")
        exit(1)
    
    # Step 2: Split into chunks
    splits = split_documents(docs)
    
    if not splits:
        print("⚠️ No splits created. Exiting.")
        exit(1)
    
    # Step 4: Create vector database
    vectordb = vector_database(splits, embeddings_model)
    
    if not vectordb:
        print("⚠️ Vector database creation failed. Exiting.")
        exit(1)
    
    # Step 5: Create retriever
    retriever = create_mmr_retriever(vectordb)
    
    if not retriever:
        print("⚠️ Retriever creation failed. Exiting.")
        exit(1)
    
    # Step 6: Create QA chain
    qa_chain = create_qa_chain(retriever)
    
    if not qa_chain:
        print("⚠️ QA chain creation failed. Exiting.")
        exit(1)
    
    # Step 7: Ask questions
    print("\n" + "="*50)
    print("❓ Testing RAG System")
    print("="*50 + "\n")
    
    question = "Who do I contact for help?"
    print(f"Question: {question}")
    print("\nSearching for answer...")
    
    result = qa_chain.invoke({"query": question})
    
    print(f"\n✅ Answer:\n{result['result']}")
    
    print("\n" + "="*50)
    print("✅ RAG Pipeline Completed Successfully!")
    print("="*50)

