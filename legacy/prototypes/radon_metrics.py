from radon.complexity import cc_visit
from radon.metrics import h_visit, mi_visit
from radon.raw import analyze

def get_radon_metrics(code):
    cc = cc_visit(code)
    halstead = h_visit(code).total
    raw = analyze(code)
    mi = mi_visit(code,multi = True)
    return {
        "cyclomatic": [c.complexity for c in cc],
        "halstead": halstead,
        "raw": raw,
        "maintainability": mi,
    }

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

def printRadonMetric(rad_metrics):
    print(f"Clyclomatic Complexity:{rad_metrics['cyclomatic']}")
    print(f"Halstead Complexity:{rad_metrics['halstead']}")
    print(f"Raw Complexity:{rad_metrics['raw']}")
    print(f"Maintainibility:{rad_metrics['maintainability']}")

rad_metrics = get_radon_metrics(source)
printRadonMetric(rad_metrics)

