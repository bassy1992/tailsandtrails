@echo off
echo 🚀 Deploying Backend to Railway
echo ================================

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found. Installing...
    echo Please install Railway CLI first:
    echo npm install -g @railway/cli
    echo or visit: https://docs.railway.app/develop/cli
    pause
    exit /b 1
)

REM Login to Railway (if not already logged in)
echo 🔐 Checking Railway authentication...
railway whoami || railway login

REM Initialize Railway project (if not already initialized)
if not exist "railway.toml" (
    echo 📝 Initializing Railway project...
    railway init
)

REM Deploy the project
echo 🚀 Deploying to Railway...
railway up

echo ✅ Deployment initiated!
echo.
echo Next steps:
echo 1. Go to your Railway dashboard
echo 2. Add a PostgreSQL database
echo 3. Configure environment variables (see RAILWAY_DEPLOYMENT.md)
echo 4. Your API will be available at: https://your-app.railway.app/api/
pause