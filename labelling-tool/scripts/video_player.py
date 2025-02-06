import cv2
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage, QKeyEvent
from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QMessageBox, QSizePolicy
)

class VideoPlayer(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.video_path = None
        self.cap = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        
        self.rewind_timer = QTimer()
        self.rewind_timer.timeout.connect(self.rewind_frame)
        self.rewind_speed = 50  

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
        self.video_path = path
        self.cap = cv2.VideoCapture(path)

        if not self.cap.isOpened():
            QMessageBox.warning(self, "Error", f"Failed to open video file from {path}")
            return

        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        ret, frame = self.cap.read()
        if ret:
            self.display_frame(frame)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            maximum_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.main_window.max_frame_label.setText(str(maximum_frames))

    def next_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)
                current_frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.main_window.current_frame_label.setText(str(current_frame_number))
            else:
                self.timer.stop()

    def rewind_frame(self):
        if self.cap and self.cap.isOpened():
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            if current_frame > 1:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, current_frame - 2))  
                ret, frame = self.cap.read()
                if ret:
                    self.display_frame(frame)
                    self.main_window.current_frame_label.setText(str(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))))
            else:
                self.rewind_timer.stop()

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        self.pixmap_item.setPixmap(pixmap)
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    def reset(self):
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def play(self):
        self.rewind_timer.stop()
        if self.cap and self.cap.isOpened():
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            if fps <= 0:
                fps = 30
            self.timer.start(1000 // fps)

    def pause(self):
        self.timer.stop()

    def rewind(self, speed=None):
        self.timer.stop()
        if speed:
            self.rewind_speed = speed
        self.rewind_timer.start(self.rewind_speed)

    '''def skip_back(self, frames=30):
        if self.cap and self.cap.isOpened():
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, current_frame - frames))
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)
                self.main_window.current_frame_label.setText(str(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))))'''
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Space:
            self.main_window.toogle_play()
        # elif event.key() == Qt.Key.Key_Left:
            #self.main_window.rewind() 
        # elif event.modifiers() == Qt.KeyboardModifier.ShiftModifier and event.key() == Qt.Key.Key_Left:
            # self.skip_back(frames=30) 