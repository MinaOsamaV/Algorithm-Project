def selection_sort(l, save_log=None):
    steps = [(l[:], {'comparing': [], 'swapped': []})]
    for i in range(len(l) - 1):
        min_index = i
        steps.append((l[:], {'comparing': [i], 'swapped': []}))
        
        for j in range(i + 1, len(l)):
            steps.append((l[:], {'comparing': [j, min_index], 'swapped': []}))
            if l[j] < l[min_index]:
                min_index = j
        
        if min_index != i:
            l[i], l[min_index] = l[min_index], l[i]
            steps.append((l[:], {'comparing': [], 'swapped': [i, min_index]}))

    if save_log:
        save_log("selection_sort_steps", steps)
    return steps

l=[1,20,30,150,120,6,7,90,110]

print(selection_sort(l))