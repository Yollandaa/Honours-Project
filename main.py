import difflib
from zss import simple_distance, Node
from static_analysis import *
from dynamic_analysis import *

# from token_similarity import calculate_token_similarity
from normalize_code import normalize_code  # Import normalize_code


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


def structural_analysis(
    original_lines,
    normalized_original,
    graph1,
    plagiarized_lines,
    normalized_plagiarized,
    graph2,
):
    # Base Case
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

    # print("-----------------Normalized Original----------------------")
    # print(normalized_original)
    # print(normalized_plagiarized)
    # print(original_lines)
    # print(plagiarized_lines)


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


## End of Structural Analysis for Static graph representation


def calculate_token_similarity(norm_code1, norm_code2):
    tokens1 = norm_code1.split()
    tokens2 = norm_code2.split()
    print(tokens1)
    print(tokens2)

    similarity_ratio = difflib.SequenceMatcher(None, tokens1, tokens2).ratio()
    return similarity_ratio * 100


def calculate_execution_trace_similarity(trace1, trace2):
    sm = difflib.SequenceMatcher(None, trace1, trace2)
    return sm.ratio() * 100


def calculate_combined_similarity(
    static_similarity, dynamic_similarity, weights=(0.5, 0.5)
):
    return static_similarity * weights[0] + dynamic_similarity * weights[1]


PLAGIARISM_THRESHOLD = 60

# Example Python code snippets for comparison
python_code1 = """
def calculate_vowel_frequency():
    text = "johndoe123"
    vowels = ["a", "e", "i", "o", "u"]
    vowel_count = 0

    for character in text:
        if character.lower() in vowels:
            vowel_count += 1

    print(f"Vowel Count: {vowel_count}")

if __name__ == "__main__":
    calculate_vowel_frequency()
"""

python_code2 = """
def count_vowels():
    st = "ammaradil"
    vowle = ["a", "e", "i", "o", "u"]
    count = 0

    for s in st:
        if s in vowle:
            count = count + 1

    print("Count", count)


if __name__ == "__main__":
    count_vowels()

"""
# Normalize the code
normalized_code1 = normalize_code(python_code1)
normalized_code2 = normalize_code(python_code2)


# Build AST graphs
graph1 = build_ast_graph(python_code1)
graph2 = build_ast_graph(python_code2)

# Vizualize the AST graph
# visualize_graph(graph1)
# visualize_graph(graph2)

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

print(
    "--------------------------------- Token Similarity: Static Side ----------------------------------"
)
# Calculate token similarity
token_similarity = calculate_token_similarity(normalized_code1, normalized_code2)
print(f"Token Similarity: {token_similarity:.2f}%")


print(
    "------------------------------------ Tracing Analysis --------------------------------"
)
# Trace and compare execution traces
start_tracing()
# exec(normalized_code1)
exec(python_code1)
stop_tracing("runtime_data1.json")
trace1 = analyze_runtime_data(load_runtime_data("runtime_data1.json"))

# Seems like the trace keeps data of the first source code
#  So erase the trace
# Better option is to modify the stop_tracing

start_tracing()
# exec(normalized_code2)
exec(python_code2)
stop_tracing("runtime_data2.json")
trace2 = analyze_runtime_data(load_runtime_data("runtime_data2.json"))

print(trace1)
print()
print(trace2)

execution_trace_similarity = calculate_execution_trace_similarity(trace1, trace2)
print(f"Execution Trace Similarity: {execution_trace_similarity:.2f}%")

print(
    "--------------------------------- Call graphs Similarity: Dynamic Side ----------------------------------"
)
# Generate call graphs (placeholder functionality)
generate_call_graph(python_code1, "call_graph1.png")
generate_call_graph(python_code2, "call_graph2.png")


# Combine static and dynamic similarities
# combined_similarity = calculate_combined_similarity(
#     token_similarity, execution_trace_similarity
# )
# print(f"Combined Similarity: {combined_similarity:.2f}%")

# Determine potential plagiarism
# if combined_similarity > PLAGIARISM_THRESHOLD:
#     print("Potential plagiarism detected.")
# else:
#     print("No plagiarism detected.")
