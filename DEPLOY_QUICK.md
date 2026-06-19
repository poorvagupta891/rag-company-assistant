# 🚀 Deployment Quick Start

Your RAG Assistant is ready to deploy! Here's the easiest path:

## 🎯 5-Minute Deployment

### 1. Push to GitHub
```bash
cd /Users/poorvagupta/Documents/RAG-Company-Assistant

# Initialize git (if not already done)
git init
git add .
git commit -m "RAG Company Assistant - Ready to deploy"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/rag-company-assistant.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to: **https://streamlit.io/cloud**
2. Click "New app"
3. Select your GitHub repo
4. Set Main file: `app.py` or `app_cloud.py`
5. Click "Deploy" ✅

**Your app is live!**

---

## 📋 What's Included

```
✅ app.py              - Main RAG web UI (works locally)
✅ app_cloud.py        - Cloud version (handles remote Ollama)
✅ rag_utils.py        - Your original RAG pipeline (unchanged)
✅ requirements.txt    - All dependencies
✅ .streamlit/config.toml - Streamlit configuration
✅ DEPLOY.md          - Full deployment guide
```

---

## ⚠️ Important: Ollama Server

**Your app needs Ollama running!**

### For Local Use:
```bash
ollama serve  # Keep running while using the app
```

### For Cloud Deployment:
You need one of these options:

**Option A: Self-Hosted Ollama**
- Deploy Ollama on your server
- Update `OLLAMA_URL` in app
- Only works on your network

**Option B: Use ngrok (Free)**
```bash
# Terminal 1: Run Ollama
ollama serve

# Terminal 2: Expose with ngrok
ngrok http 11434

# Copy the URL and set environment variable
export OLLAMA_URL="https://xxxxx-xx-xxx-xx.ngrok.io"
```

**Option C: Docker (Advanced)**
- Containerize Ollama + App together
- Deploy to Railway, Render, etc.

---

## 🎯 Quick Links

- **Streamlit Cloud**: https://streamlit.io/cloud
- **GitHub**: https://github.com
- **Ollama**: https://ollama.ai
- **Full Guide**: See `DEPLOY.md`

---

## 💡 Next Steps

1. **Create GitHub account** (if needed)
2. **Push your code**
3. **Deploy on Streamlit Cloud**
4. **Configure Ollama access**
5. **Share the link with your team**

---

## 🆘 Troubleshooting

**"Cannot connect to Ollama"**
- Ensure Ollama is running
- Check URL is correct
- For cloud: use ngrok or self-hosted

**"Documents not found"**
- Commit documents to GitHub repo, or
- Upload documents through app, or
- Set DOCUMENT_PATH environment variable

**"App is slow"**
- Check Ollama server resources
- Use faster models
- Increase timeout settings

---

**Questions?** Check `DEPLOY.md` for detailed instructions!
