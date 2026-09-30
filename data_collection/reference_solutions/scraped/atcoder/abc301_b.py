import sys

def main():
    # Read all tokens from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = [int(x) for x in input_data[1:]]
    
    result = []
    
    # Iterate through the sequence up to the second-to-last element
    for i in range(N - 1):
        curr_val = A[i]
        next_val = A[i + 1]
        
        # Append the current element
        result.append(curr_val)
        
        # Case 1: Gap going upwards
        if curr_val < next_val:
            # e.g., range(2, 5) -> 3, 4
            for num in range(curr_val + 1, next_val):
                result.append(num)
                
        # Case 2: Gap going downwards
        elif curr_val > next_val:
            # e.g., range(5 - 1, 1, -1) -> 4, 3, 2
            for num in range(curr_val - 1, next_val, -1):
                result.append(num)
                
    # Don't forget to append the final element of the sequence at the very end
    result.append(A[-1])
    
    # Print the resulting sequence separated by a space
    print(*(result))

if __name__ == '__main__':
    main()