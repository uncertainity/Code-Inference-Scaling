from pathlib import Path
import tokenize
import ast
import json
from complexity_metrics.lcb_schema import (
    RemoveDocstrings,
    _clean_source,
    get_traces_lcb,
    remove_comments,
)
from complexity_metrics.dataset_schema import get_traces_apps


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_COLLECTION_DIR = PROJECT_ROOT / "data_collection"
REFERENCE_DIR = DATA_COLLECTION_DIR / "reference_solutions"



class RemoveMetadata(ast.NodeTransformer):
    REMOVE_NAMES = {"TASK_ID", "CASES"}

    def _remove_docstring(self, node):
        self.generic_visit(node)

        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        return node

    def visit_Module(self, node):
        node = self._remove_docstring(node)

        new_body = []
        for stmt in node.body:
            if (
                isinstance(stmt, ast.Assign)
                and len(stmt.targets) == 1
                and isinstance(stmt.targets[0], ast.Name)
                and stmt.targets[0].id in self.REMOVE_NAMES
            ):
                continue
            new_body.append(stmt)

        node.body = new_body
        return node

    def visit_ClassDef(self, node):
        return self._remove_docstring(node)

    def visit_FunctionDef(self, node):
        return self._remove_docstring(node)

    def visit_AsyncFunctionDef(self, node):
        return self._remove_docstring(node)
    
    
    
def return_clean_code(file_name, base_folder):
    code_path = Path(base_folder) / file_name
    code = code_path.read_text(encoding="utf-8")
    try:
        code = remove_comments(code)
    except (IndentationError, tokenize.TokenError, ValueError):
        pass
    code = _clean_source(code)
    tree = ast.parse(code)
    if not hasattr(ast, "unparse"):
        return code
    tree = RemoveDocstrings().visit(tree)
    tree = RemoveMetadata().visit(tree)
    ast.fix_missing_locations(tree)
    clean_code = ast.unparse(tree)
    
    return clean_code


def collect_generated_codes(codex_folder, task_prefix):
    gen_codes = {}
    for path in sorted(Path(codex_folder).glob("*.py")):
        clean_code = return_clean_code(path.name, codex_folder)
        task_id = f"{task_prefix}/{path.stem}"
        gen_codes[task_id] = clean_code
    return gen_codes


def attach_generated_code(row, clean_code):
    row["reference_solutions"] = [clean_code]
    if "reference_code" in row:
        row["reference_code"] = clean_code
    if "referrence_code" in row:
        row["referrence_code"] = clean_code
    return row


def normalize_codex_solutions(
    *,
    dataset,
    task_prefix,
    codex_folder,
    data_json,
    output_data,
    output_trace,
    trace_extractor,
):
    gen_codes = collect_generated_codes(codex_folder, task_prefix)

    with open(data_json, "r", encoding="utf-8") as fin, \
        open(output_data, "w", encoding="utf-8") as fdata, \
        open(output_trace, "w", encoding="utf-8") as ftrace:
        for line in fin:
            row = json.loads(line)
            task_id = row["task_id"]
            if task_id not in gen_codes:
                continue

            row = attach_generated_code(row, gen_codes[task_id])
            ast_metrics, radon_metrics = trace_extractor(row)
            fdata.write(json.dumps(row, ensure_ascii=False) + "\n")
            trace_json = {
                "task_id": row["task_id"],
                "dataset": dataset,
                "split": row.get("split", "test"),
                **ast_metrics,
                **radon_metrics,
            }
            ftrace.write(json.dumps(trace_json, ensure_ascii=False) + "\n")


def main():
    normalize_codex_solutions(
        dataset="lcb",
        task_prefix="lcb",
        codex_folder=REFERENCE_DIR / "codex" / "lcb_test",
        data_json=DATA_COLLECTION_DIR / "normalized" / "lcb_test.jsonl",
        output_data=REFERENCE_DIR / "codex" / "lcb_test_data.jsonl",
        output_trace=REFERENCE_DIR / "codex" / "lcb_test_traces.jsonl",
        trace_extractor=get_traces_lcb,
    )
    normalize_codex_solutions(
        dataset="apps",
        task_prefix="apps",
        codex_folder=REFERENCE_DIR / "codex" / "apps_test",
        data_json=DATA_COLLECTION_DIR / "normalized" / "apps_test.jsonl",
        output_data=REFERENCE_DIR / "codex" / "apps_test_data.jsonl",
        output_trace=REFERENCE_DIR / "codex" / "apps_test_traces.jsonl",
        trace_extractor=get_traces_apps,
    )


if __name__ == "__main__":
    main()
