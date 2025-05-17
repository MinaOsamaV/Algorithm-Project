def selection_sort(arr, save_log=None):
    steps = [arr[:]]
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr[:])
    if save_log:
        save_log("selection_sort_steps", steps)
    return steps 