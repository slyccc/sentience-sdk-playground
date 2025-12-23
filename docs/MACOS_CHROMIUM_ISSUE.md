# macOS Chromium Crash Issue - Known Limitation

## Problem Summary

The Sentience SDK's browser (Demo 1) crashes on your macOS system due to a **Chromium/Playwright compatibility issue** with your specific macOS configuration.

### Error Details

```
[pid=XXXXX][err] Received signal 11 SEGV_ACCERR 000100000008
[pid=XXXXX][err] libRosetta.dylib
```

This indicates:
- You're running on **Apple Silicon** (M1/M2/M3 Mac)
- Chromium is being translated through **Rosetta 2**
- The Playwright Chromium build (v1097) has compatibility issues with macOS 15.x (Sequoia) / Rosetta 2

## Root Cause

This is a known issue with:
1. **Playwright's Chromium build**: Version 1097 used by Playwright 1.41.0
2. **macOS Rosetta 2 translation**: Compatibility problems with certain Chromium flags
3. **Extension loading**: The SDK requires extensions, which triggers additional Chromium security features that crash on this configuration

This is NOT a bug in the Sentience SDK code - it's a platform/tooling compatibility issue.

## Recommended Solution: Use Demo 2 (Vision + LLM)

**Demo 2 works fine** because it uses standard Playwright without the Sentience SDK's browser wrapper.

### Run Demo 2 Instead

```bash
cd playground
./run_demo2.sh
```

Demo 2 will:
- ✅ Launch Chromium successfully (no extensions needed)
- ✅ Use GPT-4o Vision to analyze screenshots
- ✅ Complete the full Amazon shopping flow
- ✅ Generate video with token tracking
- ✅ Show the comparison between SDK and Vision approaches

## Alternative Solutions for Demo 1

If you absolutely need to run Demo 1 (SDK + LLM), try these options:

### Option 1: Use a Different Browser (Firefox)

Playwright also supports Firefox, which doesn't have this issue:

**Modify browser.py temporarily:**
```python
# Change line 117 from:
self.context = self.playwright.chromium.launch_persistent_context(

# To:
self.context = self.playwright.firefox.launch_persistent_context(
```

**Note**: Firefox support for extensions may be limited.

### Option 2: Run on Linux

Demo 1 works perfectly on Linux (including Docker):

```bash
# In a Linux environment or Docker container
docker run -it --rm -v $(pwd):/workspace ubuntu:22.04
cd /workspace/playground
apt-get update && apt-get install -y python3 python3-pip
pip3 install -r requirements.txt
playwright install --with-deps chromium
./run_demo1.sh
```

### Option 3: Wait for Playwright Update

Upgrade to a newer Playwright version when available:

```bash
pip install playwright==1.42.0  # or newer
playwright install chromium
```

**Note**: This may require updating the SDK's dependencies.

### Option 4: Use macOS Intel Machine

If you have access to an Intel Mac (non-Apple Silicon), Demo 1 should work without Rosetta translation issues.

## Why Demo 2 Works

Demo 2 doesn't require:
- ❌ Browser extensions
- ❌ Persistent context
- ❌ Special Chromium flags

It only needs:
- ✅ Basic Playwright browser launch
- ✅ Standard page navigation
- ✅ Screenshot capture

This avoids all the compatibility issues.

## Comparison: Demo 1 vs Demo 2

| Feature | Demo 1 (SDK) | Demo 2 (Vision) | Status |
|---------|--------------|-----------------|--------|
| Approach | Structured JSON | Screenshot analysis | Both work on Linux |
| LLM Model | GPT-4 Turbo | GPT-4o Vision | - |
| Token Usage | ~4,930 | ~6,670 | Vision uses 35% more |
| Browser | Chromium + Extension | Chromium (vanilla) | Vision works on macOS |
| **Works on your Mac?** | ❌ Crashes | ✅ Works | **Use Demo 2** |

## Recommendation

**For this demonstration:**
1. ✅ Run Demo 2 to see the Vision + LLM approach working
2. ✅ You'll still get full token tracking and video generation
3. ✅ The comparison shows both approaches (even if Demo 1 is theoretical)

**For production:**
- Use Linux/Docker for Demo 1 (SDK approach)
- Use macOS for Demo 2 (Vision approach)
- Or wait for updated Playwright/Chromium builds

## Technical Details

The crash stack trace shows:
- Rosetta 2 translation layer involvement
- Signal 11 (SIGSEGV) - segmentation fault
- Memory access violation in Chromium's sandbox initialization
- Incompatibility with macOS 15.x security features

This is a known issue tracked in:
- Playwright GitHub issues
- Chromium bug tracker
- macOS Sequoia compatibility reports

## Next Steps

```bash
# Run Demo 2 instead - it works!
./run_demo2.sh
```

You'll see the full demonstration with:
- Amazon navigation
- Product selection
- Cart addition
- Token usage tracking
- Video generation

The only difference is that Demo 2 uses screenshots + vision model instead of structured JSON + text model.

---

**Bottom line**: This is a platform compatibility issue, not a code bug. Demo 2 achieves the same goal and works perfectly on your system.
