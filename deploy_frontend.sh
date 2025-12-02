#!/bin/bash

echo "=========================================="
echo "DEPLOYING FRONTEND FIXES"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "Tfront" ]; then
    echo "❌ Error: Tfront directory not found"
    echo "Please run this script from the project root"
    exit 1
fi

echo "📦 Building frontend..."
cd Tfront

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📥 Installing dependencies..."
    npm install
fi

# Build the frontend
echo "🔨 Building production bundle..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📤 Next steps:"
    echo "1. Commit the changes:"
    echo "   git add ."
    echo "   git commit -m 'Fix payment success page error'"
    echo "   git push origin main"
    echo ""
    echo "2. If using Vercel/Netlify, it will auto-deploy"
    echo "3. If using Railway, push to trigger deployment"
    echo ""
    echo "The payment success error should be fixed after deployment."
else
    echo "❌ Build failed!"
    echo "Please check the error messages above"
    exit 1
fi
