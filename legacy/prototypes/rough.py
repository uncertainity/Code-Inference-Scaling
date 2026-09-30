import pandas as pd
import os 
from pathlib import Path
from io import StringIO
import tokenize
import ast
import json

df = pd.read_csv("platform_info.csv")
df_lc = df[df["platform"] == "leetcode"]
ref_lc_path = "reference_solutions/leetcode"
df_lc_all = df_lc["question_id"].astype(int).tolist()


# for name in os.listdir(ref_lc_path):
#     stem = Path(name).stem
#     if stem not in df_lc_all:
#         print(stem)

## copying the reference solution in a string

class RemoveDocstrings(ast.NodeTransformer):
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
        return self._remove_docstring(node)

    def visit_ClassDef(self, node):
        return self._remove_docstring(node)

    def visit_FunctionDef(self, node):
        return self._remove_docstring(node)

    def visit_AsyncFunctionDef(self, node):
        return self._remove_docstring(node)


def remove_comments(source):
    result = []

    tokens = tokenize.generate_tokens(StringIO(source).readline)

    for token in tokens:
        token_type = token.type
        token_string = token.string

        if token_type == tokenize.COMMENT:
            continue

        result.append(token)

    return tokenize.untokenize(result)

def get_clean_code(file_name,base_folder):
    code = open(f"{base_folder}/{file_name}","r",encoding = "utf-8").read()
    code = remove_comments(code)
    tree = ast.parse(code)
    tree = RemoveDocstrings().visit(tree)
    ast.fix_missing_locations(tree)
    clean_code = ast.unparse(tree)
    return clean_code

leetcode_solutions = "scraped_solutions/leetcode"
atcode_solutions = "scraped_solutions/atcoder"
count = 0
for file_name in os.listdir(atcode_solutions):
    clean_code = get_clean_code(file_name,atcode_solutions)
    #print(clean_code)
    count += 1
    if count == 20:
        break


# apps_json = "traces/apps_test.jsonl"
# with open(apps_json,"r") as f:
#     for line in f:
        
##check which dont' have trace -> check if they dont have ref solutions -> store the schema

apps_json = "traces/apps_test.jsonl"
missing_apps_ids = set()
with open(apps_json,"r") as f:
    for line in f:
        row = json.loads(line)
        if "AST_Length" not in row.keys():
            missing_apps_ids.add(row["task_id"])

# print(missing_apps_ids)
print(len(missing_apps_ids))

lcb_json = "traces/lcb_test.jsonl"
missing_lcb_ids = set()
with open(lcb_json,"r") as f:
    for line in f:
        row = json.loads(line)
        if "AST_Length" not in row.keys():
            missing_lcb_ids.add(row["task_id"])

print(len(missing_lcb_ids))

data_apps = "data_json/apps_test.jsonl"
missing_data_apps = []
with open(data_apps,"r") as f:
    for line in f:
        row = json.loads(line)
        task_id = row["task_id"]
        #print(row.keys())
        #print(row["reference_solutions"])
        #if task_id in missing_apps_ids and (row["reference_solutions"] is None or row["reference_solutions"] == ""):
        
        if task_id in missing_apps_ids:
            missing_data_apps.append(row)

print(len(missing_data_apps))
            
data_lcb = "data_json/lcb_test.jsonl"
missing_data_lcb = []
with open(data_lcb,"r") as f:
    for line in f:
        row = json.loads(line)
        task_id = row["task_id"]
        #print(row.keys())
        #print(row["reference_solutions"])
        #if task_id in missing_lcb_ids and (row["reference_solutions"] is None or row["reference_solutions"] == ""):
        
        if task_id in missing_lcb_ids:
            missing_data_lcb.append(row)

print(len(missing_data_lcb))


            
