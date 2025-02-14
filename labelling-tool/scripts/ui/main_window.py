import os
from PyQt6.QtCore import Qt
from .tab_dialog import TabDialog
from .video_controls import VideoControls
from utils.file_utils import list_video_files
from utils.logging_utils import log_info, log_warning
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSplitter
import toml

class MainWindow(QMainWindow):
    def __init__(self, resources_path: str):
        super().__init__()

        # LOAD EXTERNAL STYLESHEET
        stylesheet_path = os.path.join(resources_path, "styles.qss")
        self.load_stylesheet(stylesheet_path)

        # MAIN WINDOW
        self.setWindowTitle("Human Data Labeling")
        self.setFixedSize(1642, 1008)

        # MAIN WIDGET
        container = QWidget()
        main_layout = QVBoxLayout()

        # SPLITTER DIVIDING MEDIA AND LABELING CONTROLS
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # UI COMPONENTS
        self.video_controls = VideoControls(resources_path)
        self.tab_dialog = TabDialog(self.video_controls)

        main_splitter.addWidget(self.video_controls)
        main_splitter.addWidget(self.tab_dialog)

        main_layout.addWidget(main_splitter)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # AUTOLOAD LAST USED VIDEO
        self.load_last_video(resources_path)

        human_config_path = os.path.join(resources_path, "config", "human_config.toml")
        self.load_human_config(human_config_path)

    def load_last_video(self, resources_path):
        """Loads the last available video in the directory."""
        videos_path = os.path.join(resources_path, "videos")
        video_files = list_video_files(videos_path)

        if video_files:
            last_video = video_files[-1] 
            video_path = f"{videos_path}/{last_video}"
            log_info(f"Auto-loading last video: {video_path}")
            self.video_controls.get_video_player().load_video(video_path)
        else:
            log_info("No video files found for auto-load.")

    def load_stylesheet(self, path):
        try:
            with open(path, "r") as f:
                self.setStyleSheet(f.read())
                log_info(f"Loaded stylesheet: {path}")
        except FileNotFoundError:
            log_warning(f"Stylesheet {path} not found.")

    def load_human_config(self, path):
        try:
            with open(path, "r") as f:
                self.human_config = toml.load(f)
        
        except FileNotFoundError:
            log_warning(f"Human Config file {path} not found.")
