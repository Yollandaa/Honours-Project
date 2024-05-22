import ast
import networkx as nx
import matplotlib.pyplot as plt
from graph_from_ast import build_ast_graph, visualize_graph


def differential_analysis(graph1, graph2, code1, code2):
    normalized_original, original_lines = normalize_ast(graph1, code1)
    normalized_plagiarized, plagiarized_lines = normalize_ast(graph2, code2)

    print("-----------------Normalized Original----------------------")
    print(normalized_original)
    print(normalized_plagiarized)
    print(original_lines)
    print(plagiarized_lines)

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


def structural_analysis(graph1, graph2):
    if nx.is_isomorphic(graph1, graph2):
        print("The two codes are structurally similar.")
    else:
        print("The two codes are structurally dissimilar.")

    # Additional structural analysis can be implemented here
    print(graph1)
    print(graph2)


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
data_list = [2, 5, 7, 9, 11, 17, 222]
# Test cases
print(search_binary(data_list, 11))  # Expected output: 4
print(search_binary(data_list, 12))  # Expected output: -1

"""

print("\n Differential Analysis")
graph1 = build_ast_graph(python_code1)
graph2 = build_ast_graph(python_code2)
differential_analysis(graph1, graph2, python_code1, python_code2)

print("\n Structural Analysis")
structural_analysis(graph1, graph2)
