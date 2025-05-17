import heapq

def bfs(graph, start_node, save_log=None):
    visited = []
    queue = [start_node]
    steps = []
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            steps.append(visited[:])
            for neighbor in graph.neighbors(node):
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
    if save_log:
        save_log("bfs_steps", steps)
    return steps 