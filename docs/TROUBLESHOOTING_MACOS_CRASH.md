# macOS Chromium Crash Fix

## Problem

Chromium crashes with `SEGV_ACCERR` error on macOS when using the Sentience SDK browser:

```
playwright._impl._errors.TargetClosedError: Target page, context or browser has been closed
[pid=XXXXX][err] Received signal 11 SEGV_ACCERR 000100000008
```

## Root Cause

The `--no-sandbox` flag causes Chromium to crash on macOS. This flag is hardcoded in the Sentience SDK's `browser.py` file.

## Solution

Edit the SDK source file to remove the `--no-sandbox` flag on macOS:

### Step 1: Open the browser.py file

```bash
# From the playground directory
nano ../sentience/browser.py
```

Or use any text editor:
```bash
code ../sentience/browser.py
```

### Step 2: Find and modify line 99

Find this section (around line 94-101):
```python
# Build launch arguments
args = [
    f"--disable-extensions-except={self._extension_path}",
    f"--load-extension={self._extension_path}",
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",  # <-- THIS LINE CAUSES THE CRASH
    "--disable-infobars",
]
```

### Step 3: Replace with platform-specific logic

Change it to:
```python
# Build launch arguments
args = [
    f"--disable-extensions-except={self._extension_path}",
    f"--load-extension={self._extension_path}",
    "--disable-blink-features=AutomationControlled",
    "--disable-infobars",
]

# Only add --no-sandbox on Linux (not macOS)
import platform
if platform.system() == 'Linux':
    args.append("--no-sandbox")
```

### Step 4: Save and test

Save the file and try running the demo again:
```bash
cd playground
./run_demo1.sh
```

## Alternative: Use Demo 2 (Vision + LLM) First

Demo 2 uses standard Playwright without the Sentience SDK and should work without modification:

```bash
./run_demo2.sh
```

This demo doesn't have the `--no-sandbox` issue because it doesn't use the SDK's browser wrapper.

## Why This Happens

- `--no-sandbox` is required on Linux environments (like Docker) where sandboxing isn't available
- On macOS, sandboxing works fine and the flag actually causes crashes
- The SDK currently hardcodes this flag for all platforms

## Permanent Fix

The Sentience SDK should be updated to conditionally add `--no-sandbox` only on Linux:

```python
import platform

args = [
    # ... other args ...
]

if platform.system() == 'Linux':
    args.append("--no-sandbox")
```

This would make the SDK work across all platforms without manual modifications.
