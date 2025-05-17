def merge_sort(arr, save_log=None):
    steps = [arr[:]]
    def merge_sort_helper(array, l, r):
        if r - l > 1:
            m = (l + r) // 2
            yield from merge_sort_helper(array, l, m)
            yield from merge_sort_helper(array, m, r)
            left, right = array[l:m], array[m:r]
            i = j = 0
            for k in range(l, r):
                if j >= len(right) or (i < len(left) and left[i] < right[j]):
                    array[k] = left[i]
                    i += 1
                else:
                    array[k] = right[j]
                    j += 1
                steps.append(array[:])
                yield array[:]
    yield from merge_sort_helper(arr, 0, len(arr))
    if save_log:
        save_log("merge_sort_steps", steps) 