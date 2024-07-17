import json
import sys
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

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


def save_runtime_data(filepath):
    with open(filepath, "w") as f:
        json.dump(runtime_data, f, indent=4)


def start_tracing():
    sys.settrace(trace_calls)


def stop_tracing(filepath):
    sys.settrace(None)
    save_runtime_data(filepath)


def load_runtime_data(filepath):
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


def generate_call_graph(source_code, output_file="call_graph.png"):

    graphviz = GraphvizOutput()
    graphviz.output_file = output_file

    with PyCallGraph(output=graphviz):
        exec(source_code)
