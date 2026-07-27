from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from graphs.states.rag_state import (
    RAGState,
)

from graphs.nodes.retrieve import (
    retrieve_node,
)

from graphs.nodes.validate import (
    validate_node,
)

from graphs.nodes.generate import (
    generate_node,
)

from graphs.nodes.respond import (
    response_node,
)


builder = StateGraph(
    RAGState
)

builder.add_node(
    "retrieve",
    retrieve_node,
)

builder.add_node(
    "validate",
    validate_node,
)

builder.add_node(
    "generate",
    generate_node,
)

builder.add_node(
    "respond",
    response_node,
)

builder.add_edge(
    START,
    "retrieve",
)

builder.add_edge(
    "retrieve",
    "validate",
)

builder.add_edge(
    "validate",
    "generate",
)

builder.add_edge(
    "generate",
    "respond",
)

builder.add_edge(
    "respond",
    END,
)

rag_graph = (
    builder.compile()
)