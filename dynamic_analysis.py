import os
import sys
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from networkx.algorithms import isomorphism
import networkx as nx
import json

# Tracing functions
runtime_data = []


def trace_calls(frame, event, arg):
    if event == "call":
        func_name = frame.f_code.co_name
        func_line_no = frame.f_lineno
        func_filename = frame.f_code.co_filename
        runtime_data.append(
            {
                "event": "call",
                "func_name": func_name,
                "line_no": func_line_no,
                "filename": func_filename,
            }
        )
    elif event == "return":
        func_name = frame.f_code.co_name
        runtime_data.append({"event": "return", "func_name": func_name})
    return trace_calls


def save_runtime_data(filename):
    filepath = os.path.join("./Results", filename)
    with open(filepath, "w") as f:
        json.dump(runtime_data, f, indent=4)


def start_tracing():
    sys.settrace(trace_calls)


def stop_tracing(filepath):
    global runtime_data
    sys.settrace(None)
    save_runtime_data(filepath)
    runtime_data = (
        []
    )  # Reset the trace data: This was causing the second trace to have data of the first one


def load_runtime_data(filename):
    filepath = os.path.join("./Results", filename)
    with open(filepath, "r") as f:
        return json.load(f)


def analyze_runtime_data(runtime_data):
    call_sequences = []
    current_sequence = []

    for event in runtime_data:
        if event["event"] == "call":
            current_sequence.append(event["func_name"])
        elif event["event"] == "return":
            # Convert the list to a tuple before appending
            call_sequences.append(tuple(current_sequence))
            current_sequence = []

    return call_sequences


def tokenize_trace(trace_data):
    tokens = []
    for event in trace_data:
        tokens.append(event["event"])
        if "func_name" in event:
            tokens.append(event["func_name"])
    return " ".join(tokens)


def generate_call_graph(source_code, filename="call_graph.png"):
    output_file = os.path.join("./Results", filename)
    graphviz = GraphvizOutput()
    graphviz.output_file = output_file

    with PyCallGraph(output=graphviz):
        exec(source_code, globals())


def sequences_to_graph(call_sequences):
    G = nx.DiGraph()
    for seq in call_sequences:
        for i in range(len(seq) - 1):
            G.add_edge(seq[i], seq[i + 1])
    return G


def compare_call_graphs(call_sequences_1, call_sequences_2):
    # Convert call sequences to graphs
    G1 = sequences_to_graph(call_sequences_1)
    G2 = sequences_to_graph(call_sequences_2)

    # Create a GraphMatcher object to compare the graphs
    GM = isomorphism.GraphMatcher(G1, G2)

    return GM.is_isomorphic()
