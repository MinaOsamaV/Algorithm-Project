import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
import heapq
import random
import os

# ----------------- Prepare Logs Directory -----------------

if not os.path.exists("logs"):
    os.makedirs("logs")

def save_log(filename, steps):
    with open(f"logs/{filename}.txt", "w") as f:
        for step in steps:
            f.write(str(step) + "\n")

# ----------------- Graph Visualization Functions -----------------

def draw_graph(graph, visited_nodes, pos, zoom, color):
    plt.figure(figsize=(10, 7))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=18, font_color='black')
    if visited_nodes:
        nx.draw_networkx_nodes(graph, pos, nodelist=visited_nodes, node_color=color, node_size=700)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.xlim([-zoom, zoom])
    plt.ylim([-zoom, zoom])
    st.pyplot(plt)
    plt.close()

# ----------------- Graph Algorithms -----------------

def bfs(graph, start_node):
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
    save_log("bfs_steps", steps)
    return steps

def dfs(graph, start_node, visited=None, steps=None):
    if visited is None:
        visited = []
    if steps is None:
        steps = []
    visited.append(start_node)
    steps.append(visited[:])
    for neighbor in graph.neighbors(start_node):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, steps)
    return steps

def ucs(graph, start_node):
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
    save_log("ucs_steps", steps)
    return steps

# ----------------- Sorting Algorithms -----------------

def draw_bars(data, color='skyblue'):
    plt.figure(figsize=(10, 4))
    plt.bar(range(len(data)), data, color=color)
    st.pyplot(plt)
    plt.close()

def insertion_sort(arr):
    steps = [arr[:]]
    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j-1] > arr[j]:
            arr[j], arr[j-1] = arr[j-1], arr[j]
            j -= 1
            steps.append(arr[:])
    save_log("insertion_sort_steps", steps)
    return steps

def merge_sort(arr):
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
    save_log("merge_sort_steps", steps)

def quick_sort(arr):
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
    save_log("quick_sort_steps", steps)

def selection_sort(arr):
    steps = [arr[:]]
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr[:])
    save_log("selection_sort_steps", steps)
    return steps

# ----------------- Main Streamlit App -----------------

def main():
    st.title("Graph and Sorting Visualizer")

    if 'graph' not in st.session_state:
        st.session_state.graph = nx.Graph()

    graph = st.session_state.graph

    tab1, tab2, tab3 = st.tabs(["Graph Management", "Graph Algorithms", "Sorting Visualizer"])

    # -------- Graph Management Tab --------
    with tab1:
        st.header("Add Node:")
        with st.form("Add Node"):
            node_name = st.text_input("Node name:")
            submitted_node = st.form_submit_button("Add Node")
            if submitted_node and node_name:
                graph.add_node(node_name)
                st.success(f"Node '{node_name}' added.")

        st.header("Add Edge:")
        if graph.number_of_nodes() >= 2:
            with st.form("Add Edge"):
                node1 = st.selectbox("Node 1:", list(graph.nodes), key="node1")
                node2 = st.selectbox("Node 2:", list(graph.nodes), key="node2")
                weight = st.number_input("Weight (default = 1):", min_value=1, value=1)
                submitted_edge = st.form_submit_button("Add Edge")
                if submitted_edge and node1 != node2:
                    graph.add_edge(node1, node2, weight=weight)
                    st.success(f"Connected '{node1}' to '{node2}' with weight {weight}")

        st.header("Remove Node:")
        if graph.number_of_nodes() > 0:
            with st.form("Remove Node"):
                node_to_remove = st.selectbox("Select node to remove:", list(graph.nodes))
                submitted_remove_node = st.form_submit_button("Remove Node")
                if submitted_remove_node:
                    graph.remove_node(node_to_remove)
                    st.success(f"Node '{node_to_remove}' removed.")

        st.header("Remove Edge:")
        if graph.number_of_edges() > 0:
            with st.form("Remove Edge"):
                edge_list = list(graph.edges)
                edge_to_remove = st.selectbox("Select edge to remove:", edge_list)
                submitted_remove_edge = st.form_submit_button("Remove Edge")
                if submitted_remove_edge:
                    graph.remove_edge(*edge_to_remove)
                    st.success(f"Edge {edge_to_remove} removed.")

        st.subheader("Graph Visualization:")
        zoom = st.slider("Zoom level:", 0.5, 3.0, 1.5, 0.1)
        pos = nx.spring_layout(graph, seed=42)
        draw_graph(graph, [], pos, zoom, "lightblue")

    # -------- Graph Algorithms Tab --------
    with tab2:
        st.header("Run Graph Algorithms:")
        if graph.number_of_nodes() > 0:
            start_node = st.selectbox("Start node:", list(graph.nodes), key="startnode")
            algorithm = st.selectbox("Choose algorithm:", ["BFS", "DFS", "UCS"])
            speed = st.slider("Animation speed (seconds):", 0.1, 2.0, 0.7, 0.1)

            if st.button("Start Search"):
                if algorithm == "BFS":
                    steps = bfs(graph, start_node)
                    color = 'orange'
                elif algorithm == "DFS":
                    steps = dfs(graph, start_node)
                    save_log("dfs_steps", steps)
                    color = 'blue'
                else:
                    steps = ucs(graph, start_node)
                    color = 'green'

                for step in steps:
                    draw_graph(graph, step, pos, zoom, color)
                    time.sleep(speed)

    # -------- Sorting Visualizer Tab --------
    with tab3:
        st.header("Sorting Visualizer")
        sort_algo = st.selectbox("Choose sorting algorithm:", ["Insertion Sort", "Merge Sort", "Quick Sort", "Selection Sort"])
        size = st.slider("Array size:", 5, 30, 10)
        speed = st.slider("Animation speed (seconds):", 0.1, 1.0, 0.5, 0.1)
        data = [random.randint(1, 100) for _ in range(size)]

        if st.button("Start Sorting"):
            st.write("Original Array:")
            draw_bars(data)
            if sort_algo == "Insertion Sort":
                steps = insertion_sort(data[:])
            elif sort_algo == "Merge Sort":
                steps = list(merge_sort(data[:]))
            elif sort_algo == "Quick Sort":
                steps = list(quick_sort(data[:]))
            else:
                steps = selection_sort(data[:])

            for step in steps:
                draw_bars(step)
                time.sleep(speed)

if __name__ == "__main__":
    main()
