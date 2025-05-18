def merge_sort(arr, save_log=None):
    steps = [(arr[:], {'comparing': [], 'swapped': []})]
    
    def merge(A, p, q, r):
        n1 = q - p + 1
        n2 = r - q
        
        L = [0] * (n1 + 1)
        R = [0] * (n2 + 1)
        
        for i in range(n1):
            L[i] = A[p + i]
        
        for j in range(n2):
            R[j] = A[q + 1 + j]
        
        L[n1] = float('inf')
        R[n2] = float('inf')
        
        i = 0
        j = 0
        
        for k in range(p, r + 1):
            steps.append((A[:], {'comparing': [k], 'swapped': []}))
            if L[i] <= R[j]:
                A[k] = L[i]
                i += 1
            else:
                A[k] = R[j]
                j += 1
            steps.append((A[:], {'comparing': [], 'swapped': [k]}))
    
    def merge_sort_helper(A, p, r):
        if p < r:
            q = (p + r) // 2
            merge_sort_helper(A, p, q)
            merge_sort_helper(A, q + 1, r)
            merge(A, p, q, r)
    
    merge_sort_helper(arr, 0, len(arr) - 1)
    if save_log:
        save_log("merge_sort_steps", steps)
    return steps 