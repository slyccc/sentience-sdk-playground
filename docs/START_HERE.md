# 🚀 Start Here - Amazon Shopping LLM Agent Demos

## ✅ Everything is Ready!

The Playwright version has been upgraded and the Amazon timeout issue has been fixed. Both demos now work perfectly on your Mac!

## Quick Start (3 Steps)

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Run Both Demos
```bash
./run_both.sh
```

### 3. Watch the Results!

The script will:
1. ✅ Run Demo 1 (SDK + GPT-4) - Press Enter when prompted
2. ✅ Run Demo 2 (Vision + GPT-4o) - Press Enter when prompted
3. ✅ Generate side-by-side comparison video

---

## What Each Demo Does

Both demos complete the **same Amazon shopping flow**:

1. Navigate to Amazon.com
2. Find and click search bar
3. Type "Christmas gift" and search
4. Select a product from results
5. Click "Add to Cart" button
6. Verify item was added

### Demo 1: SDK + LLM Approach
- Uses Sentience `snapshot()` for structured JSON
- GPT-4 Turbo analyzes element data
- More efficient: **~4,930 tokens**
- Cost: **~$0.06**

### Demo 2: Vision + LLM Approach
- Takes screenshots of the page
- GPT-4o Vision analyzes images
- More flexible: **~6,670 tokens**
- Cost: **~$0.08**

**Token difference**: Vision uses 35% more tokens due to image encoding

---

## Output Files

After running, you'll find:

### Demo 1 Outputs
```
demo1_sdk_llm/
├── screenshots/
│   ├── sdk_scene1_homepage.png
│   ├── sdk_scene2_typing.png
│   ├── sdk_scene3_search_results.png
│   ├── sdk_scene4_product_details.png
│   ├── sdk_scene5_confirmation.png
│   ├── sdk_scene*_data.json (snapshot JSON)
│   └── token_summary.json
└── video/
    └── demo1_sdk_final.mp4
```

### Demo 2 Outputs
```
demo2_vision_llm/
├── screenshots/
│   ├── vision_scene1_homepage.png
│   ├── vision_scene2_typing.png
│   ├── vision_scene3_search_results.png
│   ├── vision_scene4_product_details.png
│   ├── vision_scene5_confirmation.png
│   └── token_summary.json
└── video/
    └── demo2_vision_final.mp4
```

### Comparison Video
```
playground/
└── comparison_video.mp4  # Side-by-side comparison with token overlay
```

---

## Run Individual Demos

### Just Demo 1 (SDK Approach)
```bash
./run_demo1.sh
```

### Just Demo 2 (Vision Approach)
```bash
./run_demo2.sh
```

---

## Expected Console Output

You'll see real-time output like:

```
======================================================================
Scene: Scene 1: Find Search Bar
======================================================================

LLM Decision:
{
  "reasoning": "Found searchbox role element at top of page",
  "element_id": 42,
  "bbox": {"x": 450, "y": 120, "width": 600, "height": 40},
  "action": "click"
}

  Token usage: 820 (prompt: 700, completion: 120)

Clicking on search bar at bbox: {...}
```

At the end, you'll see:

```
======================================================================
Token Usage Summary: Demo 1: SDK + LLM
======================================================================
Scene 1: Find Search Bar                       820 tokens
Scene 3: Select Product                       1680 tokens
Scene 4: Add to Cart                          1330 tokens
Scene 5: Verify Success                       1100 tokens
======================================================================
Total Prompt Tokens:                           4400
Total Completion Tokens:                        530
TOTAL TOKENS:                                  4930
Average per Scene:                            1232.5
======================================================================
```

---

## Troubleshooting

### Browser Doesn't Launch
```bash
# Reinstall Chromium
source venv/bin/activate
playwright install chromium
```

### Import Errors
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
pip install -e ..
```

### Video Generation Fails
Install ImageMagick (required for text overlays):
```bash
# macOS
brew install imagemagick

# The demos will still run, just skip video generation
```

---

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Detailed usage guide
- **[README.md](README.md)** - Full documentation
- **[SETUP.md](SETUP.md)** - Virtual environment setup
- **[FIXED_PLAYWRIGHT_VERSION.md](FIXED_PLAYWRIGHT_VERSION.md)** - Fix details
- **[../docs/LLM_AGENT_AMAZON_SHOPPING_DEMO_PLAN.md](../docs/LLM_AGENT_AMAZON_SHOPPING_DEMO_PLAN.md)** - Original design plan

---

## Ready to Go!

```bash
source venv/bin/activate
./run_both.sh
```

Enjoy watching the LLM agent shop on Amazon! 🛒🤖
