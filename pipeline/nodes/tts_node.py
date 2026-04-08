import os

from gtts import gTTS

from pipeline.state import PipelineState

AUDIO_OUTPUT_PATH = "outputs/narration_audio.mp3"


def tts_node(state: PipelineState) -> PipelineState:
    """
    Node 3: Convert narration script to speech using gTTS.
    """

    os.makedirs("outputs", exist_ok=True)

    structured_script = state.get("structured_script")

    if not structured_script:
        raise ValueError("structured_script missing in pipeline state.")

    narration_text = structured_script.get("narration_script", "").strip()

    if not narration_text:
        raise ValueError("narration_script is empty.")

    print("[TTS Node] Generating narration audio...")

    try:
        tts = gTTS(
            text=narration_text,
            lang="en",
            slow=False
        )

        tts.save(AUDIO_OUTPUT_PATH)

    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {e}")

    print(f"[TTS Node] Audio saved to {AUDIO_OUTPUT_PATH}")

    return {"narration_audio": AUDIO_OUTPUT_PATH}