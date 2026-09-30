import sys

def main():
    # Read all inputs from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    
    # Parse the remaining items into a 2D grid matrix A
    A = []
    for i in range(1, N + 1):
        A.append(list(input_data[i]))
        
    # Create a replica matrix B to keep all internal elements unchanged
    B = [row[:] for row in A]
    
    # Loop 1: Top row shifts elements to the right
    for j in range(N - 1):
        B[0][j + 1] = A[0][j]
        
    # Loop 2: Right column shifts elements down
    for i in range(N - 1):
        B[i + 1][N - 1] = A[i][N - 1]
        
    # Loop 3: Bottom row shifts elements to the left
    for j in range(N - 1, 0, -1):
        B[N - 1][j - 1] = A[N - 1][j]
        
    # Loop 4: Left column shifts elements up
    for i in range(N - 1, 0, -1):
        B[i - 1][0] = A[i][0]
        
    # Print the resulting matrix B row by row
    for row in B:
        print("".join(row))

if __name__ == '__main__':
    main()