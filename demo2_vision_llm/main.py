"""
Demo 2: GPT-4o Vision + Playwright for Amazon Shopping

This demo uses GPT-4o Vision to analyze screenshots directly,
then uses Playwright to perform actions based on the vision model's decisions.
"""
import os
import sys
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from vision_agent import VisionAgent
from token_tracker import TokenTracker
# Use simplified video generator (no ImageMagick/TextClip needed)
from video_generator_simple import create_demo_video


def main():
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if not openai_api_key:
        print("ERROR: OPENAI_API_KEY not found in .env file")
        return

    # Initialize tracker and agent
    tracker = TokenTracker("Demo 2: Vision + LLM")
    agent = VisionAgent(api_key=openai_api_key, tracker=tracker)

    # Screenshot directory
    screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)

    print("\n" + "="*70)
    print("DEMO 2: GPT-4o Vision + Playwright - Amazon Shopping")
    print("="*70)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        # =================================================================
        # SCENE 1: Navigate to Amazon & Find Search Bar
        # =================================================================
        print("\n[Scene 1] Navigating to Amazon.com...")
        page.goto("https://www.amazon.com")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)  # Wait for page to fully load

        # Take screenshot
        screenshot_path = os.path.join(screenshots_dir, "vision_scene1_homepage.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"Screenshot saved: {screenshot_path}")

        # Ask Vision LLM to find search bar
        prompt = """You are an AI agent controlling a web browser to shop on Amazon.

Current Task: Find the search bar on the Amazon homepage.

Instructions:
1. Analyze the provided screenshot
2. Locate the search input field (usually near the top of the page)
3. Identify the center coordinates (x, y) of the search bar
4. Provide precise pixel coordinates based on a 1920x1080 viewport

Response Format (JSON only):
{
  "reasoning": "brief explanation of how you identified the search bar",
  "element_description": "description of the visual element",
  "coordinates": {"x": <center_x>, "y": <center_y>},
  "confidence": "high/medium/low"
}"""

        result = agent.analyze_screenshot(screenshot_path, prompt, "Scene 1: Find Search Bar")

        # Click on search bar with validation
        coords = result.get('coordinates', {})
        x = coords.get('x')
        y = coords.get('y')

        if x is None or y is None:
            print(f"\n❌ ERROR: Vision LLM could not find search bar. Response: {result}")
            raise Exception("Could not find search bar coordinates")

        print(f"\nClicking on search bar at coordinates: ({x}, {y})")
        page.mouse.click(x, y)
        time.sleep(1)

        # =================================================================
        # SCENE 2: Type Search Query
        # =================================================================
        print("\n[Scene 2] Typing search query: 'Christmas gift'")
        page.keyboard.type("Christmas gift", delay=100)
        time.sleep(0.5)

        # Take screenshot
        screenshot_path = os.path.join(screenshots_dir, "vision_scene2_typing.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"Screenshot saved: {screenshot_path}")

        # Press Enter
        print("Pressing Enter...")
        page.keyboard.press("Enter")
        time.sleep(4)  # Wait for search results

        # =================================================================
        # SCENE 3: Select Product from Search Results
        # =================================================================
        print("\n[Scene 3] Analyzing search results...")

        # Take screenshot
        screenshot_path = os.path.join(screenshots_dir, "vision_scene3_search_results.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"Screenshot saved: {screenshot_path}")

        # Ask Vision LLM to select a product
        prompt = """You are an AI agent controlling a web browser to shop on Amazon.

Current Task: Select a product from the search results for "Christmas gift".

Instructions:
1. Analyze the provided screenshot showing Amazon search results
2. Identify product listings in the main content area
3. Select the FIRST clearly visible product (top-left priority)
4. Locate the product image or title that is clickable
5. Provide the center coordinates (x, y) to click on the product
6. Avoid ads (labeled "Sponsored") if possible, but select first available product

Response Format (JSON only):
{
  "reasoning": "explanation of product selection logic",
  "product_description": "brief description of selected product",
  "coordinates": {"x": <center_x>, "y": <center_y>},
  "confidence": "high/medium/low",
  "is_sponsored": true/false
}"""

        result = agent.analyze_screenshot(screenshot_path, prompt, "Scene 3: Select Product")

        # Click on product with validation
        coords = result.get('coordinates', {})
        x = coords.get('x')
        y = coords.get('y')

        if x is None or y is None:
            print(f"\n❌ ERROR: Vision LLM could not find product. Response: {result}")
            raise Exception("Could not find product coordinates")

        print(f"\nClicking on product: {result.get('product_description', 'Unknown')}")
        print(f"Coordinates: ({x}, {y})")
        page.mouse.click(x, y)
        # Wait for navigation (Amazon pages have continuous network activity, so use simple wait)
        print("Waiting for product page to load...")
        time.sleep(5)  # Simple wait - Amazon loads dynamically

        # =================================================================
        # SCENE 4: Find and Click "Add to Cart" Button
        # =================================================================
        print("\n[Scene 4] Finding 'Add to Cart' button...")

        # Increase viewport height for this scene to enable panning effect in video
        print("Increasing viewport height for better camera panning...")
        page.set_viewport_size({"width": 1920, "height": 1600})
        time.sleep(1)  # Wait for viewport to adjust

        # Take screenshot with taller viewport
        screenshot_path = os.path.join(screenshots_dir, "vision_scene4_product_details.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"Screenshot saved: {screenshot_path} (1920x1600 for panning effect)")

        # Ask Vision LLM to find Add to Cart button
        prompt = """You are an AI agent controlling a web browser to shop on Amazon.

Current Task: Find and click the "Add to Cart" button on the product details page.

Instructions:
1. Analyze the provided screenshot of the Amazon product page
2. Locate the "Add to Cart" button (typically orange/yellow button on right side)
3. Distinguish it from "Buy Now" button if both are present
4. Provide the center coordinates (x, y) of the "Add to Cart" button
5. Ensure the button is fully visible and clickable

Response Format (JSON only):
{
  "reasoning": "explanation of how you identified the Add to Cart button",
  "button_description": "visual description of the button (color, text, position)",
  "coordinates": {"x": <center_x>, "y": <center_y>},
  "confidence": "high/medium/low",
  "other_buttons_nearby": ["Buy Now", "Add to List"]
}"""

        result = agent.analyze_screenshot(screenshot_path, prompt, "Scene 4: Add to Cart")

        # Click Add to Cart with validation
        coords = result.get('coordinates', {})
        x = coords.get('x')
        y = coords.get('y')

        if x is None or y is None:
            print(f"\n❌ ERROR: Vision LLM could not find Add to Cart button")
            print(f"Response: {result}")
            print("Attempting to find button using selector fallback...")
            # Fallback: try to find button by selector
            try:
                add_to_cart_btn = page.locator("#add-to-cart-button").first
                add_to_cart_btn.click()
                print("✅ Clicked using selector fallback")
            except Exception as e:
                print(f"Fallback also failed: {e}")
                raise Exception("Could not click Add to Cart button")
        else:
            print(f"\nClicking 'Add to Cart' button")
            print(f"Coordinates: ({x}, {y})")
            page.mouse.click(x, y)

        time.sleep(3)

        # =================================================================
        # SCENE 5: Verify Success
        # =================================================================
        print("\n[Scene 5] Verifying cart addition...")

        # Take screenshot
        screenshot_path = os.path.join(screenshots_dir, "vision_scene5_confirmation.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"Screenshot saved: {screenshot_path}")

        # Ask Vision LLM to verify
        prompt = """You are an AI agent controlling a web browser to shop on Amazon.

Current Task: Verify that the item was successfully added to the cart.

Instructions:
1. Analyze the provided screenshot
2. Look for visual confirmation indicators:
   - Success overlay/modal with "Added to Cart" message
   - Cart icon in header with updated count
   - Green checkmark or success indicator
3. Determine if the action was successful

Response Format (JSON only):
{
  "success": true/false,
  "reasoning": "explanation of what visual cues indicate success or failure",
  "confirmation_elements": ["list of visual confirmations found"],
  "cart_count": "number shown in cart icon if visible or empty string"
}"""

        result = agent.analyze_screenshot(screenshot_path, prompt, "Scene 5: Verify Success")

        if result.get('success'):
            print(f"\n✅ SUCCESS: {result.get('reasoning')}")
            print(f"Confirmations: {', '.join(result.get('confirmation_elements', []))}")
        else:
            print(f"\n❌ FAILED: {result.get('reasoning')}")

        time.sleep(2)

        browser.close()

    # Print token usage summary
    tracker.print_summary()
    tracker.save_to_file(os.path.join(screenshots_dir, "token_summary.json"))

    # Generate video
    print("\n" + "="*70)
    print("Generating video with token overlay...")
    print("="*70)
    video_output = os.path.join(os.path.dirname(__file__), "video", "demo2_vision_final.mp4")
    os.makedirs(os.path.dirname(video_output), exist_ok=True)

    try:
        create_demo_video(screenshots_dir, tracker.get_summary(), video_output)
    except Exception as e:
        print(f"Warning: Video generation failed: {e}")
        print("Screenshots and data are still available in the screenshots directory")

    print("\n" + "="*70)
    print("DEMO 2 COMPLETE!")
    print("="*70)


if __name__ == "__main__":
    main()
