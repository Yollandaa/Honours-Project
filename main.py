import ast
import networkx as nx
import matplotlib.pyplot as plt
from graph_from_ast import build_ast_graph, visualize_graph
from dynamic import (
    start_tracing,
    stop_tracing,
    load_runtime_data,
    analyze_runtime_data,
)


def normalize_ast(graph, code):
    normalized_graph = {}
    line_map = {}

    for node_id, data in graph.nodes(data=True):
        normalized_node = normalize_node(data.get("label", ""))
        normalized_edges = [
            normalize_node(graph.nodes[neighbor].get("label", ""))
            for neighbor in graph.neighbors(node_id)
        ]
        normalized_graph[normalized_node] = normalized_edges
        line_map[normalized_node] = get_code_line(data.get("label", ""), code)

    return normalized_graph, line_map


def normalize_node(label):
    label_parts = label.split(":")
    simplified_label = label_parts[0] if label_parts else label

    return simplified_label


def get_code_line(label, code):
    try:
        line_number = int(label.split(":")[1].strip().split()[1])
        code_line = code.splitlines()[line_number - 1].strip()
        return code_line
    except (IndexError, ValueError):
        return label


def calculate_weighted_similarity_and_report_lines(graph1, graph2):
    total_nodes = len(graph1) + len(graph2)
    matching_nodes = 0
    similar_lines = []

    all_nodes1 = set(graph1.keys())
    all_nodes2 = set(graph2.keys())

    common_nodes = all_nodes1.intersection(all_nodes2)

    for node in common_nodes:
        if set(graph1[node]) == set(graph2[node]):
            matching_nodes += 1
            similar_lines.append((node, node))

    similarity_score = (2 * matching_nodes / total_nodes) * 100

    return similarity_score, similar_lines


def combine_birthmarks(static_birthmarks, dynamic_birthmarks):
    return {"static": static_birthmarks, "dynamic": dynamic_birthmarks}


def calculate_combined_similarity(birthmarks1, birthmarks2):
    static_similarity, _ = calculate_weighted_similarity_and_report_lines(
        birthmarks1["static"], birthmarks2["static"]
    )

    dynamic_similarity = 0
    total_dynamic_sequences = len(birthmarks1["dynamic"]) + len(birthmarks2["dynamic"])
    matching_sequences = sum(
        1 for seq in birthmarks1["dynamic"] if seq in birthmarks2["dynamic"]
    )

    if total_dynamic_sequences > 0:
        dynamic_similarity = (2 * matching_sequences / total_dynamic_sequences) * 100
    print("\n Dynamic Similarity Score: ", dynamic_similarity)

    return (static_similarity + dynamic_similarity) / 2


def structural_analysis(
    original_lines,
    normalized_original,
    graph1,
    plagiarized_lines,
    normalized_plagiarized,
    graph2,
):
    if nx.is_isomorphic(graph1, graph2):
        print("The two codes are structurally similar.")
    else:
        print("The two codes are structurally dissimilar.")

    # Calculation of structural similarity
    similarity_score, similar_lines = calculate_weighted_similarity_and_report_lines(
        normalized_original, normalized_plagiarized
    )

    print("Similarity score: ", similarity_score)
    if similarity_score > PLAGIARISM_THRESHOLD:
        print("Potential plagiarism detected.")
        print("\n Similar lines:")
        for line1, line2 in similar_lines:
            print(
                f"Code 1: {original_lines[line1]}\nCode 2: {plagiarized_lines[line2]}\n"
            )
    else:
        print("No plagiarism detected.")

    print("-----------------Normalized Original----------------------")
    print(normalized_original)
    print(normalized_plagiarized)
    print(original_lines)
    print(plagiarized_lines)


def dynamic_analysis(execution_path_1, execution_path_2):
    """Analysing the execution paths of the two programs"""
    """ Doesn't work: was trying something"""
    deviation_score = 0

    # Compare execution paths
    for step in execution_path_1:
        if step not in execution_path_2:
            deviation_score += 1

    # Normalize score and apply threshold
    deviation_score_normalized = deviation_score / max(
        len(execution_path_1), len(execution_path_2)
    )
    if deviation_score_normalized > PLAGIARISM_THRESHOLD:
        print("Significant deviation detected.")


PLAGIARISM_THRESHOLD = 70

python_code1 = """
import math


def bin_search(li, element):
    bottom = 0
    top = len(li) - 1
    index = -1
    while top >= bottom and index == -1:
        mid = int(math.floor((top + bottom) / 2.0))
        if li[mid] == element:
            index = mid
        elif li[mid] > element:
            top = mid - 1
        else:
            bottom = mid + 1
    return index


li = [2, 5, 7, 9, 11, 17, 222]
print(bin_search(li, 11))
print(bin_search(li, 12))


"""

python_code2 = """
import math


def search_binary(collection, target_value):
    lower_bound = 0
    upper_bound = len(collection) - 1
    position = -1

    while upper_bound >= lower_bound and position == -1:
        middle = int(math.floor((upper_bound + lower_bound) / 2.0))

        # Debug statement to trace computation
        print(
            f"Searching at position {middle} with bounds ({lower_bound}, {upper_bound})"
        )

        if collection[middle] == target_value:
            position = middle
        elif collection[middle] > target_value:
            upper_bound = middle - 1
        else:
            lower_bound = middle + 1

    return position


# Sample data for demonstration
data_list = [22, 25, 27, 29, 31, 217, 223]
# Test cases
print(search_binary(data_list, 29))  # Expected output: 4
print(search_binary(data_list, 2))  # Expected output: -1

"""

print("\n Building AST Analysis")
graph1 = build_ast_graph(python_code1)
graph2 = build_ast_graph(python_code2)

visualize_graph(graph1)

print("\n Structural Analysis")
static_birthmarks1, static_lines1 = normalize_ast(
    build_ast_graph(python_code1), python_code1
)
static_birthmarks2, static_lines2 = normalize_ast(
    build_ast_graph(python_code2), python_code2
)
structural_analysis(
    static_lines1, static_birthmarks1, graph1, static_lines2, static_birthmarks2, graph2
)


print("-----------------------------------------------------------------------")
print("\n Dynamic Analysis")
# Execute and trace the first code
start_tracing()
exec(python_code1)
stop_tracing("runtime_data1.json")

# Execute and trace the second code
start_tracing()
exec(python_code2)
stop_tracing("runtime_data2.json")

# Load and analyze dynamic data
runtime_data1 = load_runtime_data("runtime_data1.json")
runtime_data2 = load_runtime_data("runtime_data2.json")

dynamic_birthmarks1 = analyze_runtime_data(runtime_data1)
dynamic_birthmarks2 = analyze_runtime_data(runtime_data2)

# Calculate dynamic similarity


# Combine static and dynamic birthmarks
combined_birthmarks1 = combine_birthmarks(static_birthmarks1, dynamic_birthmarks1)
combined_birthmarks2 = combine_birthmarks(static_birthmarks2, dynamic_birthmarks2)

# Calculate and print combined similarity score
similarity_score = calculate_combined_similarity(
    combined_birthmarks1, combined_birthmarks2
)
print("\n Combined Similarity Score:", similarity_score)
