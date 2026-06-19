# 🚀 Deploy to Streamlit Cloud

Your RAG Company Assistant is ready to deploy! Here's how to share it with others.

## Step 1: Push to GitHub

1. Create a new GitHub repository
2. Initialize git in your project:
   ```bash
   cd /Users/poorvagupta/Documents/RAG-Company-Assistant
   git init
   git add .
   git commit -m "Initial commit: RAG Company Assistant"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/rag-company-assistant.git
   git push -u origin main
   ```

## Step 2: Deploy on Streamlit Cloud

### Option A: Streamlit Cloud (Easiest)

1. Go to: https://streamlit.io/cloud
2. Click "Sign up with GitHub"
3. Authorize Streamlit
4. Click "New app" → "Create app"
5. Fill in:
   - **GitHub account**: Your username
   - **Repository**: rag-company-assistant
   - **Branch**: main
   - **Main file path**: `app.py`
6. Click "Deploy"

**Your app is now live!** Share the URL with your team.

### Option B: Railway (Alternative)

1. Go to: https://railway.app
2. Connect your GitHub account
3. Create new project → Deploy from GitHub repo
4. Select `rag-company-assistant`
5. Configure environment:
   - Set PORT to 8501
6. Click deploy

## Step 3: Configure for Production

### Environment Variables (if needed)

Create `.streamlit/secrets.toml` for any secrets:
```toml
# Don't commit this file!
ollama_url = "http://your-ollama-server.com"
```

### Document Location

The app looks for documents at:
```python
DOCUMENT_PATH = "/Users/poorvagupta/Downloads/Company_Documents for RAG/"
```

**For cloud deployment**, you have options:
1. **Option A**: Store documents in GitHub (included with repo)
2. **Option B**: Load from cloud storage (S3, Google Drive, etc.)
3. **Option C**: Use an API endpoint

## Step 4: Important Notes

### ⚠️ Ollama Server

The app requires Ollama running locally on:
```
http://localhost:11434
```

**For cloud deployment**, you need to:

**Option 1: Self-hosted Ollama**
- Deploy Ollama on your own server
- Update `app.py` to point to your Ollama URL

**Option 2: Docker + Cloud**
- Package Ollama in Docker
- Deploy container alongside your app

**Option 3: Use API**
- Keep Ollama running locally
- Expose via ngrok: `ngrok http 11434`
- Update app to use ngrok URL

### Document Updates

If documents change, either:
1. Push new documents to GitHub repo
2. Pull latest from source directory
3. Implement file upload feature

## Step 5: Share Your App

Once deployed:
- **Public Link**: Share directly with anyone
- **Private Access**: Restrict to GitHub users
- **Embed**: Add to your website/intranet

Example URL:
```
https://rag-company-assistant-YOUR_USERNAME.streamlit.app
```

## Quick Checklist

- [ ] Create GitHub account
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Connect Streamlit Cloud account
- [ ] Configure Ollama server access
- [ ] Deploy app
- [ ] Test with sample questions
- [ ] Share URL with team

## Troubleshooting

### "Cannot connect to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check URL in code: `http://localhost:11434`
- For cloud: use public Ollama server or ngrok

### "Documents not found"
- Update `DOCUMENT_PATH` in `app.py`
- Or store documents in app directory

### "App is slow"
- Check Ollama server resources
- Reduce `CHUNK_SIZE` in rag_utils.py
- Use faster models if available

## Support

- **Streamlit Docs**: https://docs.streamlit.io/deploy/streamlit-cloud
- **Railway Docs**: https://docs.railway.app
- **Ollama Docs**: https://ollama.ai

---

**Next Steps:**
1. Create GitHub repo
2. Push your code
3. Deploy on Streamlit Cloud
4. Share the link!

Need help? Check your local setup first, then configure cloud deployment.
