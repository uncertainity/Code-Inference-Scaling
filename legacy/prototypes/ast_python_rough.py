import ast

source = """
def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    a.sort(reverse=True)

    if sum(a) < m:
        print(-1)
        return

    def can(d):
        total = 0
        for i, x in enumerate(a):
            total += max(0, x - i // d)
            if total >= m:
                return True
        return False

    left, right = 1, n

    while left < right:
        mid = (left + right) // 2

        if can(mid):
            right = mid
        else:
            left = mid + 1

    print(left)

solve()
"""



tree = ast.parse(source)
print(type(tree))
print("Length of tree body:",len(tree.body))
# print("Printing tree body")
# for i in range(len(tree.body)):
#     print(f"Body[{i}]:",tree.body[i])
#     print(tree.body[i]._fields)
#     print("==============================")

  
    
# def walk(node,depth = 0):
#     print("  " * depth + type(node).__name__)
#     for field in node._fields:
#         value = getattr(node,field)
#         if isinstance(value,ast.AST):
#             walk(value,depth + 1)
#         elif isinstance(value,list):
#             for item in value:
#                 if isinstance(item,ast.AST):
#                     walk(item,depth + 1)
                    
type_dict = {}
    
def walk(node, depth=0):
    indent = "  " * depth
    
    if isinstance(node, ast.FunctionDef):
        print(f"{indent}FunctionDef name={node.name}")
        
    elif isinstance(node, ast.Name):
        print(f"{indent}Name id={node.id} ctx={type(node.ctx).__name__}")

    elif isinstance(node, ast.arg):
        print(f"{indent}arg name={node.arg}")

    elif isinstance(node, ast.Constant):
        print(f"{indent}Constant value={node.value}")

    elif isinstance(node, ast.Attribute):
        print(f"{indent}Attribute attr={node.attr}")

    elif isinstance(node, ast.Call):
        print(f"{indent}Call")
    else:
        print(f"{indent}{type(node).__name__}")
        type_dict[type(node).__name__] = type_dict.get(type(node).__name__,0) + 1

    for field in node._fields:
        if field == "ctx":
            continue
        value = getattr(node, field)
        if isinstance(value, ast.AST):
            walk(value, depth + 1)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    walk(item, depth + 1)        
                    
    
for i in range(len(tree.body)):
    print(f"Body[{i}]:",tree.body[i])
    print(tree.body[i]._fields)
    node = tree.body[i]
    walk(node)
    print("==============================")


for key in type_dict.keys():
    print("keys:",key)      


