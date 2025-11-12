# simplest_langgraph_two_nodes.py
from typing import TypedDict
from langgraph.graph import StateGraph, END

class State(TypedDict):
    text: str


# Functions which exists inside the nodes
def first(state: State):
    # Append to the incoming string
    return {"text": state["text"] + " -> first"}

def second(state: State):
    # Append again
    return {"text": state["text"] + " -> second"}

# Build the graph
builder = StateGraph(State)
builder.add_node("first", first)
builder.add_node("second", second)
builder.set_entry_point("first")
builder.add_edge("first", "second")
builder.add_edge("second", END)

graph = builder.compile()

# Run it
final_state = graph.invoke({"text": "start"})
print(final_state)         # {'text': 'start -> first -> second'}
