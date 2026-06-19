#!/bin/bash
# Setup script to push your RAG Assistant to GitHub
# Replace REPO_NAME with your desired repository name

echo "🚀 Setting up GitHub repository for RAG Assistant"
echo ""

# Configuration
GITHUB_USERNAME="poorvagupta891"
REPO_NAME="rag-company-assistant"

echo "📋 GitHub Setup:"
echo "   Username: $GITHUB_USERNAME"
echo "   Repo Name: $REPO_NAME"
echo ""

# Step 1: Check if git is installed
echo "1️⃣  Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git first:"
    echo "   brew install git"
    exit 1
fi
echo "✅ Git is installed"
echo ""

# Step 2: Initialize git repository
echo "2️⃣  Initializing Git repository..."
git init
echo "✅ Git initialized"
echo ""

# Step 3: Configure git (if needed)
echo "3️⃣  Configuring Git..."
git config user.name "Your Name" 2>/dev/null || true
git config user.email "your.email@example.com" 2>/dev/null || true
echo "✅ Git configured"
echo ""

# Step 4: Add all files
echo "4️⃣  Adding files..."
git add .
echo "✅ Files added"
echo ""

# Step 5: Create initial commit
echo "5️⃣  Creating initial commit..."
git commit -m "Initial commit: RAG Company Assistant - AI-powered document search"
echo "✅ Commit created"
echo ""

# Step 6: Rename branch to main
echo "6️⃣  Setting up main branch..."
git branch -M main
echo "✅ Branch set to main"
echo ""

# Step 7: Instructions for remote
echo "7️⃣  Next steps to complete:"
echo ""
echo "   1. Go to: https://github.com/new"
echo "   2. Create a new repository named: $REPO_NAME"
echo "   3. DO NOT initialize with README, .gitignore, or license"
echo "   4. Copy the HTTPS URL from the new repo"
echo "   5. Run these commands:"
echo ""
echo "   git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "   OR if using SSH:"
echo ""
echo "   git remote add origin git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Full instructions at: DEPLOY_QUICK.md"
