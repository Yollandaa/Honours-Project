import ast


class IdentifierNormalizer(ast.NodeTransformer):
    def __init__(self):
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
            node.id = self.var_mapping[node.id]
        elif isinstance(node.ctx, ast.Load):
            if node.id in self.var_mapping:
                node.id = self.var_mapping[node.id]
        return node

    def visit_FunctionDef(self, node):
        if node.name not in self.func_mapping:
            self.func_counter += 1
            self.func_mapping[node.name] = f"func{self.func_counter}"
        node.name = self.func_mapping[node.name]
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        if node.name not in self.class_mapping:
            self.class_counter += 1
            self.class_mapping[node.name] = f"class{self.class_counter}"
        node.name = self.class_mapping[node.name]
        self.generic_visit(node)
        return node


def normalize_code(code):
    tree = ast.parse(code)
    normalizer = IdentifierNormalizer()
    normalized_tree = normalizer.visit(tree)
    normalized_code = ast.unparse(normalized_tree)
    return normalized_code
