import ast


class FindVarsClassFunctionsMixin:

    @staticmethod
    def get_all_names_vars_in_tree(tree):
        return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]

    @staticmethod
    def get_all_names_classes_in_tree(tree):
        return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    @staticmethod
    def get_all_names_functions_in_tree(tree):
        return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

    @staticmethod
    def get_all_names_in_tree(tree):
        names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                names.append(node.id)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                names.append(node.name.lower())
        return names
