README.md
# 🤖 RAG Company Document Assistant

A smart AI system that answers questions about company documents.

## What Does It Do?

Imagine you have 100 company documents. Instead of reading all of them:
1. **You ask a question**: "What are the legal policies?"
2. **AI finds relevant documents** (searches instantly)
3. **AI reads the documents** and answers based on them
4. **You get an answer** in 2-3 seconds

## Why Is This Useful?

- **For Companies**: Quick answers from documents without reading everything
- **For AI**: Uses real information (doesn't make up answers)
- **For Recruiters**: Shows you understand AI + organization + deployment

## How Does It Work?
### Step-by-Step:

1. **Documents Loaded**: Read all company documents
2. **Split into Chunks**: Break into 1500-character pieces
3. **Converted to Embeddings**: Convert text to numbers (vectors)
4. **Stored in Database**: Save in Chroma for fast searching
5. **User Asks Question**: Question becomes embedding too
6. **Search**: Find most similar documents using vectors
7. **LLM Reads**: Llama 3 reads relevant documents
8. **Answer Generated**: AI generates answer based on documents
9. **Response Sent**: Answer shown to user

## Technologies Used

- **Python** - Programming language
- **LangChain** - Connects all AI tools
- **Chroma** - Stores embeddings (vector database)
- **Ollama** - Runs AI models locally
- **Streamlit** - Creates the website
- **MMR** - Retrieval algorithm (finds diverse results)

## 💻 How to Run Locally

### Prerequisites (Must Install First)

1. **Install Ollama**
   - Go to https://ollama.ai
   - Download and install for your computer
   - Open Ollama and run these commands:
   2. **Install Python 3.9+**
   - Go to https://python.org
   - Download and install

### Run the App

```bash
# Open terminal/command prompt in project folder

# Create virtual environment (only first time)
python -m venv venv

# Activate virtual environment
# On Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py

# Open http://localhost:8501 in your browser
```

## 📁 Project Structure
## 🎯 Key Concepts Explained

### Embeddings
- **What**: Converting text to numbers (vectors)
- **Why**: AI understands numbers better than text
- **Example**: "Hello world" → [0.1, 0.5, 0.3, 0.2, ...]

### Vector Search
- **What**: Finding similar numbers quickly
- **Why**: Don't need to read every document
- **Speed**: Millions of documents searched in milliseconds

### RAG (Retrieval-Augmented Generation)
- **What**: Find documents + Generate answers
- **Why**: Answers are based on real information
- **Result**: No hallucinations (made-up answers)

### MMR (Maximum Marginal Relevance)
- **What**: Finding relevant AND diverse documents
- **Why**: Don't want 5 similar answers
- **Example**: Search "funny movies" → Get different genres

## 📊 How It's Different From ChatGPT

| Feature | ChatGPT | Our RAG |
|---------|---------|---------|
| **Source** | Training data (might be outdated) | Your documents (always current) |
| **Accuracy** | Can hallucinate | Based on real documents |
| **Privacy** | Data sent to OpenAI | Everything stays local |
| **Cost** | Paid API | Free (runs locally) |
| **Explainability** | No source shown | Can show source documents |

## 🚀 Deploy to Internet

Once code is on GitHub, you can deploy to Streamlit Cloud (free):

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub
4. Deploy in 1 click
5. Share link with recruiters

## 🎓 Learning Resources

- **LangChain**: https://python.langchain.com
- **Chroma**: https://docs.trychroma.com
- **Ollama**: https://github.com/ollama/ollama
- **Streamlit**: https://docs.streamlit.io
- **Embeddings**: https://www.pinecone.io/learn/vector-embeddings/

## 🤝 What Recruiters Will See

✅ Clean code organized into files
✅ Good documentation (this README)
✅ Working project they can test
✅ Understanding of AI concepts
✅ Deployment skills
✅ GitHub practices

## ❓ Common Questions

**Q: Why not just use ChatGPT?**
A: ChatGPT doesn't know about YOUR documents. This system does.

**Q: Why Ollama instead of OpenAI API?**
A: Ollama is free and runs locally. Great for learning and privacy.

**Q: Can I use different documents?**
A: Yes! Just put .txt files in `documents/` folder.

**Q: How long does it take to process documents?**
A: Depends on size. Usually 1-5 minutes.

---

## 👤 About Me

This project demonstrates:
- Understanding of AI/ML concepts
- Clean code practices
- Ability to build complete applications
- Deployment skills
- Documentation skills

---
