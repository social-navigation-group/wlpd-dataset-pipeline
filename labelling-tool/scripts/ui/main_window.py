from PyQt6.QtCore import Qt
from .tab_dialog import TabDialog
from .video_controls import VideoControls
from utils.logging_utils import log_info, log_warning
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSplitter

class MainWindow(QMainWindow):
    def __init__(self, resource_manager: str):
        super().__init__()
        self.resource_manager = resource_manager

        # LOAD EXTERNAL STYLESHEET
        self.load_stylesheet(self.resource_manager.get_stylesheet())

        # MAIN WINDOW
        self.setWindowTitle("Human Data Labeling")
        self.setFixedSize(1642, 1008)

        # MAIN WIDGET
        container = QWidget()
        main_layout = QVBoxLayout()

        # SPLITTER DIVIDING MEDIA AND LABELING CONTROLS
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # UI COMPONENTS
        self.video_controls = VideoControls(self.resource_manager)
        self.tab_dialog = TabDialog(self.video_controls)

        main_splitter.addWidget(self.video_controls)
        main_splitter.addWidget(self.tab_dialog)

        main_layout.addWidget(main_splitter)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_stylesheet(self, path):
        try:
            with open(path, "r") as f:
                self.setStyleSheet(f.read())
                log_info(f"Loaded stylesheet: {path}")
        except FileNotFoundError:
            log_warning(f"Stylesheet {path} not found.")
