import cv2
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QImage, QPainter, QBrush
from PyQt6.QtWidgets import (QLabel, QVBoxLayout, QWidget, QMessageBox, QSizePolicy)

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.video_path = None
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

        self.frame_label = QLabel()
        self.frame_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_label.setScaledContents(False)
        self.frame_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.frame_label.setStyleSheet("border-radius: 8px; background-color: black;")

        layout = QVBoxLayout()
        layout.addWidget(self.frame_label)
        self.setLayout(layout)

    def load_video(self, path):
        self.video_path = path
        self.cap = cv2.VideoCapture(path)

        if not self.cap.isOpened():
            QMessageBox.warning(self, "Error", f"Failed to open video file from {path}")
            return

        # VIDEO DIMENSIONS
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # RESIZE QLABEL TO MAINTAIN VIDEO ASPECT RATIO
        self.update_display_size()

        # DISPLAY THUMBNAIL (FIRST FRAME)
        ret, frame = self.cap.read()
        if ret:
            self.display_frame(frame)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  

    def next_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)
            else:
                self.timer.stop()

    def display_frame(self, frame):
        """
        Converts a video frame to a QPixmap and applies a border-radius mask.
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        if self.frame_label.width() > 0 and self.frame_label.height() > 0:
            target_size = self.frame_label.size()
        else:
            target_size = QSize(self.video_width, self.video_height)  

        # SCALE PIXMAP WHILE MAINTAINING ASPECT RATIO
        # scaled_pixmap = pixmap.scaled(self.frame_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        scaled_pixmap = pixmap.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # APPLY BORDER RADIUS MASK
        mask = QPixmap(scaled_pixmap.size())
        # mask.fill(Qt.GlobalColor.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        # painter.setBrush(QBrush(Qt.GlobalColor.white))
        # painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(mask.rect(), 8, 8)
        print(f"{mask.rect()}")
        painter.end()

        scaled_pixmap.setMask(mask.createMaskFromColor(Qt.GlobalColor.transparent, Qt.MaskMode.MaskInColor))
        self.frame_label.setPixmap(scaled_pixmap)

    def update_display_size(self):
        """ Resizes the QLabel to fit the aspect ratio while maintaining the set width. """
        if not hasattr(self, "video_width") or self.video_width == 0:
            return  

        container_width = self.width()
        aspect_ratio = self.video_width / self.video_height
        adjusted_height = int(container_width / aspect_ratio)
        self.frame_label.setFixedSize(container_width, adjusted_height)

    def reset(self):
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def play(self):
        if self.cap and self.cap.isOpened():
            fps = int(self.cap.get(cv2.CAP_PROP_FPS)) 
            if fps <= 0: 
                fps = 30 
            self.timer.start(1000 // fps)

    def pause(self):
        self.timer.stop()
    
    