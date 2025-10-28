import tkinter as tk
from tkinter import messagebox, ttk
import heapq

# ------------------- DIJKSTRA FUNCTION -------------------
def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {start: 0}
    previous = {start: None}

    while queue:
        current_dist, current_node = heapq.heappop(queue)
        if current_node == end:
            break
        for neighbor, weight in graph.get(current_node, []):
            distance = current_dist + weight
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous.get(node)
    path.reverse()

    return path, distances.get(end, float('inf'))

# ------------------- GRAPH STORAGE -------------------
graph = {}

# ------------------- FUNCTIONS -------------------
def refresh_edge_list():
    edge_list.delete(*edge_list.get_children())
    seen = set()
    for a in graph:
        for b, w in graph[a]:
            if (b, a) not in seen:
                edge_list.insert("", "end", values=(a, b, w))
                seen.add((a, b))

def add_node():
    node = node_entry.get().strip()
    if not node:
        messagebox.showwarning("⚠ Warning", "Enter a node name!")
        return
    if node in graph:
        messagebox.showwarning("⚠ Warning", "Node already exists!")
        return
    graph[node] = []
    node_list.insert("", "end", values=(node,))
    node_entry.delete(0, tk.END)

def delete_node():
    node = node_entry.get().strip()
    if not node:
        messagebox.showwarning("⚠ Warning", "Enter a node name to delete!")
        return
    if node not in graph:
        messagebox.showwarning("⚠ Warning", "Node does not exist!")
        return

    del graph[node]
    for key in graph:
        graph[key] = [(n, w) for n, w in graph[key] if n != node]

    node_list.delete(*node_list.get_children())
    for n in graph.keys():
        node_list.insert("", "end", values=(n,))
    refresh_edge_list()
    node_entry.delete(0, tk.END)
    messagebox.showinfo("✅ Success", f"Node '{node}' deleted successfully.")

def add_edge():
    a, b, w = edge_from_entry.get().strip(), edge_to_entry.get().strip(), weight_entry.get().strip()
    if not (a and b and w):
        messagebox.showwarning("⚠ Warning", "Fill all edge fields!")
        return
    try:
        w = int(w)
    except:
        messagebox.showwarning("⚠ Warning", "Weight must be a number!")
        return
    if a not in graph or b not in graph:
        messagebox.showwarning("⚠ Warning", "Both nodes must exist!")
        return

    graph[a].append((b, w))
    graph[b].append((a, w))
    refresh_edge_list()
    edge_from_entry.delete(0, tk.END)
    edge_to_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)

def delete_edge():
    a, b = edge_from_entry.get().strip(), edge_to_entry.get().strip()
    if not (a and b):
        messagebox.showwarning("⚠ Warning", "Enter both node names!")
        return
    if a not in graph or b not in graph:
        messagebox.showwarning("⚠ Warning", "Both nodes must exist!")
        return
    before_a, before_b = len(graph[a]), len(graph[b])
    graph[a] = [(n, w) for n, w in graph[a] if n != b]
    graph[b] = [(n, w) for n, w in graph[b] if n != a]
    if len(graph[a]) < before_a or len(graph[b]) < before_b:
        refresh_edge_list()
        messagebox.showinfo("✅ Success", f"Edge between {a} and {b} deleted.")
    else:
        messagebox.showwarning("⚠ Warning", "Edge not found!")
    edge_from_entry.delete(0, tk.END)
    edge_to_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)

def find_path():
    start, end = start_entry.get().strip(), end_entry.get().strip()
    if not (start and end):
        messagebox.showwarning("⚠ Warning", "Enter both start and end nodes!")
        return
    if start not in graph or end not in graph:
        messagebox.showwarning("⚠ Warning", "Both nodes must exist!")
        return
    path, distance = dijkstra(graph, start, end)
    if distance == float('inf'):
        result_text.set("❌ No path found!")
    else:
        result_text.set(f"🚀 Shortest Path: {' → '.join(path)}\n📏 Distance: {distance}")

