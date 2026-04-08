import json
import os
import subprocess

from pipeline.state import PipelineState

FINAL_VIDEO_PATH = "outputs/final_video.mp4"


def _probe_duration(path: str) -> float:
    """
    Get media duration using ffprobe.
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {path}: {result.stderr}")

    payload = json.loads(result.stdout)

    return float(payload["format"]["duration"])


def merge_node(state: PipelineState) -> PipelineState:
    """
    Node 4: Merge animation video + narration audio using FFmpeg.
    """

    os.makedirs("outputs", exist_ok=True)

    video_path = state.get("animation_video")
    audio_path = state.get("narration_audio")

    if not video_path:
        raise ValueError("animation_video missing from pipeline state.")

    if not audio_path:
        raise ValueError("narration_audio missing from pipeline state.")

    print("[Merge Node] Starting merge process...")

    video_duration = _probe_duration(video_path)
    audio_duration = _probe_duration(audio_path)

    print(f"[Merge Node] Video duration : {video_duration:.2f}s")
    print(f"[Merge Node] Audio duration : {audio_duration:.2f}s")

    target_duration = max(video_duration, audio_duration)

    print(f"[Merge Node] Target duration: {target_duration:.2f}s")

    cmd = [
        "ffmpeg",
        "-y",
        "-stream_loop",
        "-1",
        "-i",
        video_path,
        "-i",
        audio_path,
        "-filter_complex",
        "[1:a]apad[a]",
        "-map",
        "0:v:0",
        "-map",
        "[a]",
        "-t",
        f"{target_duration:.3f}",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        FINAL_VIDEO_PATH,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("[Merge Node] FFmpeg ERROR:", result.stderr)
        raise RuntimeError("FFmpeg merge failed.")

    print(f"[Merge Node] Final video saved to: {FINAL_VIDEO_PATH}")

    return {"final_video": FINAL_VIDEO_PATH}