import cv2
from PyQt6.QtCore import Qt, QTimer
from playback_mode import PlaybackMode
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QMessageBox, QSizePolicy
)

class VideoPlayer(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.cap = None
        self.video_fps = 30  
        self.total_frames = 0  
        self.video_path = None
        self.main_window = main_window
        self.playback_mode = PlaybackMode.STOPPED

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.playback_speed = 1  # Default speed (1x for normal, -1 for rewind, 2x for fast-forward)

        # Graphics Scene
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.view.setMinimumSize(1092, 888)
        self.view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.view.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def load_video(self, path):
        """Loads the video file and initializes the UI elements."""
        if self.cap:
            self.cap.release()  

        self.video_path = path
        self.cap = cv2.VideoCapture(path)

        if not self.cap.isOpened():
            QMessageBox.warning(self, "Error", f"Failed to open video file from {path}")
            return

        self.video_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.main_window.max_frame_label.setText(str(self.total_frames))
        self.main_window.frame_slider.setRange(0, self.total_frames)

        self.show_frame_at(0)

    def update_frame(self):
        """Handles frame updates for play, rewind, and forward."""
        if not self.cap or not self.cap.isOpened():
            self.timer.stop()
            return

        current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

        if self.playback_mode == PlaybackMode.PLAYING:
            new_frame = min(self.total_frames - 1, current_frame + self.playback_speed)
        elif self.playback_mode == PlaybackMode.REWINDING:
            new_frame = max(0, current_frame - self.playback_speed)
        elif self.playback_mode == PlaybackMode.FORWARDING:
            new_frame = min(self.total_frames - 1, current_frame + self.playback_speed)
        else:
            self.timer.stop()
            return

        self.show_frame_at(new_frame)

        # Stop if at boundaries
        if new_frame == 0 or new_frame == self.total_frames - 1:
            self.timer.stop()
            self.playback_mode = PlaybackMode.STOPPED
            self.main_window.play_pause_button.setIcon(QIcon("../resources/icons/play/play-60.png"))

    def show_frame_at(self, frame_number):
        """Displays the frame at a given position."""
        if self.cap and self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)
                self.main_window.current_frame_label.setText(str(frame_number))
                self.main_window.frame_slider.setValue(frame_number)

    def display_frame(self, frame):
        """Converts the OpenCV frame to a QPixmap and displays it."""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        self.pixmap_item.setPixmap(pixmap)
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    def change_playback_mode(self, mode, speed=1):
        """Sets playback mode and adjusts timer settings."""
        if self.playback_mode == mode:
            self.pause()
            return
        
        self.playback_mode = mode
        self.playback_speed = speed

        if not self.timer.isActive():
            self.timer.start(1000 // self.video_fps)

    def stop(self):
        """Stops the video and resets to the first frame."""
        self.timer.stop()
        self.playback_mode = PlaybackMode.STOPPED
        if self.cap:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)
            if self.cap.isOpened():
                self.show_frame_at(0)

    def play(self):
        """Starts video playback."""
        self.change_playback_mode(PlaybackMode.PLAYING, speed=1)

    def pause(self):
        """Pauses playback."""
        self.timer.stop()
        self.playback_mode = PlaybackMode.STOPPED

    def rewind(self, speed=2):
        """Starts rewinding at the given speed."""
        self.change_playback_mode(PlaybackMode.REWINDING, speed=speed)

    def forward(self, speed=2):
        """Starts fast-forwarding at the given speed."""
        self.change_playback_mode(PlaybackMode.FORWARDING, speed=speed)
