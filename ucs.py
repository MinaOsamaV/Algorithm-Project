import heapq

def ucs(graph, start_node, save_log=None):
    visited = []
    queue = [(0, start_node)]
    heapq.heapify(queue)
    costs = {start_node: 0}
    steps = []
    while queue:
        cost, node = heapq.heappop(queue)
        if node not in visited:
            visited.append(node)
            steps.append(visited[:])
            for neighbor in graph.neighbors(node):
                edge_weight = graph[node][neighbor].get('weight', 1)
                new_cost = cost + edge_weight
                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor))
    if save_log:
        save_log("ucs_steps", steps)
    return steps 