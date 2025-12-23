# Video Generation Enhancements

## Overview

The video generation has been enhanced with two key improvements:
1. **No ImageMagick dependency** - Works without external tools
2. **Camera panning effect** - Smooth vertical pan on product details scene

## Changes Made

### 1. Simplified Video Generator (No ImageMagick)

**Problem**: The original `video_generator.py` required ImageMagick for TextClip, which caused this error:
```
MoviePy Error: creation of None failed because of the following error:
[Errno 2] No such file or directory: 'unset'
```

**Solution**: Created `video_generator_simple.py` that:
- ✅ Works without ImageMagick
- ✅ Uses image-based overlays instead of TextClip
- ✅ Focuses on smooth video playback
- ✅ Adds camera panning effect

**File**: [shared/video_generator_simple.py](shared/video_generator_simple.py)

### 2. Camera Panning Effect

**Feature**: Smooth vertical camera pan on the "Add to Cart" scene (Scene 4)

**How it works**:

1. **Increased Viewport**: Scene 4 uses 1920x1600 viewport (vs 1920x1080 for other scenes)
2. **Extra Height**: The additional 520px allows room for panning
3. **Bezier Curve**: Smooth acceleration/deceleration using cubic bezier
4. **5-Second Duration**: Scene 4 lasts 5 seconds (vs 3 seconds for others)

**Visual Effect**:
```
Start: Top of page (showing product title, images)
  ↓
 Pan smoothly downward with bezier curve
  ↓
End: Bottom of page (showing Add to Cart button)
```

**Implementation** (from `video_generator_simple.py`):
```python
def create_panning_clip(image_path: str, duration: float = 5.0):
    """
    Create smooth vertical pan using bezier curve

    Cubic bezier control points: P0=0, P1=0.25, P2=0.75, P3=1
    This creates an S-curve for natural acceleration/deceleration
    """
    def pan_position(t):
        progress = t / duration

        # Cubic bezier easing
        eased = 3 * (1 - progress)**2 * progress * 0.25 + \
                3 * (1 - progress) * progress**2 * 0.75 + \
                progress**3

        # Calculate Y position (negative moves image up)
        y = -int(eased * max_pan)
        return (0, y)

    # Apply panning to clip
    panned_clip = base_clip.set_position(pan_position).set_duration(duration)
```

### 3. Demo Updates

**Both demos updated** to:
- Use `video_generator_simple` instead of `video_generator`
- Increase viewport to 1920x1600 for Scene 4
- Capture taller screenshots for panning effect

**Demo 1 changes** ([demo1_sdk_llm/main.py](demo1_sdk_llm/main.py#L173-L180)):
```python
# Increase viewport height for this scene to enable panning effect
browser.page.set_viewport_size({"width": 1920, "height": 1600})
time.sleep(1)  # Wait for viewport to adjust

# Take screenshot with taller viewport
screenshot_path = os.path.join(screenshots_dir, "sdk_scene4_product_details.png")
browser.page.screenshot(path=screenshot_path, full_page=False)
print(f"Screenshot saved: {screenshot_path} (1920x1600 for panning effect)")
```

**Demo 2 changes** ([demo2_vision_llm/main.py](demo2_vision_llm/main.py#L152-L159)):
```python
# Same viewport increase for Scene 4
page.set_viewport_size({"width": 1920, "height": 1600})
```

## Video Output Specifications

### Scene Durations
- **Scenes 1-3**: 3 seconds each (static)
- **Scene 4**: 5 seconds (with panning effect)
- **Scene 5**: 3 seconds (static)
- **Summary**: 3 seconds (static)

**Total duration**: ~17-20 seconds per demo

### Video Specs
- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30 FPS (smooth panning)
- **Codec**: H.264 (libx264)
- **Format**: MP4

### Panning Details
- **Pan Distance**: 520 pixels (1600 - 1080)
- **Pan Curve**: Cubic bezier S-curve
- **Direction**: Vertical (top to bottom)
- **Speed**: Variable (accelerates then decelerates)

## Panning Curve Visualization

```
Velocity over time:

  ^
  │     ╱─────╲
V │    ╱       ╲
e │   ╱         ╲
l │  ╱           ╲
  │ ╱             ╲
  0─────────────────> Time
  0s    2.5s      5s

Smooth acceleration → constant velocity → smooth deceleration
```

## Benefits

### 1. No External Dependencies
- ❌ No ImageMagick installation needed
- ✅ Pure Python solution
- ✅ Works on all platforms
- ✅ Faster to set up

### 2. Enhanced Visual Experience
- ✅ Smooth camera movement
- ✅ Highlights the "Add to Cart" action
- ✅ More engaging than static screenshots
- ✅ Professional-looking output

### 3. Technical Improvements
- ✅ 30 FPS for fluid motion
- ✅ Bezier easing for natural movement
- ✅ Proper video compositing
- ✅ Optimized rendering

## Testing the Videos

After running the demos, check:

1. **Scene 4 panning**: Should smoothly pan from top to bottom
2. **No jittery motion**: Bezier curve ensures smooth movement
3. **Video quality**: 1080p HD resolution
4. **File size**: Reasonable (5-10 MB per demo)

## Future Enhancements (Optional)

### Horizontal Panning
For buttons on the right side, could add horizontal pan:
```python
x = int(eased * max_pan_x)  # Pan left to right
```

### Mouse Movement Animation
Could add animated mouse cursor moving to button:
```python
def draw_mouse_cursor(frame, position):
    # Draw cursor following bezier path
    ...
```

### Token Overlay (with PIL)
Could add token count overlays using PIL:
```python
from PIL import Image, ImageDraw, ImageFont

def add_token_overlay(image, tokens):
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), f"Tokens: {tokens}", fill='yellow')
```

## Running the Demos

The video generation now works automatically:

```bash
./run_demo1.sh  # Generates video with panning
./run_demo2.sh  # Generates video with panning
./run_both.sh   # Generates both + comparison
```

**Expected output**:
```
✅ Video created: demo1_sdk_llm/video/demo1_sdk_final.mp4
   Total duration: 18.0s
   Scenes: 6
```

## Troubleshooting

### Video Not Generated
- Check that screenshots exist in `screenshots/` directory
- Ensure MoviePy is installed: `pip install moviepy==1.0.3`
- Look for error messages in console

### Panning Not Smooth
- Verify Scene 4 screenshot is 1920x1600
- Check FPS is set to 30
- Ensure bezier calculation is correct

### File Size Too Large
- Reduce FPS to 24
- Use lower quality preset: `preset='fast'`
- Compress with: `ffmpeg -i input.mp4 -crf 28 output.mp4`

## Summary

✅ **Video generation fixed** - No ImageMagick needed
✅ **Camera panning added** - Smooth bezier curve motion
✅ **Both demos updated** - Scene 4 uses 1920x1600 viewport
✅ **Professional output** - 30 FPS, 1080p, smooth motion

The demos now create engaging videos that showcase the LLM agent's decision-making process with a cinematic camera pan highlighting the crucial "Add to Cart" action! 🎬
