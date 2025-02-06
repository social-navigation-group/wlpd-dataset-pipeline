from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from video_player import VideoPlayer
from PyQt6.QtWidgets import (QMainWindow, QPushButton, QSlider, QVBoxLayout, QLabel,
                             QHBoxLayout, QWidget, QTextEdit, QFileDialog, QSplitter, QSizePolicy)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # LOAD EXTERNAL STYLESHEET
        self.load_stylesheet("styles.qss")

        # MAIN WINDOW
        self.setWindowTitle("Human Data Labeling")
        self.setFixedSize(1442, 1008)

        # MAIN WIDGET
        container = QWidget()
        main_layout = QVBoxLayout()

        # SPLITTER DIVIDING MEDIA AND LABELING CONTROLS
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # VIDEO PLAYER WIDGET
        self.video_player = VideoPlayer(self)

        # SLIDER & CONTROLS
        self.frame_slider = QSlider(Qt.Orientation.Horizontal)
        self.frame_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.frame_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.current_frame_label = QLabel() 
        self.current_frame_label.setText("0")

        self.max_frame_label = QLabel() 
        self.max_frame_label.setText("0")  

        # PLAYBACK BUTTONS
        self.rewind_button = QPushButton()
        self.rewind_button.setFixedSize(50, 22)
        self.rewind_button.setIcon(QIcon("../resources/icons/rewind/rewind-60.png"))
        self.rewind_button.clicked.connect(self.rewind)

        self.play_pause_button = QPushButton()
        self.play_pause_button.setFixedSize(50, 22)
        self.play_pause_button.setIcon(QIcon("../resources/icons/play/play-60.png"))
        self.play_pause_button.clicked.connect(self.toggle_play)

        self.upload_button = QPushButton()
        self.upload_button.setFixedSize(50, 22)
        self.upload_button.setIcon(QIcon("../resources/icons/upload/upload-60.png"))
        self.upload_button.clicked.connect(self.load_video)

        self.stop_button = QPushButton()
        self.stop_button.setFixedSize(50, 22)
        self.stop_button.setIcon(QIcon("../resources/icons/stop/stop-60.png"))

        self.forward_button = QPushButton()
        self.forward_button.setFixedSize(50, 22)
        self.forward_button.setIcon(QIcon("../resources/icons/fast-forward/forward-60.png"))

        # Arrange video controls
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.current_frame_label)
        slider_layout.addWidget(self.frame_slider)
        slider_layout.addWidget(self.max_frame_label)

        playback_controls = QHBoxLayout()
        playback_controls.addWidget(self.rewind_button)
        playback_controls.addWidget(self.play_pause_button)
        playback_controls.addWidget(self.stop_button)
        playback_controls.addWidget(self.forward_button)
        playback_controls.addWidget(self.upload_button)
        playback_controls.setAlignment(Qt.AlignmentFlag.AlignLeft)

        video_layout = QVBoxLayout()
        video_layout.addWidget(self.video_player)
        video_layout.addLayout(playback_controls)
        video_layout.addLayout(slider_layout)

        video_widget = QWidget()
        video_widget.setLayout(video_layout)

        # LABELING CONTROLS
        labeling_layout = QVBoxLayout()
        for label in ["Relabel", "Missing", "Break", "Join", "Delete", "Disentangle", "Undo"]:
            button = QPushButton(label)
            labeling_layout.addWidget(button)

        self.log_labeling = QTextEdit()
        self.log_labeling.setPlaceholderText("Log the labeling here if needed...")

        self.log_submit_button = QPushButton("Submit")

        labeling_layout.addWidget(self.log_labeling)
        labeling_layout.addWidget(self.log_submit_button)

        controls_widget = QWidget()
        controls_widget.setLayout(labeling_layout)

        main_splitter.addWidget(video_widget)
        main_splitter.addWidget(controls_widget)

        main_layout.addWidget(main_splitter)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.avi *.mp4)")
        if file_path:
            self.video_player.load_video(file_path)

    def toggle_play(self):
        if self.video_player.timer.isActive():
            self.video_player.pause()
            self.play_pause_button.setIcon(QIcon("../resources/icons/play/play-60.png"))
        else:
            self.video_player.play()
            self.play_pause_button.setIcon(QIcon("../resources/icons/pause/pause-60.png"))

    def rewind(self):
        self.video_player.rewind()

    def forward(self):
        self.video_player.next_frame()

    def slider_moved(self):
        # Functionality for slider interaction (to be implemented)
        pass

    def load_stylesheet(self, path):
        try:
            with open(path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Stylesheet {path} not found.")
