import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from video_player import VideoPlayer
from playback_mode import PlaybackMode
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

        # UI COMPONENTS
        video_widget = self.create_video_controls()
        controls_widget = self.create_labeling_controls()

        main_splitter.addWidget(video_widget)
        main_splitter.addWidget(controls_widget)

        main_layout.addWidget(main_splitter)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_button(self, icon_path, callback, size=(50, 22)):
        """Helper function to create buttons with icons."""
        button = QPushButton()
        button.setFixedSize(*size)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    def create_video_controls(self):
        """Creates and returns the video control UI."""
        # PLAYBACK BUTTONS
        self.rewind_button = self.create_button("../resources/icons/rewind/rewind-60.png", self.toggle_to_rewind)
        self.play_pause_button = self.create_button("../resources/icons/play/play-60.png", self.toggle_to_play)
        self.stop_button = self.create_button("../resources/icons/stop/stop-60.png", self.toggle_to_stop)
        self.forward_button = self.create_button("../resources/icons/fast-forward/forward-60.png", self.toggle_to_forward)
        self.upload_button = self.create_button("../resources/icons/upload/upload-60.png", self.load_video)

        playback_controls = QHBoxLayout()
        for btn in [self.rewind_button, self.play_pause_button, self.stop_button, self.forward_button, self.upload_button]:
            playback_controls.addWidget(btn)
        playback_controls.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # FRAME SLIDER
        self.frame_slider = QSlider(Qt.Orientation.Horizontal)
        self.frame_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.frame_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.frame_slider.valueChanged.connect(self.slider_moved)

        self.current_frame_label = QLabel()
        self.current_frame_label.setText("0")
        self.max_frame_label = QLabel()
        self.max_frame_label.setText("0")

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.current_frame_label)
        slider_layout.addWidget(self.frame_slider)
        slider_layout.addWidget(self.max_frame_label)

        # VIDEO LAYOUT
        video_layout = QVBoxLayout()
        video_layout.addWidget(self.video_player)
        video_layout.addLayout(playback_controls)
        video_layout.addLayout(slider_layout)

        video_widget = QWidget()
        video_widget.setLayout(video_layout)

        return video_widget
    
    def create_labeling_controls(self):
        """Creates and returns the labeling control UI."""
        labeling_layout = QVBoxLayout()
        labels = ["Relabel", "Missing", "Break", "Join", "Delete", "Disentangle", "Undo"]
        buttons = [QPushButton(label) for label in labels]
        for button in buttons:
            labeling_layout.addWidget(button)

        self.log_labeling = QTextEdit()
        self.log_labeling.setPlaceholderText("Log the labeling here if needed...")
        self.log_submit_button = QPushButton()
        self.log_submit_button.setText("Submit")

        labeling_layout.addWidget(self.log_labeling)
        labeling_layout.addWidget(self.log_submit_button)

        controls_widget = QWidget()
        controls_widget.setLayout(labeling_layout)

        return controls_widget

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.avi *.mp4)")
        if file_path:
            self.video_player.load_video(file_path)
            self.frame_slider.setRange(0, int(self.video_player.cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    
    def toggle_to_play(self):
        """Toggles between play and pause, ensuring a single click pauses all playback modes."""
        if self.video_player.playback_mode in [PlaybackMode.PLAYING, PlaybackMode.REWINDING, PlaybackMode.FORWARDING]:
            self.video_player.pause()
            self.play_pause_button.setIcon(QIcon("../resources/icons/play/play-60.png"))
        else:
            self.video_player.play()
            self.play_pause_button.setIcon(QIcon("../resources/icons/pause/pause-60.png"))

    def toggle_to_rewind(self):
        """Toggles between rewind and stop."""
        if self.video_player.playback_mode == PlaybackMode.REWINDING:
            self.video_player.pause()
            self.play_pause_button.setIcon(QIcon("../resources/icons/play/play-60.png"))
        else:
            self.video_player.rewind()
            self.play_pause_button.setIcon(QIcon("../resources/icons/pause/pause-60.png"))

    def toggle_to_forward(self):
        """Toggles between fast forward and stop."""
        if self.video_player.playback_mode == PlaybackMode.FORWARDING:
            self.video_player.pause()
            self.play_pause_button.setIcon(QIcon("../resources/icons/play/play-60.png"))
        else:
            self.video_player.forward()
            self.play_pause_button.setIcon(QIcon("../resources/icons/pause/pause-60.png"))

    def toggle_to_stop(self):
        """Stops playback and resets to the first frame."""
        self.video_player.stop()
        self.play_pause_button.setIcon(QIcon("../resources/icons/play/play-60.png"))
        self.frame_slider.setValue(0)

    def slider_moved(self, position):
        """Handles manual frame seeking via the slider."""
        if self.video_player.cap and self.video_player.cap.isOpened():
            self.video_player.show_frame_at(position)
            self.current_frame_label.setText(str(position))
    
    def load_stylesheet(self, path):
        try:
            with open(path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Stylesheet {path} not found.")
