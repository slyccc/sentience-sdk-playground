# LLM Agent Amazon Shopping Demos

This directory contains two demonstrations comparing different approaches to LLM-powered web automation for Amazon shopping.

## Overview

Both demos complete the same Amazon shopping flow:
1. Navigate to Amazon.com
2. Find and click the search bar
3. Type "Christmas gift" and search
4. Select a product from search results
5. Click "Add to Cart" button
6. Verify item was added to cart

## Demo 1: Sentience SDK + LLM

**Approach**: Uses Sentience SDK's `snapshot()` function to get structured JSON data with semantic information, then uses GPT-4 to analyze and make decisions.

**Advantages**:
- More efficient token usage (structured JSON vs. image encoding)
- Precise element identification with IDs
- Semantic metadata (importance scores, visual cues)
- Lower latency (no image encoding/transmission)

**Directory**: `demo1_sdk_llm/`

## Demo 2: GPT-4o Vision + Playwright

**Approach**: Uses GPT-4o Vision to analyze raw screenshots and identify elements visually, then uses Playwright for browser control.

**Advantages**:
- No dependency on SDK or browser extension
- Works with any web page (no instrumentation needed)
- Can handle visual-only interfaces
- More human-like perception

**Directory**: `demo2_vision_llm/`

## Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
cd playground
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configure API Keys

Create a `.env` file in the `playground/` directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
SENTIENCE_API_KEY=your_sentience_api_key_here  # Optional for Demo 1
```

### 3. Install Sentience SDK (for Demo 1)

```bash
# From the sdk-python root directory
pip install -e .
```

## Running the Demos

### Run Demo 1 Only

```bash
cd demo1_sdk_llm
python main.py
```

### Run Demo 2 Only

```bash
cd demo2_vision_llm
python main.py
```

### Run Both Demos + Generate Comparison

```bash
cd playground
python run_both_demos.py
```

This will:
1. Run Demo 1 and generate video with token overlay
2. Run Demo 2 and generate video with token overlay
3. Create a side-by-side comparison video

## Output

Each demo produces:
- **Screenshots**: Saved in `screenshots/` directory
- **Snapshot Data** (Demo 1 only): JSON files with structured page data
- **Token Summary**: JSON file with detailed token usage
- **Video**: MP4 file with scene transitions and token overlay

### Demo 1 Outputs
```
demo1_sdk_llm/
├── screenshots/
│   ├── sdk_scene1_homepage.png
│   ├── sdk_scene2_typing.png
│   ├── sdk_scene3_search_results.png
│   ├── sdk_scene4_product_details.png
│   ├── sdk_scene5_confirmation.png
│   ├── sdk_scene*_data.json (snapshot data)
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

### Comparison Output
```
playground/
└── comparison_video.mp4  # Side-by-side comparison
```

## Expected Token Usage

Based on the demo plan, estimated token usage:

| Demo | Total Tokens | Cost (approx) |
|------|--------------|---------------|
| Demo 1 (SDK + LLM) | ~4,930 | $0.06 |
| Demo 2 (Vision + LLM) | ~6,670 | $0.08 |

**Note**: Vision approach uses ~35% more tokens due to image encoding overhead.

## Troubleshooting

### Amazon CAPTCHA or Bot Detection

If Amazon shows a CAPTCHA:
- Try running in non-headless mode (already default)
- Add longer delays between actions
- Use a real user session cookie
- Consider using residential proxies

### Element Not Found

- Check screenshots to see what the page actually shows
- Verify coordinates are within viewport (1920x1080)
- Ensure page fully loaded before taking snapshot/screenshot
- Review LLM reasoning in console output

### Video Generation Failed

- Check that MoviePy is installed correctly
- Ensure ImageMagick is installed (required for TextClip)
- On macOS: `brew install imagemagick`
- On Linux: `sudo apt-get install imagemagick`
- On Windows: Download from imagemagick.org

### Token Limits Exceeded

- Reduce snapshot data size by filtering elements
- Compress images before sending to Vision API
- Use lower resolution screenshots

## Development

### Project Structure

```
playground/
├── shared/                    # Shared utilities
│   ├── token_tracker.py      # Token usage tracking
│   └── video_generator.py    # MoviePy video generation
├── demo1_sdk_llm/            # SDK + LLM demo
│   ├── main.py               # Demo script
│   ├── llm_agent.py          # LLM wrapper
│   └── screenshots/          # Output directory
├── demo2_vision_llm/         # Vision + LLM demo
│   ├── main.py               # Demo script
│   ├── vision_agent.py       # Vision LLM wrapper
│   └── screenshots/          # Output directory
├── requirements.txt          # Python dependencies
├── .env                      # API keys (create this)
├── run_both_demos.py         # Master script
└── README.md                 # This file
```

### Customization

To modify the shopping flow:
1. Edit the main.py scripts in each demo directory
2. Update prompts to match your desired behavior
3. Adjust timeouts and delays as needed
4. Modify video generation settings in video_generator.py

## References

- [Sentience SDK Documentation](../README.md)
- [Demo Plan Document](../docs/LLM_AGENT_AMAZON_SHOPPING_DEMO_PLAN.md)
- [OpenAI GPT-4 Vision API](https://platform.openai.com/docs/guides/vision)
- [Playwright Documentation](https://playwright.dev/python/)
- [MoviePy Documentation](https://zulko.github.io/moviepy/)

## License

See parent directory LICENSE file.
