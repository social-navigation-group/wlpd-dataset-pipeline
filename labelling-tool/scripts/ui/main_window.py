import os
import toml
import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from .tab_dialog import TabDialog
from .video_controls import VideoControls
from utils.logging_utils import log_info, log_warning
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSplitter, QFileDialog, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, resource_manager: str):
        super().__init__()
        self.resource_manager = resource_manager

        # LOAD EXTERNAL STYLESHEET
        self.load_stylesheet(self.resource_manager.get_stylesheet())

        # MAIN WINDOW
        self.setWindowTitle("Human Data Labeling")
        self.setFixedSize(1642, 1008)

        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        
        save_action = QAction("Save Progress", self)
        save_action.triggered.connect(self.save_progress)
        file_menu.addAction(save_action)

        # MAIN WIDGET
        container = QWidget()
        main_layout = QVBoxLayout()

        # SPLITTER DIVIDING MEDIA AND LABELING CONTROLS
        main_splitter = QSplitter(Qt.Orientation.Horizontal, self)

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
    
    def save_progress(self):
        """Opens a file dialog to allow user to specify a save filename"""
        
        # Ensure the save directory exists
        save_dir = "saved_modified_trajectories"
        save_path = os.path.join(self.resource_manager.config_path, save_dir)
        os.makedirs(save_path, exist_ok = True)
        
        # Generate the default filename
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y_%m_%d_-_%H:%M")
        sanitized_video_filename = os.path.splitext(os.path.basename(self.resource_manager.video_name))[0]
        default_filename = f"{timestamp}_-_{sanitized_video_filename}.toml"
        default_filepath = os.path.join(save_path, default_filename)

        # Open a file dialog for the user to choose a filename
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilters(["TOML Files (*.toml)", "All Files (*)"])
        file_dialog.setDefaultSuffix("toml")
        
        file_dialog.selectFile(default_filepath)
        
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            
            if file_path:  
                try:
                    self.save_modified_trajectories(
                        self.video_controls.video_player.trajectory_manager,
                        self.video_controls.video_player.human_config,
                        file_path
                    )
                    QMessageBox.information(self, "Success", f"File saved to {file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {e}")


    def save_modified_trajectories(self, trajectory_manager, human_config, filepath):
        """Save the modified trajectory data to a TOML file."""
        data = {}
        
        for human_id, traj_start in trajectory_manager.traj_starts.items():
            trajectories = trajectory_manager.trajectories.get(human_id, [])
            
            data[f"human{human_id}"] = {
                "traj_start": traj_start,
                "trajectories": trajectories,
                "human_context": human_config.get_element(human_id, "human_context")
            }
        
        with open(filepath, "w") as file:
            toml.dump(data, file)
        
        print(f"Modified trajectories saved to {filepath}")