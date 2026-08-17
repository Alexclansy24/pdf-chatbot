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
from graphs.nodes.history import (
    history_node,
)


builder = StateGraph(
    RAGState
)

builder.add_node(
    "Retrieve",
    retrieve_node,
)

builder.add_node(
    "Validate",
    validate_node,
)

builder.add_node(
    "Generate",
    generate_node,
)

builder.add_node(
    "Respond",
    response_node,
)

builder.add_node(
    "History",
    history_node,
)

builder.add_edge(
    START,
    "History",
)

builder.add_edge(
    "History",
    "Retrieve",
)

builder.add_edge(
    "Retrieve",
    "Validate",
)

builder.add_edge(
    "Validate",
    "Generate",
)

builder.add_edge(
    "Generate",
    "Respond",
)

builder.add_edge(
    "Respond",
    END,
)


rag_graph = (
    builder.compile()
)