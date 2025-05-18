def insertion_sort(l, save_log=None):
    steps = [(l[:], {'comparing': [], 'swapped': []})]
    for i in range(1, len(l)):
        current = l[i]
        j = i - 1
        steps.append((l[:], {'comparing': [i], 'swapped': []}))
        
        while j >= 0 and l[j] > current:
            steps.append((l[:], {'comparing': [j, j+1], 'swapped': []}))
            l[j + 1] = l[j]
            steps.append((l[:], {'comparing': [], 'swapped': [j, j+1]}))
            j -= 1
        
        l[j + 1] = current
        steps.append((l[:], {'comparing': [], 'swapped': [j+1]}))

    if save_log:
        save_log("insertion_sort_steps", steps)
    return steps 