import streamlit as st
import os
import shutil
import tempfile
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

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
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .metric-card {
        border-radius: 10px;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============ CONFIGURATION ============
PERSIST_DIRECTORY = os.path.join(os.getcwd(), 'chroma_db')
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploaded_documents')

# Create necessary directories
os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============ SESSION STATE INITIALIZATION ============
if "messages" not in st.session_state:
    st.session_state.messages = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "vectordb" not in st.session_state:
    st.session_state.vectordb = None
if "embeddings_model" not in st.session_state:
    st.session_state.embeddings_model = None
if "doc_count" not in st.session_state:
    st.session_state.doc_count = 0

# ============ RAG FUNCTIONS ============
@st.cache_resource
def load_embeddings_model():
    """Load embeddings model (cached for performance)."""
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        return embeddings
    except Exception as e:
        st.error(f"❌ Failed to load embeddings: {e}")
        return None

def load_and_process_documents(doc_path):
    """Load documents from directory."""
    if not os.path.exists(doc_path):
        return []
    
    try:
        loader = DirectoryLoader(
            doc_path,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        docs = loader.load()
        return docs
    except Exception as e:
        st.error(f"Error loading documents: {e}")
        return []

def split_documents(docs):
    """Split documents into chunks."""
    if not docs:
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True
    )
    splits = text_splitter.split_documents(docs)
    return splits

def create_vector_database(splits, embeddings_model):
    """Create or update vector database."""
    if not splits or embeddings_model is None:
        return None
    
    try:
        vectordb = Chroma.from_documents(
            documents=splits,
            embedding=embeddings_model,
            persist_directory=PERSIST_DIRECTORY,
            collection_name="company_documents"
        )
        return vectordb
    except Exception as e:
        st.error(f"Error creating vector database: {e}")
        return None

def create_qa_chain(embeddings_model):
    """Create QA chain from existing vector database."""
    try:
        vectordb = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embeddings_model,
            collection_name="company_documents"
        )
        
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
        return qa_chain
    except Exception as e:
        st.error(f"Error creating QA chain: {e}")
        return None

# ============ UTILITY FUNCTIONS ============
def get_db_stats():
    """Get statistics about the vector database."""
    try:
        if st.session_state.embeddings_model:
            vectordb = Chroma(
                persist_directory=PERSIST_DIRECTORY,
                embedding_function=st.session_state.embeddings_model,
                collection_name="company_documents"
            )
            count = vectordb._collection.count()
            return count
    except:
        return 0

def process_uploaded_files(uploaded_files):
    """Process uploaded files and add to database."""
    if not uploaded_files:
        return 0
    
    for uploaded_file in uploaded_files:
        try:
            # Save uploaded file
            temp_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Convert to txt if needed
            if uploaded_file.name.endswith('.txt'):
                pass  # Already txt
            
            st.success(f"✅ Uploaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {e}")
    
    return len(uploaded_files)

# ============ MAIN APP ============
st.title("🤖 Company RAG Assistant")
st.caption("Ask questions about your company documents with AI-powered search and retrieval")

# Initialize embeddings model
if st.session_state.embeddings_model is None:
    with st.spinner("Loading embeddings model..."):
        st.session_state.embeddings_model = load_embeddings_model()

# Tabs for different sections
tab1, tab2 = st.tabs(["💬 Chat", "⚙️ Admin Panel"])

# ============ TAB 1: CHAT INTERFACE ============
with tab1:
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.metric("📊 Documents Indexed", get_db_stats())
    
    # Display chat history
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg.get("sources"):
                    with st.expander("📚 Sources"):
                        for source in msg["sources"]:
                            st.text(source)
    
    # Chat input
    question = st.chat_input("Ask your question here...", key="chat_input")
    
    if question:
        # Check if QA chain is available
        if st.session_state.qa_chain is None:
            st.warning("⚠️ No documents indexed yet. Please go to Admin Panel to upload documents.")
        else:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": question,
                "sources": []
            })
            
            with chat_container:
                with st.chat_message("user"):
                    st.write(question)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Searching documents..."):
                    try:
                        result = st.session_state.qa_chain({"query": question})
                        answer = result["result"]
                        sources = [doc.metadata.get("source", "Unknown") for doc in result.get("source_documents", [])]
                        
                        st.write(answer)
                        
                        if sources:
                            with st.expander("📚 Sources"):
                                for source in sources:
                                    st.text(source)
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        })
                    except Exception as e:
                        st.error(f"❌ Error generating response: {e}")

