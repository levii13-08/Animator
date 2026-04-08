# AI Educational Animation Pipeline

An AI-powered system that automatically generates educational animated videos from a simple concept prompt.

This project combines **LLMs, LangGraph workflows, Manim animations, and text-to-speech synthesis** to create short educational videos automatically.

Example input:

python main.py "Explain centrifugal force"

The system will generate:
- A structured educational script
- Animated visualization
- Voice narration
- A final merged educational video

---

# Project Architecture

The pipeline is built using **LangGraph**, which enables stateful workflows and parallel execution of AI tasks.

Pipeline Flow:

User Prompt
      │
      ▼
Script Generator (LLM)
      │
      ├───────────────┐
      ▼               ▼
Manim Animation     TTS Audio
      │               │
      └───────┬───────┘
              ▼
        Video + Audio Merge
              ▼
         Final Video

---

# Core Technologies

- **LangGraph** – Workflow orchestration
- **Google Gemini API** – Script and animation planning
- **Manim** – Mathematical animation engine
- **gTTS** – Text-to-speech narration
- **FFmpeg** – Video/audio merging
- **Python** – Pipeline implementation

---

# Project Components

## 1. Script Generator

Generates a structured educational script using an LLM.

Input:
Concept prompt

Output JSON:

{
  "narration_script": "...",
  "scene_descriptions": [...],
  "scene_duration_seconds": [...]
}

The script is shared with both animation and narration pipelines. :contentReference[oaicite:1]{index=1}

---

## 2. Animation Generator

Creates Manim animation automatically from the script.

Steps:
1. Generate animation plan using Gemini
2. Build base Manim scene code
3. Enhance visuals with LLM
4. Render animation using Manim

Output:
animation_video.mp4 :contentReference[oaicite:2]{index=2}

---

## 3. Text-to-Speech (TTS)

Generates narration audio from the script using Google TTS.

Output:
narration_audio.mp3 :contentReference[oaicite:3]{index=3}

---

## 4. Parallel Execution (LangGraph)

After script generation, two tasks run **in parallel**:

- Animation generation
- Narration generation

This reduces pipeline latency and demonstrates **agentic workflow execution**. :contentReference[oaicite:4]{index=4}

---

## 5. Video + Audio Merge

The final step merges animation and narration using FFmpeg.

Features:
- Synchronizes audio/video duration
- Loops video if necessary
- Pads audio when required

Output:
final_video.mp4 :contentReference[oaicite:5]{index=5}

---

# State Management

The pipeline uses a **shared state object** to pass information between nodes.

State structure:

concept_prompt  
structured_script  
animation_video  
narration_audio  
final_video  

This enables modular node execution and workflow orchestration. :contentReference[oaicite:6]{index=6}

---

# Running the Project

## 1. Install dependencies

pip install langgraph manim gtts google-generativeai numpy

Install FFmpeg separately.

---

## 2. Set API Key

export GEMINI_API_KEY=your_api_key

Windows:

set GEMINI_API_KEY=your_api_key

---

## 3. Run the pipeline

python main.py "Explain Fourier Series"

---

# Output

Generated files:

outputs/
 ├── narration_audio.mp3
 ├── animation_video.mp4
 └── final_video.mp4

---

# Example Use Cases

- AI generated educational videos
- Automated STEM explanations
- AI tutoring systems
- Social media educational content
- AI powered learning platforms

---

# Future Improvements

- Better animation planning using LLMs
- Multi-scene timeline control
- Improved synchronization
- Support for multiple languages
- 3D animations
- Voice cloning

---

# Key Learning Outcomes

This project demonstrates:

- LangGraph agentic workflows
- LLM-driven content generation
- Automated animation synthesis
- Parallel AI task execution
- Media pipeline orchestration
