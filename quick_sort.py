def quick_sort(arr, save_log=None):
    steps = [(arr[:], {'comparing': [], 'swapped': []})]
    
    def partition(l, low, high):
        pivot = l[low]
        i = low - 1
        j = high + 1
        
        while True:
            j -= 1
            while l[j] > pivot:
                j -= 1
            
            i += 1
            while l[i] < pivot:
                i += 1
            
            if i < j:
                steps.append((l[:], {'comparing': [i, j], 'swapped': []}))
                l[i], l[j] = l[j], l[i]
                steps.append((l[:], {'comparing': [], 'swapped': [i, j]}))
            else:
                return j
    
    def quick_sort_helper(l, low, high):
        if low < high:
            q = partition(l, low, high)
            quick_sort_helper(l, low, q)
            quick_sort_helper(l, q + 1, high)
    
    quick_sort_helper(arr, 0, len(arr) - 1)
    if save_log:
        save_log("quick_sort_steps", steps)
    return steps 