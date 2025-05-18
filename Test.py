import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
import heapq
import os

# ----------------- Prepare Logs Directory -----------------
if not os.path.exists("logs"):
    os.makedirs("logs")

def save_log(filename, steps):
    with open(f"logs/{filename}.txt", "w") as f:
        for step in steps:
            f.write(str(step) + "\n")

# ----------------- Graph Visualization Functions -----------------
def draw_graph(graph, visited_nodes, pos, zoom, color, directed):
    plt.figure(figsize=(10, 7))
    if directed:
        nx.draw_networkx_edges(graph, pos, arrowstyle='->', arrows=True, edge_color='gray')
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=16, font_color='black')
    if visited_nodes:
        nx.draw_networkx_nodes(graph, pos, nodelist=visited_nodes, node_color=color, node_size=800)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red', font_size=12)
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

# ----------------- Sorting Visualization Functions -----------------
def draw_bars(data, highlight_indices=None, default_color='skyblue', highlight_color='orange'):
    plt.figure(figsize=(max(10, len(data)//2), 2))
    if highlight_indices is None:
        highlight_indices = []
    ax = plt.gca()
    ax.clear()
    for i, val in enumerate(data):
        color = highlight_color if i in highlight_indices else default_color
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color, ec='black'))
        ax.text(i + 0.5, 0.5, str(val), ha='center', va='center', fontsize=12, color='black')
    ax.set_xlim(0, len(data))
    ax.set_ylim(0, 1)
    ax.axis('off')
    st.pyplot(plt)
    plt.close()

def insertion_sort(arr):
    steps = [(arr[:], [])]
    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j-1] > arr[j]:
            arr[j], arr[j-1] = arr[j-1], arr[j]
            j -= 1
            steps.append((arr[:], [j, j+1]))
    save_log("insertion_sort_steps", [step[0] for step in steps])
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
    steps = [(arr[:], [])]
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append((arr[:], [i, min_idx]))
    save_log("selection_sort_steps", [step[0] for step in steps])
    return steps

