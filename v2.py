import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.graph = None
        self.tree_edges = None
        self.current_edge_index = 0
        self.node_positions = None
        self.completed = False
        self.paused = False

        self.setWindowTitle("Graph Viewer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)

        import_button = QPushButton("Import JSON")
        import_button.clicked.connect(self.import_json)
        layout.addWidget(import_button)

        self.run_button = QPushButton("Run Prim's Algorithm")
        self.run_button.clicked.connect(self.run_prim)
        layout.addWidget(self.run_button)

        self.pause_button = QPushButton("Pause/Resume")
        self.pause_button.clicked.connect(self.pause_resume_animation)
        layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_animation)
        layout.addWidget(self.reset_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)

    def import_json(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Import JSON", "", "JSON Files (*.json)")

        if file_path:
            try:
                with open(file_path, "r") as file:
                    json_data = json.load(file)
                    self.draw_graph(json_data)
            except (FileNotFoundError, json.JSONDecodeError):
                QMessageBox.warning(self, "Error", "Invalid JSON file.")
        else:
            QMessageBox.warning(self, "Error", "No file selected.")

    def draw_graph(self, json_data):
        self.graph = nx.Graph()

        for node in json_data["nodes"]:
            self.graph.add_node(node["id"])

        for edge in json_data["edges"]:
            self.graph.add_edge(edge["source"], edge["target"], distance=edge["distance"])

        self.node_positions = nx.spring_layout(self.graph)

        self.figure.clear()
        nx.draw(self.graph, with_labels=True, pos=self.node_positions, ax=self.figure.gca())
        self.canvas.draw()

    def run_prim(self):
        if self.graph is None:
            QMessageBox.warning(self, "Error", "No graph data available.")
            return

        if self.tree_edges is None:
            self.tree_edges = prim_mst(self.graph)
            self.current_edge_index = 0
            self.completed = False

        if self.completed:
            QMessageBox.information(self, "Completed", "Prim's algorithm traversal completed.")
            return

        self.highlight_edges()

        if not self.timer.isActive():
            self.timer.start(1000)  # Cambia el valor (en milisegundos) según tu preferencia para la velocidad de la animación

    def next_step(self):
        if self.tree_edges is None:
            return

        if self.paused or self.completed:
            return

        self.current_edge_index += 1

        if self.current_edge_index >= len(self.tree_edges):
            self.current_edge_index = len(self.tree_edges) - 1
            self.completed = True
            self.timer.stop()

        self.highlight_edges()

        if self.completed:
            QMessageBox.information(self, "Completed", "Prim's algorithm traversal completed.")

    def highlight_edges(self):
        if self.tree_edges is None:
            return

        self.figure.clear()

        nx.draw_networkx_nodes(self.graph, self.node_positions, node_color="lightblue", node_size=500)
        nx.draw_networkx_labels(self.graph, self.node_positions)
        nx.draw_networkx_edges(self.graph, self.node_positions, edge_color="gray")

        for i, edge in enumerate(self.tree_edges):
            if i <= self.current_edge_index:
                nx.draw_networkx_edges(self.graph, self.node_positions, edgelist=[edge], edge_color="green", width=2)

        self.canvas.draw()

    def pause_resume_animation(self):
        if self.tree_edges is None or self.completed:
            return

        if self.paused:
            self.paused = False
            self.timer.start()
        else:
            self.paused = True
            self.timer.stop()

    def reset_animation(self):
        if self.tree_edges is None:
            return

        self.current_edge_index = 0
        self.completed = False
        self.highlight_edges()
        self.timer.stop()

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)


def prim_mst(graph):
    tree_edges = []

    start_node = list(graph.nodes)[0]  # Comenzar desde el primer nodo

    visited_nodes = set([start_node])
    available_edges = list(graph.edges(start_node, data=True))

    while len(visited_nodes) < len(graph.nodes):
        min_edge = None
        min_distance = float("inf")

        for edge in available_edges:
            if edge[1] not in visited_nodes and edge[2]["distance"] < min_distance:
                min_edge = edge
                min_distance = edge[2]["distance"]

        if min_edge is not None:
            tree_edges.append(min_edge)
            visited_nodes.add(min_edge[1])
            available_edges.extend(graph.edges(min_edge[1], data=True))

        available_edges.remove(min_edge)

    return tree_edges


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec_())
