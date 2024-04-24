# Creating a dynamic birthmark for python codes

# So I like the idea of representing each program as a graph.
# The basic idea is to treat variables as nodes (vertices), and the control flow of the variables as edges
# After converting the two programs into graphs, then I can compare if there is some kind of similarity in them
# I am sure there are many methods that compare two graphs (e.g., isormophism)
# https://docs.python.org/3/library/ast.html
# Use this https://github.com/coetaur0/staticfg -> convert a piece of code to control flow 

import ast
import networkx as nx

class DynamicBirthmarkGenerator:
    def __init__(self, code):
        self.graph = None
        self.generate_dynamic_birthmark(code)

    def generate_ast_from_code(self, code):
        """
        Receive Python code and return the abstract syntax tree (AST).
        """
        return ast.parse(code)

    def generate_graph_from_ast(self, ast_tree):
        """
        Generate a graph representation from the abstract syntax tree (AST) of Python code.
        """
        G = nx.DiGraph() # Directed graph

        def traverse(node, parent_id): # Adding nodes and edges to the graph
            node_id = id(node)
            G.add_node(node_id, type=type(node).__name__)
            if parent_id is not None:
                G.add_edge(parent_id, node_id)
            for child in ast.iter_child_nodes(node):
                traverse(child, node_id)

        traverse(ast_tree, None)
        return G

    def generate_dynamic_birthmark(self, code):
        """
        Generate a dynamic birthmark for Python code.
        """
        ast_tree = self.generate_ast_from_code(code)
        self.graph = self.generate_graph_from_ast(ast_tree)

        # Add dynamic information here (e.g., variable values, function calls, etc.)
        # I could: add functionality to track variable values or function calls during execution and then incorporate this information into the graph representation.
        # Not sure how helpful this could be

    def get_graph(self):
        """
        Get the generated graph.
        """
        return self.graph

def compare_birthmarks(code1, code2):
    """
    Compare birthmarks of two Python codes.
    """
    if not isinstance(code1, DynamicBirthmarkGenerator) or not isinstance(code2, DynamicBirthmarkGenerator):
        print("Error: Both inputs should be instances of DynamicBirthmarkGenerator.")
        return

    birthmark1 = code1.get_graph()
    birthmark2 = code2.get_graph()

    #TODO: In here, I can create my own comparison function to compare the birthmarks of the 2 codes

    # An existing isomorphic implementation of nx
    if nx.is_isomorphic(birthmark1, birthmark2):
        print("The two code are isomorphic.")
    else:
        print("The two codes are not isomorphic.")

# I can instead read in 2 separate files
python_code1 = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

result = factorial(5)
print(result)
"""

python_code2 = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

result = factorial(5)
print(result)
"""
code1 = DynamicBirthmarkGenerator(python_code1)
code2 = DynamicBirthmarkGenerator(python_code2)
compare_birthmarks(code1, code2)
