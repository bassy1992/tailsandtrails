# Vercel Deployment Guide

## 🚀 Deploying Video URL Updates to Vercel

### Current Status
- ✅ Frontend code updated to load videos from gallery API
- ✅ Fallback system in place for hardcoded videos
- ✅ Environment variables configured for production
- ✅ Changes committed and pushed to GitHub

### Automatic Deployment
Vercel will automatically deploy when you push to the `master` branch. The deployment includes:

1. **Updated Home Page** (`client/pages/Index.tsx`):
   - Loads videos from `/api/gallery/videos/?featured=true`
   - Transforms API data to match VideoSection component
   - Falls back to hardcoded videos if API fails

2. **Updated API Client** (`client/lib/api.ts`):
   - Includes `GalleryVideo` interface
   - Supports video URL field

3. **Environment Configuration**:
   - `VITE_API_URL=https://tailsandtrails-production.up.railway.app/api`
   - Points to Railway backend

### Backend Requirements
The Railway backend must have:
- ✅ Gallery video models migrated
- ✅ Video URL field added
- ✅ Sample videos with URLs

### Deployment Steps

#### 1. Verify Backend is Ready
```bash
# Test the API endpoint
curl https://tailsandtrails-production.up.railway.app/api/gallery/videos/?featured=true

# Should return videos with video_url field
```

#### 2. Deploy to Vercel
The deployment happens automatically when you push to GitHub. You can also trigger manually:

```bash
# If using Vercel CLI
vercel --prod

# Or push to trigger auto-deployment
git push origin master
```

#### 3. Verify Deployment
After deployment, check:
- Home page loads without errors
- Video section shows videos from database
- Videos play correctly
- Fallback works if API is unavailable

### Environment Variables in Vercel

Make sure these are set in your Vercel project settings:

```
VITE_API_BASE_URL=https://tailsandtrails-production.up.railway.app
VITE_API_URL=https://tailsandtrails-production.up.railway.app/api
```

### Troubleshooting

#### If videos don't load:
1. Check browser console for API errors
2. Verify Railway backend is running
3. Check CORS settings on backend
4. Fallback videos should still display

#### If deployment fails:
1. Check Vercel build logs
2. Verify all dependencies are in package.json
3. Check for TypeScript errors

#### If API calls fail:
1. Verify backend URL in environment variables
2. Check Railway deployment status
3. Test API endpoints directly

### Expected Behavior

After successful deployment:

1. **Home Page**:
   - Loads 3 featured videos from gallery API
   - Shows video thumbnails, titles, descriptions
   - Videos play when clicked
   - Falls back to hardcoded videos if API fails

2. **Video Data**:
   - Comes from Railway database
   - Uses Pexels video URLs
   - Includes proper metadata (duration, views, etc.)

3. **Performance**:
   - Fast loading (videos are URLs, not files)
   - Responsive design works
   - SEO-friendly

### Manual Deployment Commands

If you need to deploy manually:

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Check deployment status
vercel ls
```

### Post-Deployment Verification

1. Visit your Vercel URL
2. Check home page loads
3. Verify video section appears
4. Test video playback
5. Check mobile responsiveness

The deployment should be seamless since the frontend has fallback mechanisms! 🎉