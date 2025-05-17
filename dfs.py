def dfs(graph, start_node, visited=None, steps=None, save_log=None):
    if visited is None:
        visited = []
    if steps is None:
        steps = []
    visited.append(start_node)
    steps.append(visited[:])
    for neighbor in graph.neighbors(start_node):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, steps)
    if save_log:
        save_log("dfs_steps", steps)
    return steps 