# ----------------- Main Streamlit App -----------------
def main():
    st.set_page_config(page_title="Graph & Sorting Visualizer", page_icon="📊", layout="wide")

    st.title("📊 Graph and Sorting Visualizer")
    st.markdown(
        """
        <style>
        .css-18e3th9 {padding-top: 1rem;}  /* تقليل المسافة العلوية */
        .stButton>button {background-color: #4CAF50; color: white; font-weight: bold;}
        .stRadio > div {flex-direction: row;}  /* لجعل الخيارات بجانب بعض */
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar controls
    with st.sidebar:
        st.header("Graph Settings")
        directed = st.radio("Graph Type:", ["Undirected", "Directed"]) == "Directed"
        st.session_state.directed = directed
        zoom = st.slider("Zoom level:", 0.5, 3.0, 1.5, 0.1)

    if 'graph' not in st.session_state or st.session_state.directed != directed:
        st.session_state.graph = nx.DiGraph() if directed else nx.Graph()

    graph = st.session_state.graph

    tab1, tab2, tab3 = st.tabs(["🧩 Graph Management", "🚀 Graph Algorithms", "🔢 Sorting Visualizer"])

    # -------- Graph Management Tab --------
    with tab1:
        st.header("🧩 Graph Management")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Add Node")
            with st.form("Add Node Form"):
                node_name = st.text_input("Node name")
                submitted_node = st.form_submit_button("Add Node")
                if submitted_node:
                    if node_name:
                        if node_name in graph.nodes:
                            st.warning(f"Node '{node_name}' already exists!")
                        else:
                            graph.add_node(node_name)
                            st.success(f"Node '{node_name}' added.")
                    else:
                        st.error("Please enter a node name.")

            st.subheader("Remove Node")
            if graph.number_of_nodes() > 0:
                with st.form("Remove Node Form"):
                    node_to_remove = st.selectbox("Select node to remove", list(graph.nodes))
                    submitted_remove_node = st.form_submit_button("Remove Node")
                    if submitted_remove_node:
                        graph.remove_node(node_to_remove)
                        st.success(f"Node '{node_to_remove}' removed.")
            else:
                st.info("No nodes to remove.")

        with col2:
            st.subheader("Add Edge")
            if graph.number_of_nodes() >= 2:
                with st.form("Add Edge Form"):
                    node1 = st.selectbox("Node 1", list(graph.nodes), key="node1")
                    node2 = st.selectbox("Node 2", list(graph.nodes), key="node2")
                    weight = st.number_input("Weight (default = 1)", min_value=1, value=1)
                    submitted_edge = st.form_submit_button("Add Edge")
                    if submitted_edge:
                        if node1 == node2:
                            st.error("Cannot connect a node to itself.")
                        elif graph.has_edge(node1, node2):
                            st.warning(f"Edge from '{node1}' to '{node2}' already exists.")
                        else:
                            graph.add_edge(node1, node2, weight=weight)
                            st.success(f"Edge added from '{node1}' to '{node2}' with weight {weight}.")
            else:
                st.info("Add at least two nodes to add edges.")

            st.subheader("Remove Edge")
            if graph.number_of_edges() > 0:
                with st.form("Remove Edge Form"):
                    edges = list(graph.edges)
                    edge_to_remove = st.selectbox("Select edge to remove", edges)
                    submitted_remove_edge = st.form_submit_button("Remove Edge")
                    if submitted_remove_edge:
                        graph.remove_edge(*edge_to_remove)
                        st.success(f"Edge {edge_to_remove} removed.")
            else:
                st.info("No edges to remove.")

        # Draw graph
        if graph.number_of_nodes() > 0:
            pos = nx.spring_layout(graph, seed=42)
            draw_graph(graph, [], pos, zoom * 3, "red", directed)
        else:
            st.info("Add nodes to display the graph.")

    # -------- Graph Algorithms Tab --------
    with tab2:
        st.header("🚀 Graph Algorithms")

        if graph.number_of_nodes() == 0:
            st.info("Add nodes to run algorithms.")
        else:
            start_node = st.selectbox("Select start node:", list(graph.nodes))

            algorithm = st.selectbox("Choose algorithm:", ["BFS", "DFS", "UCS"])

            run_algo = st.button("Run Algorithm")

            if run_algo:
                pos = nx.spring_layout(graph, seed=42)
                if algorithm == "BFS":
                    steps = bfs(graph, start_node)
                elif algorithm == "DFS":
                    steps = dfs(graph, start_node)
                else:
                    steps = ucs(graph, start_node)

                st.subheader(f"Steps for {algorithm}:")
                for step in steps:
                    draw_graph(graph, step, pos, zoom * 3, "yellow", directed)
                    time.sleep(0.7)

                st.success(f"{algorithm} completed. Check logs folder for detailed steps.")

    # -------- Sorting Visualizer Tab --------
    with tab3:
        st.header("🔢 Sorting Visualizer")

        sorting_alg = st.selectbox("Select sorting algorithm:",
                                   ["Insertion Sort", "Merge Sort", "Quick Sort", "Selection Sort"])

        arr_input = st.text_input("Enter numbers separated by commas", "5,3,8,6,2")

        try:
            arr = [int(x.strip()) for x in arr_input.split(",")]
        except:
            st.error("Invalid input! Please enter only numbers separated by commas.")
            arr = []

        run_sort = st.button("Visualize Sorting")

        if run_sort and arr:
            if sorting_alg == "Insertion Sort":
                steps = insertion_sort(arr.copy())
                for data, highlights in steps:
                    draw_bars(data, highlights)
                    time.sleep(0.5)

            elif sorting_alg == "Merge Sort":
                gen = merge_sort(arr.copy())
                for step in gen:
                    draw_bars(step)
                    time.sleep(0.5)

            elif sorting_alg == "Quick Sort":
                gen = quick_sort(arr.copy())
                for step in gen:
                    draw_bars(step)
                    time.sleep(0.5)

            elif sorting_alg == "Selection Sort":
                steps = selection_sort(arr.copy())
                for data, highlights in steps:
                    draw_bars(data, highlights)
                    time.sleep(0.5)

            st.success(f"{sorting_alg} visualization completed. Check logs folder for steps.")

if __name__ == "__main__":
    main()
