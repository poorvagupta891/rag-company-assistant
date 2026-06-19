#!/usr/bin/env python3
"""
Web UI for RAG Company Assistant
Uses functions from rag_utils.py
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

# Import RAG functions from rag_utils
from rag_utils import (
    load_and_process_documents,
    split_documents,
    vector_database,
    create_mmr_retriever,
    create_qa_chain,
    embeddings_model,
    PERSIST_DIRECTORY,
    DOCUMENT_PATH
)

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Company RAG Assistant",
    page_icon="🤖",
    layout="centered",  # Better for mobile
    initial_sidebar_state="collapsed"  # Collapsed by default on mobile
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

# ============ INITIALIZE RAG PIPELINE ============
def initialize_rag():
    """Initialize the RAG pipeline from rag_utils"""
    if st.session_state.initialized:
        return True
    
    with st.spinner("🚀 Initializing RAG pipeline from your documents..."):
        try:
            # Load documents
            docs = load_and_process_documents()
            if not docs:
                st.error("❌ No documents found at: " + DOCUMENT_PATH)
                return False
            
            # Split documents
            splits = split_documents(docs)
            if not splits:
                st.error("❌ Failed to split documents")
                return False
            
            # Create vector database
            vectordb = vector_database(splits, embeddings_model)
            if not vectordb:
                st.error("❌ Failed to create vector database")
                return False
            
            # Create retriever
            retriever = create_mmr_retriever(vectordb)
            if not retriever:
                st.error("❌ Failed to create retriever")
                return False
            
            # Create QA chain
            qa_chain = create_qa_chain(retriever)
            if not qa_chain:
                st.error("❌ Failed to create QA chain")
                return False
            
            st.session_state.qa_chain = qa_chain
            st.session_state.initialized = True
            
            st.success(f"✅ RAG Pipeline Ready! Loaded {len(docs)} documents with {len(splits)} chunks")
            return True
            
        except Exception as e:
            st.error(f"❌ Error initializing RAG: {e}")
            return False

# ============ MAIN UI ============
st.title("🤖 Company RAG Assistant")
st.caption("Ask questions about your company documents. Powered by your rag_utils.py")

# Initialize
if not st.session_state.initialized:
    if not initialize_rag():
        st.stop()

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
# Chat input (mobile-optimized)
        question = st.text_input("Ask your question...", key="question_input", placeholder="What would you like to know?")
        submit_btn = st.button("🚀 Send", type="primary", use_container_width=True)

# Process question
if submit_btn and question:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "sources": []
    })
    
    # Get answer
    /* General */
    .main {
        padding: 1rem;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        .stButton button {
            width: 100%;
        }
    }
    
    /* Chat messages */
    .chat-message {
        padding: 0.75rem;
        border-radius: 10px;
        margin-bottom: 0.75rem;
        word-wrap: break-word;
        max-width: 100%;
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.75rem;
        margin: 0.25rem 0.25rem 0.25rem 0;
        word-break: break-word;
            st.error(f"❌ Error getting answer: {e}")
    
    /* Input optimization */
    .stTextInput input {
        font-size: 16px; /* Prevents zoom on iOS */
    }
    
    /* Header */
    h1, h2, h3 {
        word-break: break-word;
    }

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
    ### Your Documents
    
    **Location:**
    `{}`
    
    **Status:** ✅ Ready
    """.format(DOCUMENT_PATH))
    
    st.markdown("---")
    
    if st.button("🔄 Reinitialize", key="reinit_btn"):
        st.session_state.initialized = False
        st.session_state.qa_chain = None
        st.rerun()
    
    if st.button("🗑️ Clear Chat", key="clear_btn"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption("Powered by: LangChain + Ollama + Chroma + Streamlit")
