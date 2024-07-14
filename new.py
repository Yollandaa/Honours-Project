import difflib
from zss import simple_distance, Node
from static_analysis import *
from dynamic_analysis import *


# Checking Structural Similarities using Static Analysis Graph
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


def calculate_tree_edit_distance(graph1, graph2):
    def build_zss_tree(graph, root):
        node = Node(graph.nodes[root]["label"])
        for child in graph.successors(root):
            node.addkid(build_zss_tree(graph, child))
        return node

    root1 = [n for n, d in graph1.in_degree() if d == 0][0]
    root2 = [n for n, d in graph2.in_degree() if d == 0][0]

    zss_tree1 = build_zss_tree(graph1, root1)
    zss_tree2 = build_zss_tree(graph2, root2)

    return simple_distance(zss_tree1, zss_tree2)


def calculate_token_similarity(code1, code2):
    tokens1 = code1.split()
    tokens2 = code2.split()
    return difflib.SequenceMatcher(None, tokens1, tokens2).ratio() * 100


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

# Build AST graphs
graph1 = build_ast_graph(python_code1)
graph2 = build_ast_graph(python_code2)

# Vizualize the AST graph
visualize_graph(graph1)
visualize_graph(graph2)

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

# Generate call graphs (placeholder functionality)
generate_call_graph(python_code1, "call_graph1.png")
generate_call_graph(python_code2, "call_graph2.png")

# Calculate tree edit distance between ASTs
tree_edit_distance = calculate_tree_edit_distance(graph1, graph2)
print(f"Tree Edit Distance: {tree_edit_distance}")

# Calculate token similarity between code snippets
token_similarity = calculate_token_similarity(python_code1, python_code2)
print(f"Token Similarity: {token_similarity:.2f}%")

# Trace and compare execution traces
start_tracing()
exec(python_code1)
stop_tracing("runtime_data1.json")
trace1 = analyze_runtime_data(load_runtime_data("runtime_data1.json"))

start_tracing()
exec(python_code2)
stop_tracing("runtime_data2.json")
trace2 = analyze_runtime_data(load_runtime_data("runtime_data2.json"))

execution_trace_similarity = calculate_execution_trace_similarity(trace1, trace2)
print(f"Execution Trace Similarity: {execution_trace_similarity:.2f}%")

# Combine static and dynamic similarities
combined_similarity = calculate_combined_similarity(
    token_similarity, execution_trace_similarity
)
print(f"Combined Similarity: {combined_similarity:.2f}%")

# Determine potential plagiarism
if combined_similarity > PLAGIARISM_THRESHOLD:
    print("Potential plagiarism detected.")
else:
    print("No plagiarism detected.")
