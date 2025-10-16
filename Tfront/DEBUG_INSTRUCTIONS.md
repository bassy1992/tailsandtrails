# 🔍 Debug Instructions for Live Site

## 🎯 **Problem Identified**
- ✅ Production API has 6 images for Cape Coast Castle
- ✅ Detail endpoint returns all 6 images  
- ❌ Frontend slider not showing - likely a JavaScript issue

## 🧪 **Debug Steps**

### 1. **Open Browser Developer Tools**
1. Go to your deployed frontend URL + /gallery
2. Press **F12** to open Developer Tools
3. Go to **Console** tab
4. Keep it open while testing

### 2. **Test Cape Coast Castle Click**
1. Click on "Cape Coast Castle" card
2. Watch the Console for these messages:
   ```
   🔍 Fetching gallery details for slug: cape-coast-castle-cape-coast-gallery
   🌐 API: Calling getGallery with slug: cape-coast-castle-cape-coast-gallery
   🌐 API: Complete URL: https://tailsandtrails-production.up.railway.app/api/gallery/galleries/cape-coast-castle-cape-coast-gallery/
   🌐 API: Images in response: 6
   ✅ Received gallery details: [object with 6 images]
   ```

### 3. **Check Modal Content**
When the modal opens, look for:
- **Yellow Debug Panel** at the top showing:
  ```
  Debug Info:
  Gallery Title: Cape Coast Castle
  Images Array: 6 images
  Image Count Property: 6
  Current Index: 0
  ```

### 4. **Expected vs Actual**

**If Working Correctly:**
- ✅ Console shows "Images in response: 6"
- ✅ Yellow debug panel shows "Images Array: 6 images"
- ✅ You see image slider with arrows
- ✅ Counter shows "1 / 6"
- ✅ Thumbnail bar at bottom

**If Not Working:**
- ❌ Console shows errors
- ❌ Debug panel shows "Images Array: undefined" or "0 images"
- ❌ No arrows visible
- ❌ Only one image, no slider

## 🚨 **Common Issues & Solutions**

### Issue 1: API Call Fails
**Symptoms**: Console shows network errors
**Solution**: CORS issue or API down

### Issue 2: API Returns Empty Images
**Symptoms**: "Images in response: 0"
**Solution**: Backend database issue

### Issue 3: Frontend JavaScript Error
**Symptoms**: Console shows JavaScript errors
**Solution**: Code issue in slider logic

### Issue 4: Modal Doesn't Open
**Symptoms**: No modal appears when clicking
**Solution**: Click handler not working

## 📱 **Mobile Testing**
Also test on mobile:
1. Open site on phone
2. Click Cape Coast Castle
3. Try swiping left/right
4. Check if touch gestures work

## 🔧 **Quick Fix Test**
If the debug panel shows "Images Array: 6 images" but no slider:
- The API is working
- The issue is in the slider rendering logic
- Check for CSS/JavaScript errors

## 📊 **Expected Production API Response**
The detail endpoint should return:
```json
{
  "title": "Cape Coast Castle",
  "image_count": 6,
  "images": [
    {"caption": "Historic Cape Coast Castle exterior view", "is_main": true},
    {"caption": "Castle courtyard and colonial architecture"},
    {"caption": "Historical dungeons - Door of No Return"},
    {"caption": "Stunning Atlantic Ocean view from castle walls"},
    {"caption": "Castle museum displaying Ghana's history"},
    {"caption": "Beautiful sunset over Cape Coast Castle"}
  ]
}
```

## 🎯 **Next Steps**
1. Follow debug steps above
2. Report what you see in console
3. Check if debug panel appears
4. Note any JavaScript errors
5. Test on both desktop and mobile

This will help identify exactly where the issue is! 🔍