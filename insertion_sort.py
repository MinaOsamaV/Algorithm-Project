def insertion_sort(arr, save_log=None):
    steps = [arr[:]]
    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j-1] > arr[j]:
            arr[j], arr[j-1] = arr[j-1], arr[j]
            j -= 1
            steps.append(arr[:])
    if save_log:
        save_log("insertion_sort_steps", steps)
    return steps 