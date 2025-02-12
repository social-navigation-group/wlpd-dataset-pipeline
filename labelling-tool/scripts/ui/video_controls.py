import os
import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from utils.logging_utils import log_info
from utils.file_utils import list_video_files
from video_proc_comps.video_player import VideoPlayer
from video_proc_comps.playback_mode import PlaybackMode
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QSlider, QSizePolicy, QLabel, QVBoxLayout, QComboBox
)

class VideoControls(QWidget):
    def __init__(self, resources_path: str):
        super().__init__()

       # VIDEO PLAYER WIDGET
        self.video_player = VideoPlayer(self)

        # VIDEO FILE DROPDOWN
        self.video_dropdown = QComboBox()
        self.populate_video_list(resources_path)

        # SET THE CONTROLS IN THE LAYOUT
        self.setLayout(self.create_video_controls(resources_path))

    def populate_video_list(self, resources_path):
        """Scans the default directory and populates the dropdown with available videos."""
        videos_path = os.path.join(resources_path, "videos")
        video_files = list_video_files(videos_path)

        if not video_files:
            log_info("No video files found in the directory.")
            self.video_dropdown.addItem("No videos found")
        else:
            log_info(f"Found {len(video_files)} video files in {videos_path}")
            self.video_dropdown.addItems(video_files)

    def create_button(self, icon_path, callback, size=(50, 22)):
        """Helper function to create buttons with icons."""
        button = QPushButton()
        button.setFixedSize(*size)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    def create_video_controls(self, resources_path):
        """Creates and returns the video control UI."""

        # PLAYBACK BUTTONS
        self.rewind_button = self.create_button("../resources/icons/rewind/rewind-60.png", self.toggle_to_rewind)
        self.play_pause_button = self.create_button("../resources/icons/play/play-60.png", self.toggle_to_play)
        self.stop_button = self.create_button("../resources/icons/stop/stop-60.png", self.toggle_to_stop)
        self.forward_button = self.create_button("../resources/icons/fast-forward/forward-60.png", self.toggle_to_forward)
        self.upload_button = self.create_button("../resources/icons/upload/upload-60.png", lambda: self.load_video(resources_path))

        playback_controls = QHBoxLayout()
        for btn in [self.rewind_button, self.play_pause_button, self.stop_button, self.forward_button, self.video_dropdown, self.upload_button]:
            playback_controls.addWidget(btn)
            if btn == self.forward_button:
                playback_controls.addStretch(1)

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

        return video_layout
    
    def load_video(self, resources_path):
        """Loads the selected video from the dropdown."""
        selected_video = self.video_dropdown.currentText()
        if selected_video and selected_video != "No videos found":
            video_path = os.path.join(resources_path, "videos", selected_video)
            log_info(f"User selected video file: {video_path}")
            self.video_player.load_video(video_path)
            self.frame_slider.setRange(0, int(self.video_player.cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    
    def toggle_to_play(self):
        """Toggles between play and pause, ensuring a single click pauses all playback modes."""
        if self.video_player.playback_mode in [PlaybackMode.PLAYING, PlaybackMode.REWINDING, PlaybackMode.FORWARDING]:
            log_info("Video playback paused")
            self.video_player.pause()
            self.play_pause_button.setIcon(QIcon("../resources/icons/play/play-60.png"))
        else:
            log_info("Video playback started")
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

    def get_video_player(self):
        return self.video_player
