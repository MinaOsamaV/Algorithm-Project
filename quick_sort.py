def quick_sort(arr, save_log=None):
    steps = [arr[:]]
    def quick_sort_helper(array, low, high):
        if low < high:
            pivot = array[high]
            i = low
            for j in range(low, high):
                if array[j] < pivot:
                    array[i], array[j] = array[j], array[i]
                    i += 1
                    steps.append(array[:])
                    yield array[:]
            array[i], array[high] = array[high], array[i]
            steps.append(array[:])
            yield array[:]
            yield from quick_sort_helper(array, low, i - 1)
            yield from quick_sort_helper(array, i + 1, high)
    yield from quick_sort_helper(arr, 0, len(arr) - 1)
    if save_log:
        save_log("quick_sort_steps", steps) 