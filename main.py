import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QFrame
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), Qt.white)

        # Aquí puedes agregar la lógica para dibujar tu gráfico
        # Utiliza los métodos proporcionados por QPainter para dibujar líneas, formas, etc.
        # Puedes consultar la documentación de QPainter para obtener más información


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
            # Aquí puedes hacer algo con el archivo seleccionado, como cargarlo en el GraphWidget
            print("Archivo seleccionado:", file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
