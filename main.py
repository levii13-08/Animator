import os
import sys

from pipeline.graph import build_graph
from pipeline.state import PipelineState


def run_pipeline(concept_prompt: str) -> str:
    """
    Entry point that runs the LangGraph animation pipeline.
    Returns path to the final video.
    """

    os.makedirs("outputs", exist_ok=True)

    print("=" * 60)
    print("        AI EDUCATIONAL ANIMATION PIPELINE")
    print("=" * 60)
    print(f"Concept: {concept_prompt}")
    print("=" * 60)

    initial_state: PipelineState = {
        "concept_prompt": concept_prompt,
        "structured_script": None,
        "animation_video": None,
        "narration_audio": None,
        "final_video": None,
    }

    print("\n[Main] Building LangGraph workflow...")
    graph = build_graph()

    print("[Main] Running pipeline...\n")

    final_state = graph.invoke(initial_state)

    final_video = final_state.get("final_video")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print(f"Final video: {final_video}")
    print("=" * 60)

    return final_video or ""


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print('python main.py "Explain centrifugal force"')
        sys.exit(1)

    concept = sys.argv[1]

    output_path = run_pipeline(concept)

    print(f"\nDone! Watch your video at:\n{output_path}")