from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QFrame
import sys
import json
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MinimumSpanningTreeTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Crear una figura de Matplotlib y un lienzo de figura de Qt
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Agregar el lienzo al diseño vertical
        self.layout.addWidget(self.canvas)

    def drawGraph(self, nodes, edges):
        # Borrar el contenido de la figura antes de dibujar el grafo
        self.figure.clear()

        # Crear el grafo
        graph = nx.Graph()

        # Convertir los identificadores de nodos a cadenas
        nodes = [str(node.get("id")) for node in nodes]

        # Agregar los nodos al grafo
        graph.add_nodes_from(nodes)

        # Agregar las aristas al grafo y dibujar las conexiones con direcciones y pesos
        for edge in edges:
            source_node = str(edge.get("source"))
            target_node = str(edge.get("target"))
            weight = str(edge.get("weight", ""))

            # Agregar la arista al grafo
            graph.add_edge(source_node, target_node, weight=weight)

        # Dibujar los nodos en la figura
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue')

        # Dibujar las aristas (conexiones) en la figura con etiquetas de peso
        nx.draw_networkx_edges(
            graph, pos, edge_color='black', arrows=True, arrowstyle='->')
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

        # Dibujar los identificadores de los nodos
        node_labels = {node: node for node in graph.nodes}
        nx.draw_networkx_labels(
            graph, pos, labels=node_labels, font_color='black')

        # Actualizar el lienzo de la figura
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graph Viewer")
        self.setFixedSize(1000, 700)  # Tamaño fijo de la ventana principal

        # Crear el widget del gráfico
        self.graph_widget = MinimumSpanningTreeTab()

        # Crear los botones del menú lateral
        self.btn_find = QPushButton("Find")
        self.btn_reset = QPushButton("Reset")
        self.btn_new_graph = QPushButton("New Graph")

        # Conectar los botones a sus respectivas funciones
        self.btn_find.clicked.connect(self.find_button_clicked)
        self.btn_reset.clicked.connect(self.reset_button_clicked)
        self.btn_new_graph.clicked.connect(self.new_graph_button_clicked)

        # Crear el layout del menú lateral
        menu_layout = QVBoxLayout()
        # Márgenes del layout left, top, right, bottom
        menu_layout.setContentsMargins(1, 1, 1, 600)
        menu_layout.setSpacing(10)  # Espacio entre los botones
        menu_layout.addWidget(self.btn_find)
        menu_layout.addWidget(self.btn_reset)
        menu_layout.addWidget(self.btn_new_graph)

        # Crear el layout principal donde se mostrara el grafo
        main_layout = QHBoxLayout()
        # Uso de factor de estiramiento para auto ajustar el tamaño del widget del grafo
        main_layout.addWidget(self.graph_widget, 1)
        main_layout.addLayout(menu_layout)

        # Crear el widget central y establecer el layout principal
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Desactivar el botón "Reset" por defecto
        self.btn_reset.setEnabled(False)
        # Desactivar el botón "Find" por defecto
        self.btn_find.setEnabled(False)

        # Establecer el widget central en la ventana principal
        self.setCentralWidget(central_widget)

    def find_button_clicked(self):
        pass

    def reset_button_clicked(self):
        if self.graph_widget.figure.axes:  # Verificar si hay algún dibujo presente
            self.graph_widget.figure.clear()  # Borrar el contenido de la figura
            self.graph_widget.canvas.draw()  # Actualizar el lienzo de la figura
            self.btn_reset.setEnabled(False)  # Desactivar el botón "Reset"

    def new_graph_button_clicked(self):
        # Al momento de hacer clic se debe abrir la ventana de escritorio para que solo permita cargar archivos json

        options = QFileDialog.Options()
        # Utilizar el diálogo de PyQt en lugar del nativo del sistema
        options |= QFileDialog.DontUseNativeDialog

        file_filter = "JSON Files (*.json)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open JSON File", "", file_filter, options=options)

        if file_path:
            # Cargar el archivo JSON
            with open(file_path) as json_file:
                data = json.load(json_file)

            # Obtener nodos y aristas del archivo JSON
            nodes = data.get("nodes", [])
            edges = data.get("edges", [])

            # Dibujar los nodos y conexiones en el GraphWidget
            self.graph_widget.drawGraph(nodes, edges)

            self.btn_reset.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