# ============ TAB 2: ADMIN PANEL ============
with tab2:
    st.header("📋 Admin Panel")
    
    admin_col1, admin_col2 = st.columns(2)
    
    with admin_col1:
        st.subheader("📤 Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload company documents (txt, pdf)",
            accept_multiple_files=True,
            type=["txt", "pdf"],
            key="file_uploader"
        )
        
        if uploaded_files:
            if st.button("Process and Index Documents", key="process_btn"):
                with st.spinner("Processing documents..."):
                    try:
                        # Save files
                        for file in uploaded_files:
                            temp_path = os.path.join(UPLOAD_FOLDER, file.name)
                            with open(temp_path, "wb") as f:
                                f.write(file.getbuffer())
                        
                        # Load and process
                        docs = load_and_process_documents(UPLOAD_FOLDER)
                        if docs:
                            splits = split_documents(docs)
                            vectordb = create_vector_database(splits, st.session_state.embeddings_model)
                            
                            if vectordb:
                                st.session_state.vectordb = vectordb
                                st.session_state.qa_chain = create_qa_chain(st.session_state.embeddings_model)
                                st.session_state.doc_count = len(docs)
                                st.success(f"✅ Successfully indexed {len(docs)} documents with {len(splits)} chunks!")
                                st.rerun()
                        else:
                            st.warning("No documents found in upload folder.")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    with admin_col2:
        st.subheader("🔧 System Status")
        
        col_status1, col_status2 = st.columns(2)
        with col_status1:
            if st.session_state.embeddings_model:
                st.success("✅ Embeddings Model Ready")
            else:
                st.error("❌ Embeddings Model Error")
        
        with col_status2:
            if st.session_state.qa_chain:
                st.success("✅ QA Chain Ready")
            else:
                st.warning("⚠️ No QA Chain (upload documents)")
        
        st.markdown("---")
        st.subheader("📊 Database Stats")
        db_size = get_db_stats()
        st.metric("Indexed Chunks", db_size)
        
        if st.button("Clear Database", key="clear_db"):
            if os.path.exists(PERSIST_DIRECTORY):
                shutil.rmtree(PERSIST_DIRECTORY)
                os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
                st.session_state.qa_chain = None
                st.session_state.vectordb = None
                st.session_state.doc_count = 0
                st.success("✅ Database cleared!")
                st.rerun()
    
    st.markdown("---")
    st.subheader("📁 Uploaded Documents")
    if os.path.exists(UPLOAD_FOLDER):
        files = os.listdir(UPLOAD_FOLDER)
        if files:
            for file in files:
                st.write(f"📄 {file}")
        else:
            st.info("No documents uploaded yet.")
    
    st.markdown("---")
    st.subheader("🗑️ Manage Documents")
    if st.button("Clear All Uploaded Documents", key="clear_uploads"):
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        st.success("✅ All uploaded documents cleared!")
        st.rerun()

# ============ SIDEBAR ============
with st.sidebar:
    st.title("ℹ️ About")
    st.markdown("""
    ### Company RAG Assistant
    
    This AI assistant answers questions about your company documents using:
    
    - **🔍 RAG (Retrieval Augmented Generation)**: Searches documents first
    - **📊 Vector Database**: Fast similarity search with Chroma
    - **🤖 Ollama LLM**: Local AI model (Llama 3)
    - **💫 Smart Retrieval**: MMR algorithm for diverse results
    
    ### How to Use
    1. Go to **Admin Panel**
    2. Upload your documents
    3. Click **Process and Index**
    4. Return to **Chat** tab
    5. Start asking questions!
    """)
    
    st.markdown("---")
    st.markdown("""
    **Version**: 1.0  
    **Powered by**: LangChain + Ollama + Chroma
    """)