# ------------------- STYLING -------------------
root = tk.Tk()
root.title("🚀 Dijkstra Shortest Path Visualizer")
root.geometry("700x780")
root.config(bg="#eaf2f8")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, relief="flat", background="#3498db", foreground="white")
style.map("TButton", background=[("active", "#2980b9")])
style.configure("Treeview", background="white", fieldbackground="white", rowheight=25)
style.configure("TLabel", background="#eaf2f8", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"), background="#eaf2f8", foreground="#2c3e50")

# ------------------- UI ELEMENTS -------------------
title_label = ttk.Label(root, text="✨ Shortest Path Finder (Dijkstra’s Algorithm)", style="Header.TLabel")
title_label.pack(pady=10)

# NODE FRAME
frame_nodes = ttk.LabelFrame(root, text="🟢 Manage Nodes")
frame_nodes.pack(padx=15, pady=10, fill="x")

tk.Label(frame_nodes, text="Node Name:", bg="#eaf2f8").grid(row=0, column=0, padx=5, pady=5)
node_entry = ttk.Entry(frame_nodes, width=15)
node_entry.grid(row=0, column=1, padx=5)
ttk.Button(frame_nodes, text="Add Node", command=add_node).grid(row=0, column=2, padx=5)
ttk.Button(frame_nodes, text="Delete Node", command=delete_node).grid(row=0, column=3, padx=5)

node_list = ttk.Treeview(frame_nodes, columns=("Node",), show="headings", height=5)
node_list.heading("Node", text="Node Name")
node_list.grid(row=1, column=0, columnspan=4, pady=8, sticky="ew")

# EDGE FRAME
frame_edges = ttk.LabelFrame(root, text="🔵 Manage Edges")
frame_edges.pack(padx=15, pady=10, fill="x")

tk.Label(frame_edges, text="From:", bg="#eaf2f8").grid(row=0, column=0, pady=5)
edge_from_entry = ttk.Entry(frame_edges, width=10)
edge_from_entry.grid(row=0, column=1, pady=5)

tk.Label(frame_edges, text="To:", bg="#eaf2f8").grid(row=0, column=2)
edge_to_entry = ttk.Entry(frame_edges, width=10)
edge_to_entry.grid(row=0, column=3)

tk.Label(frame_edges, text="Weight:", bg="#eaf2f8").grid(row=0, column=4)
weight_entry = ttk.Entry(frame_edges, width=6)
weight_entry.grid(row=0, column=5)

ttk.Button(frame_edges, text="Add Edge", command=add_edge).grid(row=0, column=6, padx=5)
ttk.Button(frame_edges, text="Delete Edge", command=delete_edge).grid(row=0, column=7, padx=5)

edge_list = ttk.Treeview(frame_edges, columns=("From", "To", "Weight"), show="headings", height=6)
for col in ("From", "To", "Weight"):
    edge_list.heading(col, text=col)
edge_list.grid(row=1, column=0, columnspan=8, pady=8, sticky="ew")

# PATH FRAME
frame_path = ttk.LabelFrame(root, text="🟣 Find Shortest Path")
frame_path.pack(padx=15, pady=10, fill="x")

tk.Label(frame_path, text="Start:", bg="#eaf2f8").grid(row=0, column=0)
start_entry = ttk.Entry(frame_path, width=12)
start_entry.grid(row=0, column=1)

tk.Label(frame_path, text="End:", bg="#eaf2f8").grid(row=0, column=2)
end_entry = ttk.Entry(frame_path, width=12)
end_entry.grid(row=0, column=3)

ttk.Button(frame_path, text="Find Path", command=find_path).grid(row=0, column=4, padx=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Segoe UI", 11, "bold"), bg="#eaf2f8", fg="#2c3e50")
result_label.pack(pady=25)


root.mainloop()
