#!/usr/bin/env python3
"""
Cloud-ready version of RAG Company Assistant
Works with local or remote Ollama servers
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Company RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS ============
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #F3E5F5;
        border-left: 4px solid #9C27B0;
    }
    .source-badge {
        display: inline-block;
        background-color: #FFC107;
        color: #000;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
if "messages" not in st.session_state:
    st.session_state.messages = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "error" not in st.session_state:
    st.session_state.error = None

# ============ CONFIGURATION ============
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DOCUMENT_PATH = os.getenv("DOCUMENT_PATH", "/Users/poorvagupta/Downloads/Company_Documents for RAG/")

# ============ INITIALIZE RAG PIPELINE ============
@st.cache_resource
def initialize_rag():
    """Initialize the RAG pipeline from rag_utils"""
    try:
        # Import here to avoid issues if Ollama isn't available
        from rag_utils import (
            load_and_process_documents,
            split_documents,
            vector_database,
            create_mmr_retriever,
            create_qa_chain,
            embeddings_model,
        )
        
        # Load documents
        docs = load_and_process_documents()
        if not docs:
            return None, f"No documents found at: {DOCUMENT_PATH}"
        
        # Split documents
        splits = split_documents(docs)
        if not splits:
            return None, "Failed to split documents"
        
        # Create vector database
        vectordb = vector_database(splits, embeddings_model)
        if not vectordb:
            return None, "Failed to create vector database"
        
        # Create retriever
        retriever = create_mmr_retriever(vectordb)
        if not retriever:
            return None, "Failed to create retriever"
        
        # Create QA chain
        qa_chain = create_qa_chain(retriever)
        if not qa_chain:
            return None, "Failed to create QA chain"
        
        return qa_chain, None
        
    except Exception as e:
        return None, str(e)

# ============ MAIN UI ============
st.title("🤖 Company RAG Assistant")
st.caption("Ask questions about your company documents. Powered by your rag_utils.py")

# Initialize on first load
if not st.session_state.initialized:
    with st.spinner("🚀 Initializing RAG pipeline from your documents..."):
        qa_chain, error = initialize_rag()
        
        if error:
            st.session_state.error = error
            st.session_state.qa_chain = None
        else:
            st.session_state.qa_chain = qa_chain
            st.session_state.error = None
        
        st.session_state.initialized = True

# Show error if any
if st.session_state.error:
    st.error(f"❌ Error initializing RAG: {st.session_state.error}")
    
    with st.expander("ℹ️ Troubleshooting"):
        st.markdown("""
        **Make sure:**
        1. Ollama is running: `ollama serve`
        2. Documents exist at: `{}`
        3. Models are available:
           - `ollama pull nomic-embed-text`
           - `ollama pull llama3`
        """.format(DOCUMENT_PATH))
    
    st.stop()

# Success - show chat
st.success("✅ RAG Pipeline Ready! Loaded and indexed your documents.")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <b>You:</b> {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <b>Assistant:</b> {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
        
        if msg.get("sources"):
            st.markdown("**📚 Sources:**")
            for source in msg["sources"]:
                source_name = os.path.basename(source)
                st.markdown(f'<span class="source-badge">{source_name}</span>', unsafe_allow_html=True)

# Chat input
col1, col2 = st.columns([6, 1])
with col1:
    question = st.text_input("Ask your question...", key="question_input", placeholder="What would you like to know?")
with col2:
    submit_btn = st.button("Send", type="primary")

# Process question
if submit_btn and question and st.session_state.qa_chain:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "sources": []
    })
    
    # Get answer
    with st.spinner("🔍 Searching your documents..."):
        try:
            result = st.session_state.qa_chain({"query": question})
            answer = result["result"]
            sources = [doc.metadata.get("source", "Unknown") for doc in result.get("source_documents", [])]
            
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
            
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error getting answer: {e}")

# ============ SIDEBAR ============
with st.sidebar:
    st.title("ℹ️ About")
    
    st.markdown("""
    ### How It Works
    
    This AI assistant answers questions about your company documents using:
    
    **🔍 RAG (Retrieval Augmented Generation)**
    - Searches documents first
    - Uses vector embeddings for fast search
    
    **🗄️ Vector Database**
    - Powered by Chroma
    - Fast similarity search
    
    **🤖 Ollama LLM**
    - Local AI model (Llama 3)
    - Generates answers from documents
    
    **💫 Smart Retrieval**
    - MMR algorithm
    - Diverse and relevant results
    """)
    
    st.markdown("---")
    st.markdown("""
    ### Configuration
    
    **Ollama URL:**
    `{}`
    
    **Document Path:**
    `{}`
    
    **Status:** ✅ Ready
    """.format(OLLAMA_URL, DOCUMENT_PATH))
    
    st.markdown("---")
    
    if st.button("🔄 Reinitialize", key="reinit_btn"):
        # Clear cache
        st.cache_resource.clear()
        st.session_state.initialized = False
        st.session_state.qa_chain = None
        st.rerun()
    
    if st.button("🗑️ Clear Chat", key="clear_btn"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption("Powered by: LangChain + Ollama + Chroma + Streamlit")
    
    with st.expander("📚 Sample Questions"):
        st.markdown("""
        Try asking:
        - What is the deployment process?
        - What are the employee benefits?
        - How do I troubleshoot issues?
        - What is FintechAI Pro?
        - What are the security policies?
        """)
