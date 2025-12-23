# Quick Start Guide

## Prerequisites

✅ All dependencies installed
✅ API keys configured in `.env`
✅ Playwright browsers installed
✅ Sentience SDK installed

## Running the Demos

**IMPORTANT**: Always activate the virtual environment first:
```bash
source venv/bin/activate
```

Or use the provided shell scripts:

### Option 1: Run Both Demos with Comparison (Recommended)

```bash
# With shell script (recommended)
./run_both.sh

# Or manually
source venv/bin/activate
python run_both_demos.py
```

This will:
1. Run Demo 1 (SDK + LLM) - Press Enter when prompted
2. Run Demo 2 (Vision + LLM) - Press Enter when prompted
3. Generate side-by-side comparison video automatically

**Output**: `comparison_video.mp4` in playground directory

---

### Option 2: Run Individual Demos

#### Demo 1: SDK + LLM

```bash
# With shell script
./run_demo1.sh

# Or manually
source venv/bin/activate
python demo1_sdk_llm/main.py
```

**What happens**:
- Opens Chrome browser (visible)
- Navigates to Amazon.com
- Uses SDK `snapshot()` to analyze page structure
- LLM analyzes JSON data to find search bar
- Types "Christmas gift" and searches
- LLM selects a product from search results
- LLM finds "Add to Cart" button
- Verifies item was added to cart
- Saves screenshots and token usage data
- Generates video with token overlay

**Output Directory**: `demo1_sdk_llm/screenshots/` and `demo1_sdk_llm/video/`

---

#### Demo 2: Vision + LLM

```bash
# With shell script
./run_demo2.sh

# Or manually
source venv/bin/activate
python demo2_vision_llm/main.py
```

**What happens**:
- Opens Chrome browser (visible)
- Navigates to Amazon.com
- Takes screenshot and sends to GPT-4o Vision
- Vision LLM analyzes image to find search bar
- Types "Christmas gift" and searches
- Vision LLM selects a product from screenshot
- Vision LLM finds "Add to Cart" button
- Verifies item was added to cart
- Saves screenshots and token usage data
- Generates video with token overlay

**Output Directory**: `demo2_vision_llm/screenshots/` and `demo2_vision_llm/video/`

---

## Expected Flow

### All Demos Follow This Pattern:

1. **Scene 1**: Homepage → Find search bar
2. **Scene 2**: Type "Christmas gift" (no LLM call)
3. **Scene 3**: Search results → Select product
4. **Scene 4**: Product page → Click "Add to Cart"
5. **Scene 5**: Verify cart confirmation

### Token Usage Display

During each demo, you'll see:
```
======================================================================
Scene: Scene 1: Find Search Bar
======================================================================
Analyzing snapshot: ...

LLM Decision:
{
  "reasoning": "Found searchbox role element at top of page",
  "element_id": 42,
  "bbox": {"x": 450, "y": 120, "width": 600, "height": 40},
  "action": "click"
}

  Token usage: 820 (prompt: 700, completion: 120)
```

### Final Summary

At the end of each demo:
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

### Browser Opens But Gets Blocked by Amazon

**Problem**: Amazon shows CAPTCHA or blocks automation

**Solutions**:
- Increase delays between actions (edit `time.sleep()` values in main.py)
- Try different times of day
- Use a VPN or different IP address
- Consider using real browser cookies

### LLM Can't Find Elements

**Problem**: LLM returns incorrect coordinates or can't find buttons

**Solutions**:
- Check screenshots in `screenshots/` directory to see what LLM sees
- Review LLM reasoning in console output
- Adjust prompts in main.py to be more specific
- Increase wait times after page loads

### Video Generation Fails

**Problem**: "Video generation failed" error

**Solutions**:
- Install ImageMagick: `brew install imagemagick` (macOS)
- Check that screenshots were saved successfully
- Run without video generation (comment out `create_demo_video()` calls)

### Token Limit Exceeded

**Problem**: OpenAI API returns token limit error

**Solutions**:
- Reduce snapshot data size (filter elements in Demo 1)
- Use lower resolution screenshots (Demo 2)
- Switch to a model with higher token limits

---

## Output Files

### Demo 1 (SDK + LLM)
```
demo1_sdk_llm/
├── screenshots/
│   ├── sdk_scene1_homepage.png          # Amazon homepage
│   ├── sdk_scene1_data.json             # Snapshot JSON data
│   ├── sdk_scene2_typing.png            # Search query typed
│   ├── sdk_scene3_search_results.png    # Search results
│   ├── sdk_scene3_data.json             # Search results snapshot
│   ├── sdk_scene4_product_details.png   # Product page
│   ├── sdk_scene4_data.json             # Product page snapshot
│   ├── sdk_scene5_confirmation.png      # Cart confirmation
│   ├── sdk_scene5_data.json             # Confirmation snapshot
│   └── token_summary.json               # Token usage summary
└── video/
    └── demo1_sdk_final.mp4              # Final video with overlay
```

### Demo 2 (Vision + LLM)
```
demo2_vision_llm/
├── screenshots/
│   ├── vision_scene1_homepage.png       # Amazon homepage
│   ├── vision_scene2_typing.png         # Search query typed
│   ├── vision_scene3_search_results.png # Search results
│   ├── vision_scene4_product_details.png # Product page
│   ├── vision_scene5_confirmation.png   # Cart confirmation
│   └── token_summary.json               # Token usage summary
└── video/
    └── demo2_vision_final.mp4           # Final video with overlay
```

### Comparison Video
```
playground/
└── comparison_video.mp4                 # Side-by-side comparison
```

---

## Next Steps

After running the demos:

1. **Review Token Usage**: Compare token summaries between both approaches
2. **Watch Videos**: See side-by-side comparison of execution
3. **Analyze Screenshots**: Review visual data in screenshots directories
4. **Examine Snapshot Data**: (Demo 1 only) Inspect JSON structure
5. **Cost Analysis**: Calculate costs based on OpenAI pricing

### Cost Calculation

**OpenAI Pricing** (as of Dec 2024):
- GPT-4 Turbo: $10/1M input tokens, $30/1M output tokens
- GPT-4o Vision: $2.50/1M input tokens, $10/1M output tokens

**Example**:
```
Demo 1: (4400 × $10 + 530 × $30) / 1M = $0.06
Demo 2: (5900 × $2.50 + 770 × $10) / 1M = $0.02
```

---

## Customization

### Modify Search Query

Edit in `main.py`:
```python
browser.page.keyboard.type("YOUR SEARCH QUERY HERE", delay=100)
```

### Change LLM Model

Edit in agent initialization:
```python
# Demo 1
agent = LLMAgent(api_key=openai_api_key, tracker=tracker, model="gpt-4")

# Demo 2
agent = VisionAgent(api_key=openai_api_key, tracker=tracker, model="gpt-4o")
```

### Adjust Wait Times

Find and modify `time.sleep()` calls:
```python
time.sleep(3)  # Increase for slower connections
```

### Customize Prompts

Edit prompt strings in `main.py` to change LLM behavior

---

## Support

For issues or questions:
1. Check [README.md](README.md) for detailed documentation
2. Review [LLM_AGENT_AMAZON_SHOPPING_DEMO_PLAN.md](../docs/LLM_AGENT_AMAZON_SHOPPING_DEMO_PLAN.md)
3. Examine console output for error messages
4. Check screenshots to debug visual issues

---

**Ready to run!** Execute `python run_both_demos.py` to get started.
