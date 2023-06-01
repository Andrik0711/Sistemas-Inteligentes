import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer, QEventLoop
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.graph = None
        self.tree_edges = None
        self.current_edge_index = 0
        self.node_positions = None
        self.completed = False

        self.setWindowTitle("Graph Viewer")
        self.setGeometry(100, 100, 800, 400)

        layout = QVBoxLayout()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)

        import_button = QPushButton("Import JSON")
        import_button.clicked.connect(self.import_json)
        layout.addWidget(import_button)

        self.find_button = QPushButton("Find Minimum Spanning Tree")
        self.find_button.clicked.connect(self.find_mst)
        layout.addWidget(self.find_button)

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
        file_path, _ = file_dialog.getOpenFileName(
            self, "Import JSON", "", "JSON Files (*.json)")

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
            self.graph.add_edge(
                edge["source"], edge["target"], weight=edge["weight"])

        self.node_positions = nx.spring_layout(self.graph)

        self.figure.clear()
        nx.draw(self.graph, with_labels=True,
                pos=self.node_positions, ax=self.figure.gca())
        self.canvas.draw()

    def find_mst(self):
        if self.graph is None:
            QMessageBox.warning(self, "Error", "No graph data available.")
            return

        if self.tree_edges is None:
            self.tree_edges = prim_mst(self.graph)
            self.current_edge_index = 0
            self.completed = False

        if self.completed:
            QMessageBox.information(
                self, "Completed", "Minimum Spanning Tree found.")
            return

        self.next_step()

    def next_step(self):
        if self.tree_edges is None:
            return

        if self.current_edge_index >= len(self.tree_edges):
            self.current_edge_index = len(self.tree_edges) - 1
            self.completed = True

            QMessageBox.information(
                self, "Completed", "Minimum Spanning Tree found.")
            return

        self.highlight_edges()

        self.current_edge_index += 1

        # Pausa de 3 segundos antes de la siguiente animación
        QTimer.singleShot(3000, self.next_step)

    def highlight_edges(self):
        if self.tree_edges is None:
            return

        self.figure.clear()

        nx.draw_networkx_nodes(
            self.graph, self.node_positions, node_color="gray", node_size=400)
        nx.draw_networkx_labels(self.graph, self.node_positions)
        nx.draw_networkx_edges(
            self.graph, self.node_positions, edge_color="black", width=1, arrows=True, arrowstyle="->")

        # Dibuja el peso de las aristas
        edge_labels = {}
        for source, target, data in self.graph.edges(data=True):
            edge_labels[(source, target)] = data["weight"]

        # Dibuja las etiquetas de las aristas
        nx.draw_networkx_edge_labels(
            self.graph, self.node_positions, edge_labels=edge_labels)

        # Dibuja las aristas del árbol de expansión mínima
        for i, edge in enumerate(self.tree_edges):
            if i <= self.current_edge_index:
                nx.draw_networkx_edges(self.graph, self.node_positions, edgelist=[
                                       edge], edge_color="blue", width=1, arrows=True, arrowstyle="->")

        # Dibuja los nodos del árbol de expansión mínima
        self.canvas.draw()

    # Reinicia la animación
    def reset_animation(self):
        if self.tree_edges is None:
            return

        self.current_edge_index = 0  # Reinicia el índice de la arista
        self.completed = False  # Reinicia la flag de completado
        self.highlight_edges()  # Dibuja el grafo original

    # Cierra la ventana
    def closeEvent(self, event):
        super().closeEvent(event)


def prim_mst(graph):
    tree_edges = []

    # Elegir un nodo arbitrario como nodo inicial
    start_node = list(graph.nodes)[0]

    # Conjunto de nodos ya visitados
    visited = set([start_node])

    while len(visited) < len(graph.nodes):
        min_edge = None
        min_weight = float('inf')

        # Buscar la arista de menor peso que conecta un nodo visitado con un nodo no visitado
        for source, target, data in graph.edges(data=True):
            if source in visited and target not in visited and data["weight"] < min_weight:
                min_edge = (source, target)
                min_weight = data["weight"]

        if min_edge is not None:
            tree_edges.append(min_edge)
            visited.add(min_edge[1])

    return tree_edges


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec_())
