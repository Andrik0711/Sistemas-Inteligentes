import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.graph = None
        self.tree_edges = None
        self.current_edge_index = 0
        self.node_positions = None
        self.completed = False

        self.AlgorithmPrim = AlgorithPrim()

        self.setWindowTitle(
            "Simulación de Algoritmo de Prim con Interfaz Gráfica")
        self.setFixedSize(1000, 700)  # tamaño fijo de la ventana

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # layour principal para el grafo
        main_layout = QHBoxLayout()

        # creación del layout para los botones
        menu_layout = QVBoxLayout()

        # alineación de los botones
        menu_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        # creación de los botones
        import_button = QPushButton("New Graph")
        self.find_button = QPushButton("Find MST Prim")
        self.reset_button = QPushButton("Reiniciar")
        self.clear_button = QPushButton("Limpiar")

        # conectar los botones con las funciones
        import_button.clicked.connect(self.import_json)
        self.find_button.clicked.connect(self.find_mst)
        self.reset_button.clicked.connect(self.reset_animation)
        self.clear_button.clicked.connect(self.clear_graph)

        menu_layout.addWidget(import_button)
        menu_layout.addWidget(self.find_button)
        menu_layout.addWidget(self.reset_button)
        menu_layout.addWidget(self.clear_button)

        main_layout.addWidget(self.canvas, 1)

        # agregar el layout de los botones al layout principal
        main_layout.addLayout(menu_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
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
        self.graph = nx.Graph()  # crea un grafo vacio

        # agrega los nodos al grafo creado
        for node in json_data["nodes"]:
            self.graph.add_node(node["id"])

        # agrega las aristas al grafo creado
        for edge in json_data["edges"]:
            #  agrega las aristas con su peso al grafo
            self.graph.add_edge(
                edge["source"], edge["target"], weight=edge["weight"])

        self.node_positions = nx.spring_layout(
            self.graph)  # posiciona los nodos en el grafo

        # limpia el grafo que fue cargado previamente
        self.figure.clear()

        # dibuja los nodos del grafo
        nx.draw(self.graph, with_labels=True,
                pos=self.node_positions, ax=self.figure.gca())

        # dibuja el grafo
        self.canvas.draw()

    def find_mst(self):
        # Si el grafo no está cargado, no hace nada
        if self.graph is None:
            QMessageBox.warning(self, "Error", "Datos del grafo no validos")
            return

        # Si el árbol de expansión mínima no ha sido calculado, se calcula
        if self.tree_edges is None:
            self.tree_edges = AlgorithPrim.prim_mst(self.graph)
            self.current_edge_index = 0
            self.completed = False

        # Si el árbol de expansión mínima ya fue calculado, se detiene la animación
        if self.completed:
            QMessageBox.information(
                self, "Listo", "Minimum Spanning Tree encontrado.")
            return

        self.next_step()

    def next_step(self):
        # Si el grafo no está cargado, no hace nada
        if self.tree_edges is None:
            return

        # Si el índice de la arista actual es mayor o igual al número de aristas del árbol, se detiene la animación
        if self.current_edge_index >= len(self.tree_edges):
            # Se asegura de que el índice de la arista actual no sea mayor al número de aristas del árbol
            self.current_edge_index = len(self.tree_edges) - 1
            self.completed = True

            QMessageBox.information(
                self, "Listo", "Minimum Spanning Tree encontrado.")
            return

        # Colorea las aristas del árbol de expansión mínima
        self.highlight_edges()
        self.current_edge_index += 1

        # Pausa de 3 segundos antes de la siguiente animación
        QTimer.singleShot(6000, self.next_step)

    def highlight_edges(self):
        # Si el grafo no está cargado, no hace nada
        if self.tree_edges is None:
            return

        # Limpia el grafo que fue cargado previamente
        self.figure.clear()

        # Colorea los nodos del grafo
        node_colors = ["gray" for _ in range(len(self.graph.nodes))]

        # Colorea los nodos que están en el grafo
        for i, edge in enumerate(self.tree_edges):
            if i <= self.current_edge_index:  # Si la arista está en el árbol de expansión mínima
                source, target = edge
                # Colorea el nodo fuente de rojo
                node_colors[list(self.graph.nodes).index(source)] = "red"
                # Colorea el nodo destino de azul
                node_colors[list(self.graph.nodes).index(target)] = "blue"

        nx.draw_networkx_nodes(
            self.graph, self.node_positions, node_color=node_colors, node_size=400)  # Dibuja los nodos
        # Dibuja las etiquetas de los nodos
        nx.draw_networkx_labels(self.graph, self.node_positions)
        nx.draw_networkx_edges(
            self.graph, self.node_positions, edge_color="black", width=1, arrows=True, arrowstyle="->")  # Dibuja las aristas

        # Dibuja el peso de las aristas
        edge_labels = {}
        for source, target, data in self.graph.edges(data=True):
            edge_labels[(source, target)] = data["weight"]

        # Dibuja las etiquetas de las aristas
        nx.draw_networkx_edge_labels(
            self.graph, self.node_positions, edge_labels=edge_labels)

        # Dibuja las aristas del árbol de expansión mínima que ya fueron recorridas
        for i, edge in enumerate(self.tree_edges):
            if i <= self.current_edge_index:
                nx.draw_networkx_edges(self.graph, self.node_positions, edgelist=[
                                       edge], edge_color="blue", width=1, arrows=True, arrowstyle="->")

        # Dibuja los nodos del árbol de expansión mínima
        self.canvas.draw()

    # Reinicia la animación del algoritmo
    def reset_animation(self):
        if self.tree_edges is None:
            return

        self.current_edge_index = 0  # Reinicia el índice de la arista
        self.completed = False  # Reinicia la flag de completado
        self.highlight_edges()  # Dibuja el grafo original

    # limpiar el grafo
    def clear_graph(self):
        self.graph = None
        self.tree_edges = None
        self.current_edge_index = 0
        self.node_positions = None
        self.completed = False
        self.figure.clear()
        self.canvas.draw()

    # # Cierra la ventana
    # def closeEvent(self, event):
    #     super().closeEvent(event)


class AlgorithPrim(QWidget):
    def __init__(self):
        pass

    def prim_mst(graph):
        tree_edges = []

        # Elegir un nodo arbitrario como nodo inicial
        start_node = list(graph.nodes)[0]

        # Conjunto de nodos ya visitados
        visited = set([start_node])

        # Itera hasta que todos los nodos estén visitados
        while len(visited) < len(graph.nodes):
            min_edge = None
            min_weight = float('inf')

            # Buscar la arista de menor peso que conecta un nodo visitado con un nodo no visitado
            for source, target, data in graph.edges(data=True):
                if source in visited and target not in visited and data["weight"] < min_weight:
                    min_edge = (source, target)
                    min_weight = data["weight"]

            # Agregar la arista de menor peso encontrada al árbol
            if min_edge is not None:
                tree_edges.append(min_edge)
                visited.add(min_edge[1])

        return tree_edges


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec_())
