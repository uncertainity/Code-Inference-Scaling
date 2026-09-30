import sys

# Gustavo Eugenio John - RA 248318
# Algoritmo genérico de Toplogical Sort produzido com IA generativa
def topological_sort(adj, start):
    visited = [False] * len(adj)
    order = []
    stack = []
    stack.append((start, 0))
    visited[start] = True
    while (len(stack) > 0):
        current, index = stack.pop()
        if (index < len(adj[current])):
            stack.append((current, (index + 1)))
            neighbor = adj[current][index]
            if (not visited[neighbor]):
                visited[neighbor] = True
                stack.append((neighbor, 0))
        else:
            order.append(current)
    return order

# fim do algoritmo

def main():
    input_ = sys.stdin.read().split()
    input_.reverse() #pilha

    vertices = int(input_.pop())

    vizinhos = []
    for i in range((vertices+1)):
        vizinhos.append([])

    for livro in range(1, (vertices+1)):
        c = int(input_.pop())
        for k in range(c):
            vizinhos[livro].append(int(input_.pop()))

    ordenacao = topological_sort(vizinhos, 1)

    resultado = []
    for atual in ordenacao:
        if (atual != 1):
            resultado.append(str(atual))

    print(" ".join(resultado)) # pra otimizar


main()