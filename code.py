import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
import heapq
import random
import os
from bfs import bfs
from dfs import dfs
from ucs import ucs
from quick_sort import quick_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from selection_sort import selection_sort

st.set_page_config(page_title="Algorithm Visualizer", layout="wide", initial_sidebar_state="auto")
st.markdown(
    '''
    <style>
    body, .main, .block-container {
        background: #f6f8fc !important;
        color: #1e293b !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');
    html, body, .main, .block-container {
        background: #181926 !important;
        color: #f1f5f9 !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        font-size: 17px;
        letter-spacing: 0.01em;
    }
    .main {
        background: #181926 !important;
        min-height: 100vh;
        padding: 32px 0 32px 0;
        max-width: 1200px;
        margin: 0 auto;
    }
    h1 {
        background: linear-gradient(90deg, #6366f1, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.7rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 2.2rem;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.18);
        line-height: 1.1;
    }
    h2, h3 {
        color: #f1f5f9;
        font-weight: 700;
        letter-spacing: -0.2px;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    h2 {
        font-size: 1.45rem;
        margin: 1.7rem 0 1.1rem 0;
        position: relative;
        padding-left: 0.8rem;
    }
    h2::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 3px;
        height: 20px;
        background: linear-gradient(90deg, #6366f1, #38bdf8);
        border-radius: 2px;
    }
    h3 {
        font-size: 1.08rem;
        margin-bottom: 1.1rem;
        font-weight: 600;
    }
    .stForm {
        background: rgba(36, 39, 58, 0.98) !important;
        backdrop-filter: blur(8px);
        border-radius: 18px;
        padding: 1.3rem 1.5rem 1.2rem 1.5rem;
        box-shadow: 0 4px 18px -4px rgba(0,0,0,0.22), 0 2px 6px -2px rgba(0,0,0,0.13);
        border: 1px solid rgba(99, 102, 241, 0.10);
        margin-bottom: 1.3rem;
        transition: all 0.3s cubic-bezier(.4,0,.2,1);
    }
    .stForm:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 28px -4px rgba(56,189,248,0.13), 0 3px 8px -2px rgba(99,102,241,0.08);
    }
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: #23243a !important;
        border: 2px solid #334155 !important;
        border-radius: 12px;
        padding: 0.85rem 1.1rem;
        font-size: 1.05rem;
        color: #f1f5f9 !important;
        transition: all 0.2s cubic-bezier(.4,0,.2,1);
        width: 100%;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        font-weight: 500;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56,189,248,0.13);
        outline: none;
        transform: translateY(-1px) scale(1.01);
    }
    .stButton button {
        background: linear-gradient(90deg, #6366f1, #38bdf8);
        color: #f1f5f9;
        border: none;
        padding: 0.85rem 1.5rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.08rem;
        transition: all 0.2s cubic-bezier(.4,0,.2,1);
        box-shadow: 0 2px 8px -1px rgba(56,189,248,0.10);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .stButton button:hover {
        transform: translateY(-1.5px) scale(1.01);
        box-shadow: 0 4px 14px -1px rgba(99,102,241,0.18);
        background: linear-gradient(90deg, #38bdf8, #6366f1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.7rem;
        background-color: #23243a !important;
        padding: 0.4rem 0.2rem;
        border-radius: 14px;
        margin-bottom: 1.2rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a5b4fc !important;
        font-weight: 600;
        padding: 0.7rem 1.3rem;
        border-radius: 10px;
        transition: all 0.2s cubic-bezier(.4,0,.2,1);
        background: rgba(36, 39, 58, 0.8) !important;
        font-size: 1.02rem;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #6366f1, #38bdf8) !important;
        color: #f1f5f9 !important;
        box-shadow: 0 2px 8px -1px rgba(56,189,248,0.10);
        transform: translateY(-1px) scale(1.01);
    }
    .stSuccess {
        background: #134e4a !important;
        color: #6ee7b7 !important;
        padding: 1rem 1.3rem;
        border-radius: 11px;
        margin: 1.1rem 0;
        border: 1px solid #6ee7b7;
        font-weight: 600;
        font-size: 1.01rem;
        box-shadow: 0 2px 6px -1px rgba(16,185,129,0.08);
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .stSlider {
        margin: 1.2rem 0;
    }
    .stSlider [data-baseweb="slider"] {
        background: #23243a !important;
        border-radius: 8px;
        height: 8px;
    }
    .stSlider [data-baseweb="slider"] [data-baseweb="thumb"] {
        background: #38bdf8 !important;
        border: 2px solid #181926;
        box-shadow: 0 2px 6px rgba(56,189,248,0.13);
        width: 18px;
        height: 18px;
    }
    .graph-container {
        background: rgba(36, 39, 58, 0.98) !important;
        backdrop-filter: blur(8px);
        padding: 1.3rem 1.5rem;
        border-radius: 18px;
        box-shadow: 0 4px 18px -4px rgba(0,0,0,0.22);
        border: 1px solid rgba(99, 102, 241, 0.10);
        margin: 1.1rem 0;
        transition: all 0.2s cubic-bezier(.4,0,.2,1);
    }
    .graph-container:hover {
        transform: translateY(-1.5px) scale(1.01);
        box-shadow: 0 8px 24px -4px rgba(56,189,248,0.10);
    }
    @media (max-width: 768px) {
        .main {
            padding: 1rem 0.2rem 1rem 0.2rem;
        }
        h1 {
            font-size: 1.5rem;
            margin-bottom: 1.1rem;
        }
        h2 {
            font-size: 1.1rem;
        }
        .stForm {
            padding: 0.7rem 0.5rem;
        }
        .stButton button {
            padding: 0.5rem 0.7rem;
            font-size: 0.95rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


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

# ----------------- Sorting Visualization Functions -----------------
def draw_bars(data, highlight_indices=None, default_color='#6366f1', highlight_color='#38bdf8', comparing_color='#f59e0b'):
    plt.figure(figsize=(max(10, len(data)//2), 2))
    if highlight_indices is None:
        highlight_indices = {}
    ax = plt.gca()
    ax.clear()
    
    for i, val in enumerate(data):
        if i in highlight_indices.get('comparing', []):
            color = comparing_color
        elif i in highlight_indices.get('swapped', []):
            color = highlight_color
        else:
            color = default_color
            
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color, ec='black'))
        ax.text(i + 0.5, 0.5, str(val), ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    
    ax.set_xlim(0, len(data))
    ax.set_ylim(0, 1)
    ax.axis('off')
    st.pyplot(plt)
    plt.close()

def insertion_sort(arr):
    steps = []
    steps.append((arr[:], {'comparing': [], 'swapped': []}))
    
    for i in range(1, len(arr)):
        j = i
        steps.append((arr[:], {'comparing': [j], 'swapped': []}))
        
        while j > 0 and arr[j-1] > arr[j]:
            steps.append((arr[:], {'comparing': [j, j-1], 'swapped': []}))
            arr[j], arr[j-1] = arr[j-1], arr[j]
            steps.append((arr[:], {'comparing': [], 'swapped': [j, j-1]}))
            j -= 1
    
    return steps

def merge_sort(arr):
    steps = []
    steps.append((arr[:], {'comparing': [], 'swapped': []}))
    
    def merge_sort_helper(array, l, r):
        if r - l > 1:
            m = (l + r) // 2
            merge_sort_helper(array, l, m)
            merge_sort_helper(array, m, r)
            
            left = array[l:m]
            right = array[m:r]
            i = j = 0
            k = l
            
            while i < len(left) and j < len(right):
                steps.append((array[:], {'comparing': [k], 'swapped': []}))
                if left[i] <= right[j]:
                    array[k] = left[i]
                    i += 1
                else:
                    array[k] = right[j]
                    j += 1
                steps.append((array[:], {'comparing': [], 'swapped': [k]}))
                k += 1
            
            while i < len(left):
                array[k] = left[i]
                steps.append((array[:], {'comparing': [], 'swapped': [k]}))
                i += 1
                k += 1
            
            while j < len(right):
                array[k] = right[j]
                steps.append((array[:], {'comparing': [], 'swapped': [k]}))
                j += 1
                k += 1
    
    merge_sort_helper(arr, 0, len(arr))
    return steps

def quick_sort(arr):
    steps = []
    steps.append((arr[:], {'comparing': [], 'swapped': []}))
    
    def quick_sort_helper(array, low, high):
        if low < high:
            pivot = array[high]
            i = low
            
            for j in range(low, high):
                steps.append((array[:], {'comparing': [j, high], 'swapped': []}))
                if array[j] < pivot:
                    array[i], array[j] = array[j], array[i]
                    steps.append((array[:], {'comparing': [], 'swapped': [i, j]}))
                    i += 1
            
            array[i], array[high] = array[high], array[i]
            steps.append((array[:], {'comparing': [], 'swapped': [i, high]}))
            
            quick_sort_helper(array, low, i - 1)
            quick_sort_helper(array, i + 1, high)
    
    quick_sort_helper(arr, 0, len(arr) - 1)
    return steps

def selection_sort(arr):
    steps = []
    steps.append((arr[:], {'comparing': [], 'swapped': []}))
    
    for i in range(len(arr)):
        min_idx = i
        steps.append((arr[:], {'comparing': [i], 'swapped': []}))
        
        for j in range(i + 1, len(arr)):
            steps.append((arr[:], {'comparing': [j, min_idx], 'swapped': []}))
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append((arr[:], {'comparing': [], 'swapped': [i, min_idx]}))
    
    return steps

# ----------------- Main Streamlit App -----------------

def main():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 3rem;
            text-align: center;
        ">
            <h1 style="color: white; text-shadow: none; -webkit-text-fill-color: white;">Algorithm Visualizer</h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.2rem; margin-top: 1rem;">
                Interactive visualization of graph and sorting algorithms
            </p>
        </div>
    """, unsafe_allow_html=True)

    if 'graph' not in st.session_state:
        st.session_state.graph = nx.Graph()

    graph = st.session_state.graph

    tab1, tab2, tab3 = st.tabs(["🎯 Graph Builder", "🔍 Algorithm Explorer", "📊 Sorting Visualizer"])

    # -------- Graph Builder Tab --------
    with tab1:
        st.markdown('<h2>Create and Manage Your Graph</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown('<div class="stForm">', unsafe_allow_html=True)
            st.markdown('<h3 style="margin-bottom: 1.5rem;">Add New Node</h3>', unsafe_allow_html=True)
            with st.form("Add Node"):
                node_name = st.text_input("Node Label", placeholder="Enter node name...")
                submitted_node = st.form_submit_button("✨ Add Node")
                if submitted_node and node_name:
                    graph.add_node(node_name)
                    st.success(f"Node '{node_name}' created successfully!")
            st.markdown('</div>', unsafe_allow_html=True)

            if graph.number_of_nodes() >= 2:
                st.markdown('<div class="stForm">', unsafe_allow_html=True)
                st.markdown('<h3 style="margin-bottom: 1.5rem;">Connect Nodes</h3>', unsafe_allow_html=True)
                with st.form("Add Edge"):
                    node1 = st.selectbox("From Node", list(graph.nodes), key="node1")
                    node2 = st.selectbox("To Node", list(graph.nodes), key="node2")
                    weight = st.number_input("Edge Weight", min_value=1, value=1)
                    submitted_edge = st.form_submit_button("🔗 Connect Nodes")
                    if submitted_edge and node1 != node2:
                        graph.add_edge(node1, node2, weight=weight)
                        st.success(f"Connected '{node1}' → '{node2}' (weight: {weight})")
                st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="stForm">', unsafe_allow_html=True)
            st.markdown('<h3 style="margin-bottom: 1.5rem;">Manage Graph</h3>', unsafe_allow_html=True)
            
            if graph.number_of_nodes() > 0:
                with st.form("Remove Node"):
                    node_to_remove = st.selectbox("Select Node to Remove", list(graph.nodes))
                    submitted_remove_node = st.form_submit_button("🗑️ Remove Node")
                    if submitted_remove_node:
                        graph.remove_node(node_to_remove)
                        st.success(f"Node '{node_to_remove}' removed successfully!")

            if graph.number_of_edges() > 0:
                with st.form("Remove Edge"):
                    edge_list = list(graph.edges)
                    edge_to_remove = st.selectbox("Select Edge to Remove", edge_list)
                    submitted_remove_edge = st.form_submit_button("✂️ Remove Edge")
                    if submitted_remove_edge:
                        graph.remove_edge(*edge_to_remove)
                        st.success(f"Edge {edge_to_remove} removed successfully!")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="graph-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 1.5rem;">Graph Preview</h3>', unsafe_allow_html=True)
        zoom = st.slider("🔍 Zoom Level", 0.5, 3.0, 1.5, 0.1)
        pos = nx.spring_layout(graph, seed=42)
        draw_graph(graph, [], pos, zoom, "lightblue")
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- Algorithm Explorer Tab --------
    with tab2:
        st.markdown('<h2>Explore Graph Algorithms</h2>', unsafe_allow_html=True)
        
        if graph.number_of_nodes() > 0:
            st.markdown('<div class="stForm">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                start_node = st.selectbox("Starting Node", list(graph.nodes), key="startnode")
                algorithm = st.selectbox("Algorithm", ["BFS", "DFS", "UCS"])
            
            with col2:
                speed = st.slider("⚡ Animation Speed", 0.1, 2.0, 0.7, 0.1)
            
            if st.button("▶️ Start Algorithm", use_container_width=True):
                if algorithm == "BFS":
                    steps = bfs(graph, start_node)
                    color = '#f59e0b'  # Amber
                elif algorithm == "DFS":
                    steps = dfs(graph, start_node)
                    color = '#3b82f6'  # Blue
                else:
                    steps = ucs(graph, start_node)
                    color = '#10b981'  # Green

                st.markdown('<div class="graph-container">', unsafe_allow_html=True)
                for step in steps:
                    draw_graph(graph, step, pos, zoom, color)
                    time.sleep(speed)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Please create a graph first in the Graph Builder tab.")

    # -------- Sorting Visualizer Tab --------
    with tab3:
        st.markdown('<h2>Sorting Algorithms</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="stForm">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            sort_algo = st.selectbox("Algorithm", ["Insertion Sort", "Merge Sort", "Quick Sort", "Selection Sort"])
            
            input_method = st.radio("Choose input method:", ["Manual Input", "Random Numbers"])
            
            if input_method == "Manual Input":
                input_text = st.text_input(
                    "Enter numbers (separated by commas)",
                    placeholder="Example: 5,3,8,6,2",
                    help="Enter numbers separated by commas. Example: 5,3,8,6,2"
                )
                
                try:
                    data = [int(x.strip()) for x in input_text.split(",") if x.strip()]
                    if not data:
                        st.warning("Please enter some numbers!")
                        data = []
                except ValueError:
                    st.error("Invalid input! Please enter only numbers separated by commas.")
                    data = []
            else:
                size = st.slider("📊 Array Size", 5, 30, 10)
                data = [random.randint(1, 100) for _ in range(size)]
        
        with col2:
            speed = st.slider("⚡ Animation Speed", 0.1, 1.0, 0.5, 0.1)
            
            if st.button("Clear Input", use_container_width=True):
                if 'input_text' in st.session_state:
                    del st.session_state.input_text
                data = []
                st.empty()  

        if st.button("▶️ Start Sorting", use_container_width=True):
            if not data:
                st.error("Please enter some numbers first!")
            else:
                st.markdown('<div class="graph-container">', unsafe_allow_html=True)
                st.write("Original Array:")
                draw_bars(data)
                
                try:
                    if sort_algo == "Insertion Sort":
                        steps = insertion_sort(data[:])
                    elif sort_algo == "Merge Sort":
                        steps = merge_sort(data[:])
                    elif sort_algo == "Quick Sort":
                        steps = quick_sort(data[:])
                    else:
                        steps = selection_sort(data[:])

                    for data_step, highlights in steps:
                        draw_bars(data_step, highlights)
                        time.sleep(speed)
                        
                        if highlights.get('comparing'):
                            st.write(f"Comparing elements at positions: {highlights['comparing']}")
                        if highlights.get('swapped'):
                            st.write(f"Swapped elements at positions: {highlights['swapped']}")
                    
                    st.success(f"{sort_algo} completed successfully!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
