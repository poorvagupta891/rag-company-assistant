# 📚 Your RAG System - Usage Guide

## ✅ What's Ready

Your RAG pipeline is **fully built and working**! You have 5 documents indexed with 47 chunks in the vector database.

## 🎯 Two Ways to Use Your System

### Option 1: Interactive Command-Line (Your rag_utils.py)

Ask questions directly in the terminal:

```bash
cd /Users/poorvagupta/Documents/RAG-Company-Assistant
python3 rag_utils.py
```

This will:
1. Load your 5 documents (already cached)
2. Create the vector database
3. Ask you a test question
4. Let you type your own questions interactively
5. Press `Ctrl+C` or type `exit` to quit

**Example questions to ask:**
- What is the deployment process?
- What are the employee benefits?
- How do I troubleshoot issues?
- What is FintechAI Pro?
- What are the security policies?
- Who do I contact for help?

---

### Option 2: Web UI (Streamlit App)

Use a beautiful web interface in your browser:

```bash
cd /Users/poorvagupta/Documents/RAG-Company-Assistant
python3 -m streamlit run streamlit_app.py
```

Then open: **http://localhost:8501**

**Features:**
- 💬 Chat tab: Ask questions with a modern chat interface
- ⚙️ Admin Panel: Manage documents and database
- 📊 Real-time statistics
- 📚 View source documents for each answer

---

## 📁 Project Structure

```
RAG-Company-Assistant/
├── rag_utils.py              ← Your main RAG pipeline (run this!)
├── streamlit_app.py          ← Web UI (optional)
├── setup_documents.py        ← Copy documents to upload folder
├── test_rag.py              ← Test script with Q&A
├── chroma_db/               ← Your built vector database ✅
├── uploaded_documents/      ← Documents in upload folder
├── requirements.txt         ← Dependencies
└── README.md
```

---

## 🗄️ Your Vector Database

Location: `/Users/poorvagupta/chroma_db/`

Contains:
- 5 company documents
- 47 text chunks
- Embeddings from nomic-embed-text
- Ready for instant querying!

---

## 🚀 Quick Start Commands

**Interactive Q&A (fastest):**
```bash
python3 rag_utils.py
```

**Web UI (for multiple users/collaborative):**
```bash
python3 -m streamlit run streamlit_app.py
```

**Test multiple questions:**
```bash
python3 test_rag.py
```

---

## 💡 Tips

1. **Fast Response**: Your vector database is already built, so responses are instant
2. **Modify Questions**: Edit `rag_utils.py` to change the default test question
3. **Add Documents**: Copy new documents to `/Users/poorvagupta/Downloads/Company_Documents for RAG/` and re-run
4. **Check Status**: Your database location is: `/Users/poorvagupta/chroma_db/`

---

## 🔧 Configuration

If you want to change settings, edit `rag_utils.py`:

```python
PERSIST_DIRECTORY = '/Users/poorvagupta/chroma_db/'    # Database location
CHUNK_SIZE = 1500                                       # Text chunk size
CHUNK_OVERLAP = 150                                    # Chunk overlap
DOCUMENT_PATH = "/Users/poorvagupta/Downloads/..."    # Document location
```

---

**Your system is ready to use! Choose your preferred method above and start asking questions!** 🚀
