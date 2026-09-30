import ast
import radon
import re
from radon.complexity import cc_visit
from radon.metrics import h_visit, mi_visit
from radon.raw import analyze
import textwrap

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

class getTraces():
    
    def __init__(self,source):
        self.source = source
        self.unique_dict = {}
        self.simplified_events = []
        self.variable_dict = {}
        self.call_dict = {}
        self.function_defs = set()
        self.max_nesting_depths = -1

    def handlerFunctions(self,node,depth):
        if isinstance(node, ast.FunctionDef):
            payload = f"depth ={depth}, FunctionDef name={node.name}" 
            self.function_defs.add(node.name)
                    
        elif isinstance(node, ast.Name):
            payload = f"depth ={depth},Name id={node.id} ctx={type(node.ctx).__name__}"
            if isinstance(node.ctx, ast.Store):
                self.variable_dict[node.id] = self.variable_dict.get(node.id, 0) + 1

        elif isinstance(node, ast.arg):
            payload = f"depth ={depth},arg name={node.arg}" 
            
        elif isinstance(node, ast.Constant):
            payload = f"depth ={depth},Constant value={node.value}" 
            
        elif isinstance(node, ast.Attribute):
            payload = f"depth ={depth},Attribute attr={node.attr}" 
            
        elif isinstance(node, ast.Call):
            payload = f"depth ={depth},Call" 
            if isinstance(node.func, ast.Name):
                call_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                call_name = node.func.attr
            else:
                call_name = type(node.func).__name__
            self.call_dict[call_name] = self.call_dict.get(call_name, 0) + 1
            
        else:
            payload = f"depth ={depth},{type(node).__name__}"  
            self.unique_dict[type(node).__name__] = self.unique_dict.get(type(node).__name__,0) + 1
        return payload

 
    def walk(self,node,depth = 0):
        payload = self.handlerFunctions(node,depth)
        self.simplified_events.append(payload)

        for field in node._fields:
            if field == "ctx":
                continue
            value = getattr(node,field)
            if isinstance(value,ast.AST):
                self.walk(value,depth + 1)
            elif isinstance(value,list):
                for item in value:
                    if isinstance(item,ast.AST):
                        self.walk(item,depth + 1)
                        
    def callWalk(self):
        source = textwrap.dedent(self.source).strip()
        tree = ast.parse(self.source)
        total_len = len(tree.body)
        for i in range(total_len):
            node = tree.body[i]
            self.walk(node)
            
    def getMaxControlNesting(self):
        control_statements = ["If","For","While"]
        #depth_regex = re.search(r"depth\s*=\s*(\d+)")
        #payload_regex = re.search(r"depth\s*=\s\d+,(.*)")
        
        cur_depth = -1
        start_depth = -1
        control_depth = 0
        nested_flag = 0
        control_nesting_depths = []
        payload = ""
        
        for line in self.simplified_events:
            #print("line:",line)
            payload_match = re.search(r"depth\s*=\s*\d+,(.*)",line)
            cur_depth_match = re.search(r"depth\s*=\s*(\d+)",line)
            
            if payload_match:
                payload = payload_match.group(1)
                #print("Payload:",payload)
            if cur_depth_match:
                cur_depth = cur_depth_match.group(1)
                #print("Cur Depth:",cur_depth)
                
            if payload in control_statements:
                if nested_flag == 0:
                    start_depth = cur_depth
                    nested_flag = 1
                control_depth += 1
            else:
                if start_depth == cur_depth and nested_flag == 1:
                    control_nesting_depths.append(control_depth)
                    control_depth = 0
                    nested_flag = 0
        
        #print(f"All nesting depths:{control_nesting_depths}")
        if len(control_nesting_depths) > 0:
            self.max_nesting_depths = max(control_nesting_depths)
        else:
            self.max_nesting_depths = 0
    
    def getASTMetrics(self):
        self.callWalk()
        self.getMaxControlNesting()
        self.ast_metrics = {"AST_Length":len(self.simplified_events),
                             "Max_Nesting_Depth":self.max_nesting_depths,"Number_of_Calls":len(self.call_dict),
                             "Number_of_Vars":len(self.variable_dict)}
        return self.ast_metrics


class RadonMetrics:
    def __init__(self,source):
        self.source = textwrap.dedent(source).strip()
        
    def flatten_radon_metrics(self,radon_metrics):
        return {
            "cyclomatic": radon_metrics["cyclomatic"],
            "maintainability": radon_metrics["maintainability"],

            # Halstead fields
            "halstead_volume": radon_metrics["halstead"].volume,
            "halstead_difficulty": radon_metrics["halstead"].difficulty,
            "halstead_effort": radon_metrics["halstead"].effort,
            "halstead_bugs": radon_metrics["halstead"].bugs,

            # Raw fields
            "loc": radon_metrics["raw"].loc,
            "lloc": radon_metrics["raw"].lloc,
            "sloc": radon_metrics["raw"].sloc,
            "comments": radon_metrics["raw"].comments,
            "blank": radon_metrics["raw"].blank,
        }
        
    def getRadonMetrics(self):
        cc = cc_visit(self.source)
        halstead = h_visit(self.source).total
        raw = analyze(self.source)
        mi = mi_visit(self.source,multi = True)
        avg_cc = 0
        for idx in range(len(cc)):
            avg_cc += cc[idx].complexity
        avg_cc = avg_cc/len(cc)
        raw_radon_metrics = {"cyclomatic":avg_cc,"halstead":halstead,"raw":raw,"maintainability":mi}
        self.radon_metrics = self.flatten_radon_metrics(raw_radon_metrics)
        return self.radon_metrics
                         
        
# astTrace = getTraces(source)
# radonTrace = RadonMetrics(source)
# ast_metrics = astTrace.getASTMetrics()
# radon_metrics = radonTrace.getRadonMetrics()
# print("Ast metrics:",ast_metrics)
# print("Radon metrics:",radon_metrics)



    
