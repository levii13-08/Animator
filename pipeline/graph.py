from langgraph.graph import END, StateGraph

from pipeline.nodes.manim_node import manim_node
from pipeline.nodes.merge_node import merge_node
from pipeline.nodes.script_generator import script_generator_node
from pipeline.nodes.tts_node import tts_node
from pipeline.state import PipelineState


def build_graph():
    graph = StateGraph(PipelineState)

    # Register nodes
    graph.add_node("script_generator", script_generator_node)
    graph.add_node("manim_node", manim_node)
    graph.add_node("tts_node", tts_node)
    graph.add_node("merge", merge_node)

    # Entry point
    graph.set_entry_point("script_generator")

    # Parallel execution after script generation
    graph.add_edge("script_generator", "manim_node")
    graph.add_edge("script_generator", "tts_node")

    # Wait for both nodes before merging
    graph.add_edge(["manim_node", "tts_node"], "merge")

    # Final node
    graph.add_edge("merge", END)

    return graph.compile()