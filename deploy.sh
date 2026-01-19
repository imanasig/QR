#!/bin/bash

# Quick deployment script for Render/Railway/Heroku

echo "🚀 Preparing Membership QR System for deployment..."

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
fi

# Add all files
echo "📁 Adding files to Git..."
git add .

# Commit
echo "💾 Creating commit..."
git commit -m "Production-ready Membership QR System" || echo "Nothing to commit or already committed"

echo ""
echo "✅ Your project is ready for deployment!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Create a GitHub repository at: https://github.com/new"
echo "2. Run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Then deploy to Render:"
echo "   - Sign up at https://render.com"
echo "   - Click 'New +' → 'Web Service'"
echo "   - Connect your GitHub repo"
echo "   - Render will auto-detect and deploy!"
echo ""
echo "📖 Full deployment guide: See DEPLOYMENT.md"
echo ""
