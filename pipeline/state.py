from typing import Any, Optional, TypedDict, List


class StructuredScript(TypedDict):
    narration_script: str
    scene_descriptions: List[str]
    scene_duration_seconds: List[int]


class PipelineState(TypedDict):
    concept_prompt: str

    # LLM output shared between nodes
    structured_script: Optional[StructuredScript]

    # Outputs from parallel nodes
    animation_video: Optional[str]
    narration_audio: Optional[str]

    # Final output
    final_video: Optional[str]