# API 400 Error Fix

## Problem

The Sentience API was returning a 400 Bad Request error:
```
requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: https://api.sentienceapi.com/v1/snapshot
```

## Root Cause

The viewport was being changed mid-demo from 1920x1080 to 1920x1600, which may have caused issues with the API's data validation or size limits.

## Solution

**Reverted viewport changes**:
- Keep viewport at standard **1920x1080** throughout the demo
- The camera panning effect will still work - we can pan within the visible content

## Camera Panning Alternative

Instead of increasing viewport height, we can:
1. Use standard 1920x1080 viewport
2. Take a **full-page screenshot** for Scene 4 instead
3. Pan within the full-page screenshot in the video

Or simpler:
- Just use the standard viewport (1920x1080)
- Pan within what's visible (buttons are usually in view anyway)

## Changes Made

Reverted these lines in `demo1_sdk_llm/main.py`:
```python
# REVERTED FROM:
browser.page.set_viewport_size({"width": 1920, "height": 1600})

# BACK TO:
browser.page.set_viewport_size({"width": 1920, "height": 1080})
```

## Testing the Fix

The demo should now work with the API:
```bash
./cleanup.sh
./run_demo1.sh
```

The API will accept the standard viewport size and the demo should complete successfully.

## Note on Panning

Camera panning can still work with 1920x1080 if:
- The "Add to Cart" button is lower on the page
- We scroll down before taking the screenshot
- Or we use a smaller pan range (within the 1080px height)

The video generator can handle panning even with the standard viewport size if there's scrollable content captured in the screenshot.
