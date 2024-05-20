import ast
import networkx as nx
import matplotlib.pyplot as plt
import textwrap


class ASTGraphBuilder(ast.NodeVisitor):
    def __init__(self, source_code):
        self.graph = nx.DiGraph()
        self.node_counter = 0
        self.node_map = {}
        self.parent_stack = []
        self.source_code = source_code
        self.lines = source_code.splitlines()

    def visit_FunctionDef(self, node):
        self.add_node(node, f"Function: {node.name}")
        self.generic_visit(node)

    def visit_If(self, node):
        test = self.get_source_segment(node.test)
        self.add_node(node, f"If: {test}")
        self.visit(node.test)
        for stmt in node.body:
            self.visit(stmt)
        for stmt in node.orelse:
            self.visit(stmt)

    def visit_Return(self, node):
        value = self.get_source_segment(node.value)
        self.add_node(node, f"Return: {value}")
        self.generic_visit(node)

        # If the previous node was a print statement, connect it to this return statement
        if (
            self.parent_stack
            and isinstance(self.parent_stack[-1], ast.Call)
            and self.get_func_name(self.parent_stack[-1]) == "print"
        ):
            print_node_id = self.node_map[self.parent_stack[-1]]
            return_node_id = self.node_map[node]
            self.graph.add_edge(print_node_id, return_node_id)

    def visit_Call(self, node):
        func_name = self.get_func_name(node)
        args = self.get_call_args(node)
        call_description = f"Call: {func_name}({args})"

        # Check if it's a print() call
        if func_name == "print":
            self.add_node(node, call_description)
            if self.parent_stack:
                # Connect the "Print" node to the relevant parent node
                self.graph.add_edge(self.parent_stack[-1], node)
        else:
            self.add_node(node, call_description)
            # Check if the call is assigned to a variable
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in self.node_map.values()
            ):
                if self.parent_stack:
                    # Connect the call node to the assignment node
                    self.graph.add_edge(self.parent_stack[-1], node)

        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = ", ".join(self.get_source_segment(t) for t in node.targets)
        value = self.get_source_segment(node.value)
        self.add_node(node, f"Assign: {targets} = {value}")

        # Connect the assign node to its expression
        if isinstance(node.value, ast.Call):
            self.graph.add_edge(self.node_map[node], self.node_map[node.value])

        self.generic_visit(node)

    def get_source_segment(self, node):
        start_lineno = node.lineno - 1
        end_lineno = (
            node.end_lineno - 1 if hasattr(node, "end_lineno") else start_lineno
        )
        start_col_offset = node.col_offset
        end_col_offset = (
            node.end_col_offset if hasattr(node, "end_col_offset") else start_col_offset
        )
        lines = self.lines[start_lineno : end_lineno + 1]
        if len(lines) == 1:
            return lines[0][start_col_offset:end_col_offset]
        lines[0] = lines[0][start_col_offset:]
        lines[-1] = lines[-1][:end_col_offset]
        return " ".join(line.strip() for line in lines)

    def get_func_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return f"{self.get_source_segment(node.func.value)}.{node.func.attr}"
        # Recognize print as a special case
        elif node.func.id == "print":
            return "print"
        return "Unknown"

    def get_call_args(self, node):
        return ", ".join(self.get_source_segment(arg) for arg in node.args)

    def add_node(self, node, label):
        node_id = self.node_counter
        self.node_counter += 1
        self.node_map[node] = node_id
        self.graph.add_node(node_id, label=label)

        if self.parent_stack:
            parent_id = self.node_map[self.parent_stack[-1]]
            self.graph.add_edge(parent_id, node_id)

        self.parent_stack.append(node)
        self.generic_visit(node)
        self.parent_stack.pop()

    def visit(self, node):
        if node not in self.node_map:
            super().visit(node)


def build_ast_graph(source_code):
    tree = ast.parse(source_code)
    builder = ASTGraphBuilder(source_code)
    builder.visit(tree)
    return builder.graph


def visualize_graph(graph):
    pos = nx.spring_layout(graph)
    labels = nx.get_node_attributes(graph, "label")
    nx.draw(
        graph,
        pos,
        with_labels=True,
        labels=labels,
        node_size=3000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
        arrowsize=20,
    )
    plt.show()


if __name__ == "__main__":
    source_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

result = factorial(5)
print(result)
print(result)
"""
    graph = build_ast_graph(source_code)
    visualize_graph(graph)
