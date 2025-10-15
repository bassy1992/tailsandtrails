# 🚀 Vercel Deployment Checklist

## ✅ **Pre-Deployment Steps**

### 1. **Backend Deployment (Railway)**
The frontend calls the Railway backend, so backend must be deployed first:

```bash
# In Tback directory
git add .
git commit -m "deploy: gallery slider with multiple images support"
git push origin master
```

**Verify Backend:**
- Check: https://tailsandtrails-production.up.railway.app/api/gallery/galleries/
- Should return galleries with image_count > 1
- Check: https://tailsandtrails-production.up.railway.app/api/gallery/galleries/cape-coast-castle-cape-coast-gallery/
- Should return 6 images in the images array

### 2. **Frontend Deployment (Vercel)**

```bash
# In Tfront directory
git add .
git commit -m "deploy: image slider for gallery modal"
git push origin master
```

Then deploy to Vercel:
```bash
vercel --prod
```

Or use Vercel dashboard to deploy from GitHub.

## 🔧 **Environment Variables**

Vercel is configured to use:
- **API URL**: `https://tailsandtrails-production.up.railway.app/api`
- **Base URL**: `https://tailsandtrails-production.up.railway.app`

## 🧪 **Testing After Deployment**

### 1. **Gallery Page Test**
1. Go to deployed Vercel URL
2. Navigate to Gallery page
3. Click on "Cape Coast Castle"
4. **Expected Results**:
   - Modal opens with image slider
   - Shows "1 / 6" counter in top-right
   - Left/right arrow buttons visible
   - 6 thumbnail images at bottom
   - Can navigate through all images

### 2. **Debug Information**
If issues occur, check browser console for:
- `🔍 Fetching gallery details for slug: cape-coast-castle-cape-coast-gallery`
- `🌐 API: Complete URL: https://tailsandtrails-production.up.railway.app/api/gallery/galleries/cape-coast-castle-cape-coast-gallery/`
- `🌐 API: Images in response: 6`

### 3. **Mobile Testing**
- Test swipe gestures on mobile
- Verify responsive design
- Check touch navigation

## 🎯 **Expected Features**

### Cape Coast Castle Gallery:
1. **Historic Cape Coast Castle exterior view** (Main)
2. **Castle courtyard and colonial architecture**
3. **Historical dungeons - Door of No Return**
4. **Stunning Atlantic Ocean view from castle walls**
5. **Castle museum displaying Ghana's history**
6. **Beautiful sunset over Cape Coast Castle**

### Navigation Options:
- **Arrow buttons**: Left/right navigation
- **Keyboard**: Arrow keys (← →)
- **Touch**: Swipe left/right on mobile
- **Thumbnails**: Click any thumbnail to jump to image
- **Counter**: Shows current position (1/6, 2/6, etc.)

## 🚨 **Troubleshooting**

### If only 1 image shows:
1. Check backend API response
2. Verify Railway deployment is complete
3. Clear browser cache
4. Check console for API errors

### If arrows don't appear:
- Backend is not returning multiple images
- Check Railway logs for errors
- Verify database has multiple images

### If API calls fail:
- CORS issues between Vercel and Railway
- Check environment variables
- Verify Railway backend is accessible

## 📱 **Mobile Considerations**
- Swipe gestures work on touch devices
- Responsive design adapts to screen size
- Touch targets are optimized for mobile

## 🎉 **Success Criteria**
- ✅ Gallery page loads without errors
- ✅ Cape Coast Castle shows "6 photos" badge
- ✅ Modal opens with image slider
- ✅ All 6 images are navigable
- ✅ Arrows and thumbnails work
- ✅ Mobile swipe gestures work
- ✅ Keyboard navigation works