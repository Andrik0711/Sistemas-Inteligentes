from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QFrame
from PyQt5.QtGui import QPainter, QBrush, QFont, QColor, QPen, QPolygonF
from PyQt5.QtCore import Qt, QPoint
import sys
import json
import random



import matplotlib.pyplot as plt
import networkx as nx

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
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
        nx.draw_networkx_edges(graph, pos, edge_color='black', arrows=True, arrowstyle='->')
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

        # Dibujar los identificadores de los nodos
        node_labels = {node: node for node in graph.nodes}
        nx.draw_networkx_labels(graph, pos, labels=node_labels, font_color='black')

        # Actualizar el lienzo de la figura
        self.canvas.draw()


# class GraphWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.nodes = []
#         self.edges = []

#     def drawGraph(self, nodes, edges):
#         self.nodes = nodes
#         self.edges = edges
#         self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         painter.fillRect(event.rect(), Qt.white)

#         # Ajustar márgenes del área de dibujo
#         menu_margin_right = 200  # Ancho del menú derecho
#         layout_margin_right = 20  # Margen adicional para el layout principal

#         # Área para dibujar los nodos dentro del layout principal
#         area = self.parent().rect().adjusted(20, 20, -menu_margin_right - layout_margin_right, -20)

#         # Dibujar nodos
#         radius = 15  # Radio de los nodos (1.5 cm)
#         node_color = QColor(255, 0, 0)  # Color de los nodos (rojo)
#         # Color del texto (identificador) (azul)
#         text_color = QColor(0, 0, 255)

#         font = QFont("Arial", 12)

#         for node in self.nodes:
#             node_id = str(node.get("id"))

#             # Generar posiciones aleatorias dentro del área
#             x = random.randint(area.left() + radius, area.right() - radius)
#             y = random.randint(area.top() + radius, area.bottom() - radius)

#             # Dibujar nodo circular
#             node_center = QPoint(x, y)
#             painter.setPen(Qt.NoPen)  # No se dibuja la línea del nodo
#             painter.setBrush(node_color)
#             painter.drawEllipse(node_center, radius, radius)

#             # Dibujar identificador centrado en el nodo
#             painter.setPen(text_color)
#             painter.setFont(font)
#             text_rect = painter.fontMetrics().boundingRect(node_id)
#             text_width = text_rect.width()
#             text_height = text_rect.height()

#             # Posición del texto centrado en el nodo, aun no lo centra bien puede ser por el tamaño de la fuente
#             text_pos = node_center - QPoint(int(text_width / 2), int(text_height / 7   ))
#             painter.drawText(text_pos, node_id)

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

        # Establecer el widget central en la ventana principal
        self.setCentralWidget(central_widget)

    def find_button_clicked(self):
        # Lógica cuando se hace clic en el botón Find
        pass

    def reset_button_clicked(self):
        # Lógica cuando se hace clic en el botón Reset
        pass

    def new_graph_button_clicked(self):
        # Lógica cuando se hace clic en el botón New Graph
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

            # Imprimir los nodos y conexiones en la consola para verificar que si se cargaron correctamente
            # print(type(nodes))
            # print(type(edges))
            # print(nodes)
            # print(edges)
            # Dibujar los nodos y conexiones en el GraphWidget
            self.graph_widget.drawGraph(nodes, edges)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
