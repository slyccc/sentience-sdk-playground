"""
Vision LLM Agent wrapper for screenshot analysis with GPT-4o
"""
import json
import os
import base64
from openai import OpenAI
from typing import Dict, Any
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from token_tracker import TokenTracker


class VisionAgent:
    """Vision LLM agent for analyzing screenshots and making decisions"""

    def __init__(self, api_key: str, tracker: TokenTracker, model: str = "gpt-4o"):
        self.client = OpenAI(api_key=api_key)
        self.tracker = tracker
        self.model = model

    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_screenshot(self, image_path: str, task_prompt: str, scene_name: str) -> Dict[str, Any]:
        """
        Analyze screenshot and return decision

        Args:
            image_path: Path to screenshot image
            task_prompt: Task-specific prompt
            scene_name: Scene identifier for tracking

        Returns:
            Parsed JSON response from LLM
        """
        print(f"\n{'='*70}")
        print(f"Scene: {scene_name}")
        print(f"{'='*70}")
        print(f"Analyzing screenshot: {image_path}")

        # Encode image
        base64_image = self.encode_image(image_path)

        # Build full prompt
        full_prompt = f"""{task_prompt}

IMPORTANT: Respond ONLY with valid JSON. No markdown, no explanation outside the JSON.
The viewport size is 1920x1080. Provide coordinates relative to this viewport."""

        # Call OpenAI Vision API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI agent that analyzes web page screenshots and returns structured JSON responses with precise coordinates."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": full_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )

        # Track token usage
        usage = response.usage
        self.tracker.log_interaction(
            scene=scene_name,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens
        )

        # Parse response
        result = json.loads(response.choices[0].message.content)
        print(f"\nVision LLM Decision:")
        print(json.dumps(result, indent=2))

        return result
