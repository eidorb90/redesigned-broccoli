import ast
from pathlib import Path

from Finding import Finding

SKIP_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
}


class ProjectAnalyzer:
    god_function_lim = None
    findings = None
    project_base = None

    def __init__(self, project_base, god_function_lim=50):
        self.god_function_lim = god_function_lim
        self.findings = []
        self.project_base = project_base

    def find_python_files(self, root):
        root = Path(root)
        py_files = []

        for path in root.rglob("*.py"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            py_files.append(path)

        return py_files

    def analyze_project(self):
        py_files = self.find_python_files(self.project_base)
        for f in py_files:
            findings = self.analyze_file(f)
            self.findings += findings

        return findings

    def analyze_file(self, path):
        findings = []
        source = path.read_text(encoding="utf-8", errors="ignore")

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return [Finding("syntax_error", str(path), 1, "File has syntax errors")]

        for node in ast.walk(tree):

            # God functions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start = node.lineno
                end = getattr(node, "end_lineno", start)
                if end - start > self.god_function_lim:
                    findings.append(
                        Finding(
                            rule_id="god_function",
                            file=str(path),
                            line=start,
                            message=f"Function '{node.name}' is {end-start} lines long",
                            confidence=1,
                        )
                    )

            # Bare except
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                findings.append(
                    Finding(
                        rule_id="bare_except",
                        file=str(path),
                        line=node.lineno,
                        message="Bare except: catches everything and hides bugs",
                        confidence=1,
                    )
                )

        return findings
