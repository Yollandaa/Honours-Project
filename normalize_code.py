import ast


class IdentifierNormalizer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.var_counter = 0
        self.func_counter = 0
        self.class_counter = 0
        self.var_mapping = {}
        self.func_mapping = {}
        self.class_mapping = {}

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            if node.id not in self.var_mapping:
                self.var_counter += 1
                self.var_mapping[node.id] = f"var{self.var_counter}"
            node.id = self.var_mapping.get(node.id, node.id)
        elif isinstance(node.ctx, ast.Load):
            node.id = self.var_mapping.get(node.id, node.id)
        return node

    def visit_FunctionDef(self, node):
        # Skip renaming for dunder functions
        if node.name.startswith("__") and node.name.endswith("__"):
            self.generic_visit(node)
            return node
        if node.name not in self.func_mapping:
            self.func_counter += 1
            self.func_mapping[node.name] = f"func{self.func_counter}"
        node.name = self.func_mapping.get(node.name, node.name)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        if node.name not in self.class_mapping:
            self.class_counter += 1
            self.class_mapping[node.name] = f"class{self.class_counter}"
        node.name = self.class_mapping.get(node.name, node.name)
        self.generic_visit(node)
        return node

    def visit_Call(self, node):
        # Handle renaming of functions and classes in calls
        if isinstance(node.func, ast.Name):
            if node.func.id in self.func_mapping:
                node.func.id = self.func_mapping[node.func.id]
            elif node.func.id in self.class_mapping:
                node.func.id = self.class_mapping[node.func.id]
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in self.func_mapping:
                node.func.attr = self.func_mapping[node.func.attr]
            elif node.func.attr in self.class_mapping:
                node.func.attr = self.class_mapping[node.func.attr]
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        # Handle renaming of attributes referencing classes or instances
        if node.attr in self.var_mapping:
            node.attr = self.var_mapping[node.attr]
        elif node.attr in self.func_mapping:
            node.attr = self.func_mapping[node.attr]
        elif node.attr in self.class_mapping:
            node.attr = self.class_mapping[node.attr]
        self.generic_visit(node)
        return node

    def visit_Import(self, node):
        # Preserve import statements
        return node

    def visit_ImportFrom(self, node):
        # Preserve import statements
        return node


def normalize_code(code):
    tree = ast.parse(code)
    normalizer = IdentifierNormalizer()
    normalized_tree = normalizer.visit(tree)
    normalized_code = ast.unparse(normalized_tree)

    return normalized_code
