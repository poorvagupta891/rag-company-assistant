# 🚀 Quick Start Guide - Enhanced Web UI

## What's New

Your RAG assistant now has a professional web interface with:

✅ **Chat Interface** - Ask questions about your documents  
✅ **Admin Panel** - Upload and manage documents  
✅ **Real-time Status** - See system health and database stats  
✅ **Source Attribution** - View which documents informed each answer  

## Prerequisites

Before running the app, make sure you have:

1. **Python 3.9+** installed
2. **Ollama** installed and running on `http://localhost:11434`
   - Download from: https://ollama.ai
   - Must have `nomic-embed-text` and `llama3` models

## Installation

```bash
# 1. Navigate to project directory
cd /Users/poorvagupta/Documents/RAG-Company-Assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run streamlit_app.py
```

Or simply run the startup script:
```bash
chmod +x run.sh
./run.sh
```

## How to Use

### Step 1: Start the App
```bash
streamlit run streamlit_app.py
```
The app will open at `http://localhost:8501`

### Step 2: Upload Documents (Admin Panel)
1. Click on the **⚙️ Admin Panel** tab
2. Click "Upload company documents"
3. Select your `.txt` or `.pdf` files
4. Click **"Process and Index Documents"**
5. Wait for processing to complete ✅

### Step 3: Ask Questions (Chat Tab)
1. Click on the **💬 Chat** tab
2. Type your question in the input box
3. Press Enter or click send
4. The AI searches your documents and provides an answer
5. Click "📚 Sources" to see which documents were used

## File Structure

```
RAG-Company-Assistant/
├── streamlit_app.py          # Main web UI application
├── rag_utils.py              # RAG pipeline utilities
├── requirements.txt          # Python dependencies
├── run.sh                    # Startup script
├── chroma_db/                # Vector database (auto-created)
├── uploaded_documents/       # Your uploaded documents (auto-created)
└── README.md
```

## Features Explained

### 💬 Chat Tab
- Clean chat interface with history
- Real-time question answering
- Source attribution with expandable details
- Status indicators for system health

### ⚙️ Admin Panel

**Upload Documents Section:**
- Drag & drop file upload
- Support for `.txt` and `.pdf` files
- Progress indicators

**System Status:**
- ✅/❌ Embeddings Model status
- ✅/❌ QA Chain status
- Database statistics

**Database Management:**
- View indexed chunks count
- Clear entire database
- Clear uploaded documents

## Troubleshooting

### "❌ Embeddings Model Error"
- Ensure Ollama is running
- Check that `nomic-embed-text` model is available
- Run: `ollama pull nomic-embed-text`

### "⚠️ No QA Chain (upload documents)"
- Go to Admin Panel
- Upload and process documents first
- Wait for processing to complete

### Port Already in Use
```bash
# Use a different port
streamlit run streamlit_app.py --server.port 8502
```

### Slow Response
- Check your document sizes
- Increase `CHUNK_SIZE` in code if documents are large
- Ensure Ollama has enough system resources

## Tips for Best Results

1. **Document Format**: Convert PDFs to text for better results
2. **Document Length**: Longer, more detailed documents work better
3. **Question Clarity**: Ask specific questions for better answers
4. **Document Organization**: Use clear headers and sections
5. **Metadata**: Add timestamps and document titles for better attribution

## API Integration (Optional)

If you want to use this with other applications, you can modify the code to:
- Add a FastAPI backend
- Create a REST API
- Add authentication
- Enable batch processing

For now, this Streamlit UI provides everything you need!

---

**Need help?** Check the Streamlit docs: https://docs.streamlit.io
