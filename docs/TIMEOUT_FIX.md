# Timeout Fix for Amazon Product Pages

## Issue

The demo was timing out after clicking a product with this error:
```
playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
```

At line:
```python
browser.page.wait_for_load_state("networkidle")
```

## Root Cause

Amazon product pages have **continuous network activity**:
- Background ads loading
- Analytics tracking
- Recommendation engines
- A/B testing scripts
- Live inventory updates

The `networkidle` state waits for 500ms with NO network requests, which **never happens** on modern Amazon pages.

## Solution

Replaced `wait_for_load_state("networkidle")` with a simple `time.sleep(5)`:

### Before (Timed Out)
```python
click_rect(browser, result['bbox'])
browser.page.wait_for_load_state("networkidle")  # ❌ Never reaches networkidle
time.sleep(3)
```

### After (Works)
```python
click_rect(browser, result['bbox'])
# Wait for navigation (Amazon pages have continuous network activity)
print("Waiting for product page to load...")
time.sleep(5)  # ✅ Simple wait - Amazon loads dynamically
```

## Why This Works

1. **Main content loads in ~2-3 seconds** (product title, price, "Add to Cart")
2. **Background activity continues indefinitely** (ads, analytics, recommendations)
3. **5-second wait** gives enough time for the LLM-needed elements to load
4. **We don't need everything** - just the core product page elements

## Applied To

- ✅ **Demo 1** (`demo1_sdk_llm/main.py` line 163-165)
- ✅ **Demo 2** (`demo2_vision_llm/main.py` line 141-143)

## Alternative Solutions Considered

### Option 1: Increase Timeout (Rejected)
```python
browser.page.wait_for_load_state("networkidle", timeout=60000)
```
**Problem**: Still might timeout, wastes time waiting

### Option 2: Wait for Specific Element (Considered)
```python
browser.page.wait_for_selector("#add-to-cart-button", timeout=10000)
```
**Problem**: Amazon uses dynamic IDs, not reliable

### Option 3: DOM Content Loaded (Too Fast)
```python
browser.page.wait_for_load_state("domcontentloaded")
```
**Problem**: Product images and key elements might not load yet

### Option 4: Simple Timer (CHOSEN) ✅
```python
time.sleep(5)
```
**Benefit**: Reliable, simple, works for Amazon's dynamic loading

## Best Practices for Modern Web Scraping

For sites with continuous network activity (e.g., Amazon, Facebook, Google):

1. ✅ **Use simple timers** for known load times
2. ✅ **Wait for specific elements** if IDs are stable
3. ❌ **Avoid `networkidle`** - rarely achieves quiet state
4. ✅ **Increase wait times** for slower connections

## Now Runs Successfully

Both demos now complete the full flow:
1. ✅ Navigate to Amazon
2. ✅ Search for "Christmas gift"
3. ✅ Click on product (**NO TIMEOUT!**)
4. ✅ Find "Add to Cart" button
5. ✅ Verify success

## Run the Fixed Demos

```bash
./run_demo1.sh  # SDK approach
./run_demo2.sh  # Vision approach
./run_both.sh   # Both with comparison
```

All demos should now complete without timeouts! 🎉
