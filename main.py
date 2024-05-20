import ast
import networkx as nx
from graph import plot
from graph_from_ast import build_ast_graph, visualize_graph


class DynamicBirthmarkGenerator:
    def __init__(self, code):
        self.graph = None
        self.generate_dynamic_birthmark(code)

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
                if (
                    node_data["dynamic_info"]
                    == other_graph.nodes[node_id]["dynamic_info"]
                ):
                    matching_nodes -= 1  # Subtract one for exact matches

        return max((matching_nodes / total_nodes) * 100, 0)

    def get_graph(self):
        """
        Gets the generated graph.
        """
        return self.graph


def compare_birthmarks(code1, code2):
    """
    Compares birthmarks of two Python codes.
    """

    birthmark1 = build_ast_graph(code1)
    birthmark2 = build_ast_graph(code2)

    # Structural/Static comparison: Check if the graphs are isomorphic
    # Same number of nodes and edges and other features
    # (each vertex v has the exact same set of neighbors in both graphs.):
    # This could just be the base case.
    if nx.is_isomorphic(birthmark1, birthmark2):
        print("The two codes are structurally similar.")
    else:
        print("The two codes are structurally dissimilar.")

    # Compare the number of nodes and edges
    if (
        birthmark1.number_of_nodes() == birthmark2.number_of_nodes()
        and birthmark1.number_of_edges() == birthmark2.number_of_edges()
    ):
        # Check if nodes and their dynamic information match
        match_count = sum(
            1
            for n1, n2 in zip(birthmark1.nodes(data=True), birthmark2.nodes(data=True))
            if n1[1].get("dynamic_info") == n2[1].get("dynamic_info")
        )
        similarity_percentage = (match_count / birthmark1.number_of_nodes()) * 100
        print(f"The two codes are {similarity_percentage}% similar.")
    else:
        print("The two codes are structurally dissimilar.")

    print(birthmark1)
    print(birthmark2)
    visualize_graph(birthmark1)
    visualize_graph(birthmark2)


# Example usage
python_code1 = """
def factorial(n):
    if n == 0:
        return 1
    else:
        print(n)
        return n * factorial(n-1)

result = factorial(5)
print(result)
"""

python_code2 = """
def calc_factorial(n):
    if n == 0:
        return 1
    else:
        return n * calc_factorial(n-1)

output = calc_factorial(5)
print(output)
"""

compare_birthmarks(python_code1, python_code2)
