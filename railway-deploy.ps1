# Railway Deployment Script for Backend

Write-Host "🚀 Setting up Railway deployment for backend..." -ForegroundColor Green

# Check current project status
Write-Host "📋 Current Railway status:" -ForegroundColor Yellow
railway status

# Try to create a new service by deploying
Write-Host "🔧 Creating new service and deploying..." -ForegroundColor Yellow

# Set essential environment variables first
$env_vars = @(
    "DEBUG=False",
    "SECRET_KEY=django-insecure-production-key-change-this-in-railway-dashboard",
    "DATABASE_URL=postgresql://postgres:vRXnewGNSGzkqibrCDPEbonqiClCYMPC@postgres.railway.internal:5432/railway"
)

Write-Host "Setting environment variables..." -ForegroundColor Cyan
foreach ($var in $env_vars) {
    Write-Host "Setting: $var" -ForegroundColor Gray
    railway variables --set $var --skip-deploys
}

Write-Host "✅ Environment variables set!" -ForegroundColor Green
Write-Host "🚀 Now deploying the application..." -ForegroundColor Green

# Deploy the application
railway up

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Your backend will be available at your Railway app URL + /api/" -ForegroundColor Cyan