#!/bin/bash

echo "🚀 Deploying Backend to Railway"
echo "================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    echo "Please install Railway CLI first:"
    echo "npm install -g @railway/cli"
    echo "or visit: https://docs.railway.app/develop/cli"
    exit 1
fi

# Login to Railway (if not already logged in)
echo "🔐 Checking Railway authentication..."
railway whoami || railway login

# Initialize Railway project (if not already initialized)
if [ ! -f "railway.toml" ]; then
    echo "📝 Initializing Railway project..."
    railway init
fi

# Deploy the project
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment initiated!"
echo ""
echo "Next steps:"
echo "1. Go to your Railway dashboard"
echo "2. Add a PostgreSQL database"
echo "3. Configure environment variables (see RAILWAY_DEPLOYMENT.md)"
echo "4. Your API will be available at: https://your-app.railway.app/api/"