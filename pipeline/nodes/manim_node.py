import os
import json
import re
import shutil
import subprocess
import numpy as np
from google import genai

from pipeline.state import PipelineState

MANIM_SCRIPT_PATH = "outputs/generated_scene.py"
VIDEO_OUTPUT_PATH = "outputs/animation_video.mp4"


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No JSON found")


def probe_duration(path: str):

    cmd = [
        "ffprobe",
        "-v","error",
        "-show_entries","format=duration",
        "-of","json",
        path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    try:
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except:
        return 60


# -------------------------------
# Animation Planner (Flash Lite)
# -------------------------------

def generate_animation_plan(script):

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    narration = script["narration_script"]
    scenes = script["scene_descriptions"]

    prompt = f"""
Create animation scenes for an educational Manim video.

Narration:
{narration}

Scenes:
{scenes}

Return JSON:

{{
 "scenes":[
   {{"type":"diagram"}},
   {{"type":"movement"}},
   {{"type":"equation"}},
   {{"type":"graph"}}
 ]
}}

Allowed types:
text
graph
wave
vector
movement
rotation
equation
diagram
highlight
array
network
transform
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        return extract_json(response.text)
    except:
        print("[Manim Node] Invalid plan. Using fallback.")

        return {
            "scenes":[
                {"type":"text","content":s}
                for s in scenes
            ]
        }


# -------------------------------
# Primitive Renderer
# -------------------------------

def build_scene_code(plan, duration):

    blocks = []

    for i, scene in enumerate(plan["scenes"]):

        t = scene.get("type","text")
        content = scene.get("content","")

        if t == "wave":

            block = f"""
        axes_{i} = Axes(x_range=[0,10,1], y_range=[-2,2,1])

        wave1_{i} = axes_{i}.plot(lambda x: np.sin(x), color=BLUE)
        wave2_{i} = axes_{i}.plot(lambda x: np.sin(2*x)/2, color=GREEN)

        self.play(Create(axes_{i}))
        self.play(Create(wave1_{i}))
        self.play(Create(wave2_{i}))
        self.wait({duration})
        self.play(FadeOut(axes_{i}), FadeOut(wave1_{i}), FadeOut(wave2_{i}))
"""

        elif t == "movement":

            block = f"""
        obj_{i} = Circle(radius=0.5)

        self.play(FadeIn(obj_{i}))
        self.play(obj_{i}.animate.shift(RIGHT*3), run_time={duration})
        self.play(FadeOut(obj_{i}))
"""

        elif t == "equation":

            block = f"""
        eq_{i} = MathTex("f(x) = a_0 + \\sum a_n \\sin(nx)")
        self.play(Write(eq_{i}))
        self.wait({duration})
        self.play(FadeOut(eq_{i}))
"""

        else:

            safe = content.replace('"',"'")

            block = f"""
        text_{i} = Text("{safe}")
        text_{i}.scale(0.8)

        self.play(Write(text_{i}))
        self.wait({duration})
        self.play(FadeOut(text_{i}))
"""

        blocks.append(block)

    return "\n".join(blocks)


def build_base_code(plan, total_duration):

    scenes = plan["scenes"]

    duration = max(4, total_duration / max(1,len(scenes)))

    scene_code = build_scene_code(plan, duration)

    return f"""
from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920

class EducationalVideo(Scene):

    def construct(self):

{scene_code}
"""


# -------------------------------
# LLM Enhancement (Flash Lite)
# -------------------------------

def enhance_with_llm(base_code):

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = f"""
Improve this Manim animation visually.

Rules:
- Only use Manim Community Edition APIs
- Do NOT use GraphScene or get_graph
- Only enhance visuals

Code:
{base_code}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    improved = response.text or base_code

    banned = ["GraphScene","get_graph","ThreeDScene"]

    for bad in banned:
        if bad in improved:
            print("[Manim Node] Unsafe API detected. Using base code.")
            return base_code

    return improved


# -------------------------------
# Main Node
# -------------------------------

def manim_node(state: PipelineState):

    os.makedirs("outputs", exist_ok=True)

    script = state["structured_script"]
    audio = state.get("narration_audio")

    duration = 60

    if audio and os.path.exists(audio):
        duration = probe_duration(audio)

    print("[Manim Node] Creating animation plan...")

    plan = generate_animation_plan(script)

    print("[Manim Node] Building base animation...")

    base_code = build_base_code(plan, duration)

    print("[Manim Node] Enhancing animation...")

    final_code = enhance_with_llm(base_code)

    with open(MANIM_SCRIPT_PATH,"w") as f:
        f.write(final_code)

    print("[Manim Node] Rendering animation...")

    subprocess.run([
        "manim",
        MANIM_SCRIPT_PATH,
        "EducationalVideo",
        "-q","l",
        "--format=mp4",
        "--media_dir=outputs/manim_media"
    ])

    for root,_,files in os.walk("outputs/manim_media"):
        for file in files:
            if file.endswith(".mp4"):
                path = os.path.join(root,file)
                shutil.move(path, VIDEO_OUTPUT_PATH)
                return {"animation_video": VIDEO_OUTPUT_PATH}

    raise RuntimeError("Manim rendering failed")