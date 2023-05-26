from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QFrame
from PyQt5.QtGui import QPainter, QBrush, QFont, QColor, QPen, QPolygonF
from PyQt5.QtCore import Qt, QPoint
from math import cos, sin, pi
from math import atan2
import sys
import json
import random


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.nodes = []
        self.edges = []

    def drawGraph(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), Qt.white)

        # Dibujar nodos
        radius = 15  # Radio de los nodos (1.5 cm)
        node_color = QColor(255, 0, 0)  # Color de los nodos (rojo)
        # Color del texto (identificador) (azul)
        text_color = QColor(0, 0, 255)
        # Color de la flecha (conexión) (verde)
        arrow_color = QColor(0, 255, 0)
        weight_color = QColor(255, 255, 0)  # Color del texto (peso) (amarillo)

        # Fuente del texto (Helvetica, tamaño 10)
        font = QFont("Helvetica", 10)

        for node in self.nodes:
            node_id = node.get("id")

            # Generar posiciones aleatorias dentro de main_layout
            x = random.randint(radius, self.parent().width() - radius * 2)
            y = random.randint(radius, self.parent().height() - radius * 2)

            # Dibujar nodo circular
            node_center = QPoint(x, y)
            painter.setBrush(node_color)
            painter.drawEllipse(node_center, radius, radius)

            # Dibujar identificador dentro del nodo
            painter.setPen(text_color)
            painter.setFont(font)
            text_width = painter.fontMetrics().boundingRect(str(node_id)).width()
            text_height = painter.fontMetrics().height()
            text_pos = node_center - \
                QPoint(int(int(text_width) / 2), int(int(text_height) / 2))
            painter.drawText(text_pos, str(node_id))

        # Dibujar aristas (conexiones)
        arrow_size = 15  # Tamaño de la flecha
        weight_offset = 20  # Desplazamiento del peso respecto a la flecha

        for edge in self.edges:
            source_id = edge.get("source")
            target_id = edge.get("target")
            weight = edge.get("weight")

            # Obtener las coordenadas de origen y destino de la arista
            source_node = next(
                (node for node in self.nodes if node.get("id") == source_id), None)
            target_node = next(
                (node for node in self.nodes if node.get("id") == target_id), None)

            if source_node and target_node:
                source_x = source_node.get("x", 0)
                source_y = source_node.get("y", 0)
                target_x = target_node.get("x", 0)
                target_y = target_node.get("y", 0)

                # Calcular los ángulos de inicio y fin de la flecha
                angle = atan2(target_y - source_y, target_x - source_x)
                angle_deg = angle * 180 / pi

                # Dibujar flecha
                painter.setPen(QPen(arrow_color, 2))
                painter.setBrush(arrow_color)
                painter.drawLine(source_x, source_y, target_x, target_y)
                painter.translate(target_x, target_y)
                painter.rotate(angle_deg)
                painter.drawPolygon(QPolygonF([
                    QPoint(0, 0),
                    QPoint(-int(arrow_size), int(int(arrow_size) / 2)),
                    QPoint(-int(arrow_size), int(-int(arrow_size) / 2))
                ]))

                # Dibujar peso
                painter.resetTransform()
                painter.setPen(weight_color)
                painter.setFont(font)
                weight_pos = QPoint(int((source_x + target_x) / 2),
                                    int((source_y + target_y) / 2))
                painter.drawText(
                    weight_pos + QPoint(weight_offset, 0), str(weight))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graph Viewer")
        self.setFixedSize(1000, 700)  # Tamaño fijo de la ventana principal

        # Crear el widget del gráfico
        self.graph_widget = GraphWidget()

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
            print(nodes)
            print(edges)
            # Dibujar los nodos y conexiones en el GraphWidget
            self.graph_widget.drawGraph(nodes, edges)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
