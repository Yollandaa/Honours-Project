import ast
import networkx as nx
from graph import plot
from graph_from_ast import build_ast_graph, visualize_graph


def differential_analysis(graph1, graph2):

    # Normalize and compare ASTs
    normalized_original = normalize_ast(graph1)
    normalized_plagiarized = normalize_ast(graph2)

    # Calculate weighted similarity
    similarity_score = calculate_weighted_similarity(
        normalized_original, normalized_plagiarized
    )

    print("Similarity score: ", similarity_score)
    # Threshold comparison
    if similarity_score > PLAGIARISM_THRESHOLD:
        print("Potential plagiarism detected.")
    else:
        print("No plagiarism detected.")


def normalize_ast(graph):
    """
    Normalize the AST graph by stripping out variable names and other non-essential details
    to focus on the structure of the code.
    """
    normalized_graph = {}
    for node, edges in graph.items():
        normalized_node = normalize_node(node)
        normalized_edges = [normalize_node(edge) for edge in edges]
        normalized_graph[normalized_node] = normalized_edges
    return normalized_graph


def normalize_ast(graph):
    """
    Normalize the AST graph by stripping out variable names and other non-essential details
    to focus on the structure of the code.
    """
    normalized_graph = {}
    for node_id, data in graph.nodes(data=True):
        normalized_node = normalize_node(data["label"])
        normalized_edges = [
            normalize_node(graph.nodes[neighbor]["label"])
            for neighbor in graph.neighbors(node_id)
        ]
        normalized_graph[normalized_node] = normalized_edges
    return normalized_graph


def normalize_node(label):
    """
    Example normalization function that removes specific identifiers or variable names.
    """
    # Simplify labels for normalization by removing values, e.g., 'Assign: x = 1' -> 'Assign'
    return label.split(":")[0]


def calculate_weighted_similarity(graph1, graph2):
    """
    Calculate a weighted similarity score between two normalized AST graphs.
    """
    total_nodes = len(graph1) + len(graph2)
    matching_nodes = 0

    for node in graph1:
        if node in graph2 and set(graph1[node]) == set(graph2[node]):
            matching_nodes += 1

    similarity_score = (2 * matching_nodes / total_nodes) * 100
    return similarity_score


def calculate_similarity_score(self, other_graph):
    """
    Calculates the similarity score between this graph and another graph.
    """
    total_nodes = len(self.graph.nodes)
    matching_nodes = 0

    for node_id, node_data in self.graph.nodes(data=True):
        if node_id in other_graph.nodes:
            matching_nodes += 1
            # Assuming dynamic_info is a set of tuples (operation, value) for simplicity
            if node_data["dynamic_info"] == other_graph.nodes[node_id]["dynamic_info"]:
                matching_nodes -= 1  # Subtract one for exact matches

    return max((matching_nodes / total_nodes) * 100, 0)


def structural_analysis(graph1, graph2):
    """
    Compares birthmarks of two Python codes.
    """

    # Structural/Static comparison: Check if the graphs are isomorphic
    # Same number of nodes and edges and other features
    # (each vertex v has the exact same set of neighbors in both graphs.):
    # This could just be the base case. They are definetely plagiarised.
    if nx.is_isomorphic(graph1, graph2):
        print("The two codes are structurally similar.")
    else:
        print("The two codes are structurally dissimilar.")

    # TODO:
    # we need to check other features.
    # Techniques for plagiarising code:
    # 1. Code insertion - adding code without affecting the functionality of the program
    # 2. Control Replacement - Replacing loops with while loops, vice verse.
    # 3. Format alterations - adding/removing extra variables, spaces, comments, and tabs etc.
    # 4. Identifier renaming - Renaming variables, comments, functions etc.
    # 5. Statement reordering - Certain statements can be reordered without affecting the functionality of the program

    print(graph1)
    print(graph2)
    # visualize_graph(graph1)
    # visualize_graph(graph2)


PLAGIARISM_THRESHOLD = 70
# Example usage
python_code1 = """
def factorial(n):
    if n == 0:
        return 1
    else:
        #print(n)
        n = n + 1
        return n * factorial(n-1)

result = factorial(5)
print(result)
"""

python_code2 = """
def calc_factorial(n):
    if n == 0:
        return 1
    else:
        #print(n)
        return n * calc_factorial(n-1)

output = calc_factorial(5)
print(output)
"""

print("\n Differential Analysis")
graph1 = build_ast_graph(python_code1)
graph2 = build_ast_graph(python_code2)
differential_analysis(graph1, graph2)
print("\n Structural Analysis")
structural_analysis(graph1, graph2)
