from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from scripts.old.video_player import VideoPlayer
from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, QSlider, QVBoxLayout, 
                             QHBoxLayout, QWidget, QTextEdit, QFileDialog, QSplitter, QSizePolicy)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # MAIN WINDOW
        self.setWindowTitle("Human Data Labeling")
        self.setFixedSize(1442, 1008)

        # MAIN WIDGET
        container = QWidget()

        # MAIN LAYOUT HOLDING THE SPLITTER 
        main_layout = QVBoxLayout()

        # SPLITTER DIVIDING THE MEDIA, AND THE LABELING RELATED CONTROLS
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setHandleWidth(0)

        # WIDGET HOLDING MEDIA LAYOUTS
        video_widget = QWidget()

        # LAYOUT HOLDING PLAYER
        video_layout = QVBoxLayout()

        # VIDEO PLAYER
        self.video_player = VideoPlayer()
        self.video_player.setFixedSize(1156, 866)

        # ADDING THE PLAYER TO THE LAYOUT
        video_layout.addWidget(self.video_player)

        # SLIDER RELATED LAYOUT
        slider_layout = QHBoxLayout()
        slider_layout.setAlignment(Qt.AlignmentFlag.AlignLeft) 

        # SLIDER WIDGET
        self.frame_slider = QSlider(Qt.Orientation.Horizontal)
        self.frame_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.frame_slider.setEnabled(True)
        self.frame_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # CURRENT FRAME LABEL
        self.current_frame_label = QLabel()
        self.current_frame_label.setText("0")
        self.current_frame_label.setFixedSize(50, 20)
        self.current_frame_label.setStyleSheet("border: 2px solid black;")

        # MAX FRAME LABEL
        self.max_frame_label = QLabel()
        self.max_frame_label.setText("000")
        self.max_frame_label.setFixedSize(50, 20)
        self.max_frame_label.setStyleSheet("border: 2px solid black;")

        # Ensure the total width of the layout matches the video player width
        self.frame_slider.setFixedWidth(self.video_player.width() - (self.current_frame_label.width() + self.max_frame_label.width() + slider_layout.spacing()))

        # ADD SLIDER WIDGETS TO LAYOUT 
        slider_layout.addWidget(self.current_frame_label)
        slider_layout.addWidget(self.frame_slider)
        slider_layout.addWidget(self.max_frame_label)

        # PLAYBACK WIDGETS
        playback_controls = QHBoxLayout()
        playback_controls.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # PLAYBACK BUTTONS
        self.rewind_button = QPushButton()
        self.rewind_button.setFixedSize(50, 22)
        self.rewind_button.setIcon(QIcon("../resources/icons/rewind/rewind-60.png"))

        self.play_pause_button = QPushButton()
        self.play_pause_button.setFixedSize(50, 22)
        self.play_pause_button.setIcon(QIcon("../resources/icons/play/play-60.png"))
        self.play_pause_button.clicked.connect(self.toggle_play)

        self.stop_button = QPushButton()
        self.stop_button.setFixedSize(50, 22)
        self.stop_button.setIcon(QIcon("../resources/icons/stop/stop-60.png"))

        self.forward_button = QPushButton()
        self.forward_button.setFixedSize(50, 22)
        self.forward_button.setIcon(QIcon("../resources/icons/fast-forward/forward-60.png"))

        self.upload_button = QPushButton()
        self.upload_button.setFixedSize(50, 22)
        self.upload_button.setIcon(QIcon("../resources/icons/upload/upload-60.png"))
        self.upload_button.clicked.connect(self.load_video)

        # ADD THE PLAYBACK BUTTONS TO THE LAYOUT
        playback_controls.addWidget(self.rewind_button)
        playback_controls.addWidget(self.play_pause_button)
        playback_controls.addWidget(self.stop_button)
        playback_controls.addWidget(self.forward_button)
        playback_controls.addWidget(self.upload_button)

        # INCLUDE ALL LEFT SIDE LAYOUTS INTO ONE
        combined_layout = QVBoxLayout(video_widget) 
        combined_layout.addLayout(video_layout)  
        combined_layout.addLayout(playback_controls)
        combined_layout.addLayout(slider_layout) 

        # ADD THE VIDEO RELATED LAYOUTS TO THE WIDGET
        video_widget.setLayout(combined_layout)  

        # LAYOUT HOLDING THE LABELING CONTROLS
        labeling_layout = QVBoxLayout()

        self.relabel_trajectory_button = QPushButton()
        self.relabel_trajectory_button.setText("Relabel")

        self.missing_trajectory_button = QPushButton()
        self.missing_trajectory_button.setText("Missing")

        self.break_trajectory_button = QPushButton()
        self.break_trajectory_button.setText("Break")

        self.join_trajectory_button = QPushButton()
        self.join_trajectory_button.setText("Join")

        self.delete_trajectory_button = QPushButton()
        self.delete_trajectory_button.setText("Delete")

        self.disentangle_trajectory_button = QPushButton()
        self.disentangle_trajectory_button.setText("Disentangle")

        self.undo_trajectory_button = QPushButton()
        self.undo_trajectory_button.setText("Undo")

        self.log_labeling = QTextEdit()
        self.log_labeling.setPlaceholderText("Log the labeling here if needed...")

        self.log_submit_button = QPushButton()
        self.log_submit_button.setText("Submit")

        # WIDGETS - BUTTONS, TEXT-FIELDS, ETC... RELATED TO THE LABELING
        labeling_layout.addWidget(self.relabel_trajectory_button)
        labeling_layout.addWidget(self.missing_trajectory_button)
        labeling_layout.addWidget(self.break_trajectory_button)
        labeling_layout.addWidget(self.join_trajectory_button)
        labeling_layout.addWidget(self.delete_trajectory_button)
        labeling_layout.addWidget(self.disentangle_trajectory_button)
        labeling_layout.addWidget(self.undo_trajectory_button)
        labeling_layout.addWidget(self.log_labeling)
        labeling_layout.addWidget(self.log_submit_button)

        # Create two widgets to hold layouts
        controls_widget = QWidget()
        controls_widget.setLayout(labeling_layout)

        # ADD HOLDING WIDGET CONTAINERS TO THE SPLITTER
        main_splitter.addWidget(video_widget)
        main_splitter.addWidget(controls_widget)

        # ADDING THE SPLITTER TO THE LAYOUT
        main_layout.addWidget(main_splitter)
        
        # ADDING THE MAIN LAYOUT TO THE MAIN CONTAINER + INCLUDE IT TO THE WINDOW
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
        self.video_player.reset()

    def forward(self):
        self.video_player.next_frame()

    def slider_moved(self):
        # Functionality for slider interaction (to be implemented)
        pass