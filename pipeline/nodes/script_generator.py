import json
import os
import re
from google import genai

from pipeline.state import PipelineState


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No JSON found")


def script_generator_node(state: PipelineState) -> PipelineState:

    concept_prompt = (state.get("concept_prompt") or "").strip()

    if not concept_prompt:
        raise ValueError("concept_prompt cannot be empty.")

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert educational video script writer.

Topic: "{concept_prompt}"

Create a script for a 60-second educational animation.

Return ONLY JSON:

{{
  "narration_script": "140-160 word explanation",
  "scene_descriptions": [
    "Scene 1 visual explanation",
    "Scene 2 visual explanation",
    "Scene 3 visual explanation",
    "Scene 4 visual explanation"
  ],
  "scene_duration_seconds": [15,15,15,15]
}}
"""

    print("[Script Generator] Generating structured script...")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text

    try:
        structured_script = extract_json(text)
    except Exception:

        print("[Script Generator] Invalid JSON from LLM. Using fallback script.")

        structured_script = {
            "narration_script": concept_prompt,
            "scene_descriptions": [
                "Introduction to the concept",
                "Explanation of the core idea",
                "Example visualization",
                "Summary of the concept"
            ],
            "scene_duration_seconds": [15, 15, 15, 15]
        }

    narration = structured_script.get("narration_script", "")
    scenes = structured_script.get("scene_descriptions", [])

    print("[Script Generator] Script generated successfully.")
    print(f"Narration preview: {narration[:80]}...")
    print(f"Scenes generated: {len(scenes)}")

    return {"structured_script": structured_script}