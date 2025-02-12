from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
)

class TrajectoryControls(QWidget):
    def __init__(self, video_player, parent: QWidget):
        super().__init__(parent)

        self.video_player = video_player

        # SET THE CONTROLS IN THE LAYOUT
        self.setLayout(self.create_labeling_controls())

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

        if self.video_player:
            labeling_layout.addWidget(QLabel("Video Player Linked!"))

        return labeling_layout
