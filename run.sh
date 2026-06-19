#!/bin/bash

echo "🚀 Starting RAG Company Assistant..."
echo ""
echo "Checking dependencies..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

# Check if streamlit is installed
python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if Ollama is running
echo "🔍 Checking for Ollama..."
curl -s http://localhost:11434 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Ollama doesn't seem to be running."
    echo "   Make sure Ollama is running on http://localhost:11434"
    echo "   Download from: https://ollama.ai"
    echo ""
fi

echo "✅ Starting Streamlit app..."
echo ""
streamlit run streamlit_app.py
