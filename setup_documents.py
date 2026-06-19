#!/usr/bin/env python3
"""
Helper script to load company documents and test the RAG pipeline
"""

import os
import shutil
from pathlib import Path

# Paths
SOURCE_DOCS = "/Users/poorvagupta/Downloads/Company_Documents for RAG/"
UPLOAD_FOLDER = "/Users/poorvagupta/Documents/RAG-Company-Assistant/uploaded_documents"
PROJECT_DIR = "/Users/poorvagupta/Documents/RAG-Company-Assistant"

def copy_documents():
    """Copy company documents to upload folder"""
    print("📋 Copying company documents...")
    
    # Create upload folder if needed
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    if not os.path.exists(SOURCE_DOCS):
        print(f"❌ Source documents not found at {SOURCE_DOCS}")
        return False
    
    # Copy all txt files
    doc_count = 0
    for file in os.listdir(SOURCE_DOCS):
        if file.endswith('.txt'):
            src = os.path.join(SOURCE_DOCS, file)
            dst = os.path.join(UPLOAD_FOLDER, file)
            try:
                shutil.copy2(src, dst)
                print(f"✅ Copied: {file}")
                doc_count += 1
            except Exception as e:
                print(f"❌ Error copying {file}: {e}")
    
    print(f"\n✅ Copied {doc_count} documents to {UPLOAD_FOLDER}")
    return True

def list_documents():
    """List uploaded documents"""
    print("\n📁 Uploaded Documents:")
    if os.path.exists(UPLOAD_FOLDER):
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.txt')]
        if files:
            for i, file in enumerate(files, 1):
                file_path = os.path.join(UPLOAD_FOLDER, file)
                size = os.path.getsize(file_path) / 1024  # KB
                print(f"  {i}. {file} ({size:.1f} KB)")
        else:
            print("  No documents found")
    else:
        print("  Upload folder does not exist")

def show_instructions():
    """Show instructions for using the system"""
    print("\n" + "="*60)
    print("🚀 NEXT STEPS")
    print("="*60)
    print("""
1. Make sure Ollama is running:
   - Open Ollama app or run: ollama serve
   - Ensure nomic-embed-text and llama3 models are available
   
2. Start the Streamlit app:
   cd {project_dir}
   python3 -m streamlit run streamlit_app.py
   
3. In the web UI:
   - Go to ⚙️ Admin Panel tab
   - Click "Process and Index Documents"
   - Wait for processing to complete
   
4. Go to 💬 Chat tab and start asking questions!

Example questions to ask:
   - "What is the deployment process?"
   - "What are the employee benefits?"
   - "How do I troubleshoot issues?"
   - "What is FintechAI Pro?"
""".format(project_dir=PROJECT_DIR))

if __name__ == "__main__":
    print("\n" + "="*60)
    print("📚 RAG Company Documents Setup")
    print("="*60)
    
    # Copy documents
    if copy_documents():
        # List them
        list_documents()
        # Show instructions
        show_instructions()
        print("\n✅ Setup complete! Your documents are ready to load.")
    else:
        print("\n❌ Setup failed. Please check the paths.")
