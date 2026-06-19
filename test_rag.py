#!/usr/bin/env python3
"""
Test script to directly test the RAG pipeline with company documents
"""

import os
import sys
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# Configuration
UPLOAD_FOLDER = "/Users/poorvagupta/Documents/RAG-Company-Assistant/uploaded_documents"
PERSIST_DIRECTORY = "/Users/poorvagupta/Documents/RAG-Company-Assistant/chroma_db_test"
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150

def check_ollama():
    """Check if Ollama is running"""
    import urllib.request
    try:
        urllib.request.urlopen('http://localhost:11434')
        print("✅ Ollama is running")
        return True
    except:
        print("❌ Ollama is not running!")
        print("   Please start Ollama: ollama serve")
        return False

def load_documents():
    """Load documents from upload folder"""
    print("\n📂 Loading documents from: " + UPLOAD_FOLDER)
    
    if not os.path.exists(UPLOAD_FOLDER):
        print("❌ Upload folder not found!")
        return []
    
    loader = DirectoryLoader(
        UPLOAD_FOLDER,
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} documents")
    
    # Show document info
    for doc in docs:
        size = len(doc.page_content)
        print(f"   - {os.path.basename(doc.metadata['source'])} ({size} characters)")
    
    return docs

def split_documents(docs):
    """Split documents into chunks"""
    print(f"\n✂️  Splitting documents into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True
    )
    
    splits = splitter.split_documents(docs)
    print(f"✅ Created {len(splits)} chunks")
    return splits

def create_vector_db(splits):
    """Create vector database"""
    print("\n🗄️  Creating vector database...")
    
    # Clean up old db
    if os.path.exists(PERSIST_DIRECTORY):
        import shutil
        shutil.rmtree(PERSIST_DIRECTORY)
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name="test_documents"
    )
    
    print("✅ Vector database created")
    return vectordb, embeddings

def create_qa_chain(vectordb, embeddings):
    """Create QA chain"""
    print("\n🔗 Creating QA chain...")
    
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 20, "lambda_mult": 0.7}
    )
    
    llm = Ollama(model="llama3", temperature=0)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    print("✅ QA chain ready")
    return qa_chain

def ask_question(qa_chain, question):
    """Ask a question and get answer"""
    print(f"\n❓ Question: {question}")
    print("-" * 60)
    
    result = qa_chain({"query": question})
    
    answer = result["result"]
    sources = result.get("source_documents", [])
    
    print(f"\n💡 Answer:\n{answer}")
    
    if sources:
        print("\n📚 Sources:")
        for i, doc in enumerate(sources, 1):
            source_name = os.path.basename(doc.metadata.get("source", "Unknown"))
            print(f"   {i}. {source_name}")
    
    print("-" * 60)
    return answer

def main():
    print("\n" + "="*60)
    print("🧪 RAG PIPELINE TEST")
    print("="*60)
    
    # Check Ollama
    if not check_ollama():
        sys.exit(1)
    
    # Load documents
    docs = load_documents()
    if not docs:
        print("❌ No documents loaded")
        sys.exit(1)
    
    # Split documents
    splits = split_documents(docs)
    if not splits:
        print("❌ No splits created")
        sys.exit(1)
    
    # Create vector DB
    vectordb, embeddings = create_vector_db(splits)
    
    # Create QA chain
    qa_chain = create_qa_chain(vectordb, embeddings)
    
    # Test questions
    print("\n" + "="*60)
    print("🧪 TESTING WITH SAMPLE QUESTIONS")
    print("="*60)
    
    test_questions = [
        "What is the deployment process?",
        "What are the employee benefits?",
        "How do I troubleshoot common issues?",
        "What is FintechAI Pro?",
        "What are the security policies?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        ask_question(qa_chain, question)
        
        # Ask for more
        if i < len(test_questions):
            cont = input("\n▶️  Press Enter for next question (or type 'q' to quit): ").strip().lower()
            if cont == 'q':
                break
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETE")
    print("="*60)
    print("""
Now you can:
1. Use the Streamlit web UI to ask more questions
2. Run this script again to test with different questions
3. Add more documents to the uploaded_documents folder

To start the web UI:
   python3 -m streamlit run streamlit_app.py
""")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
