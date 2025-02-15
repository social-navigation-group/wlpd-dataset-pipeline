from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit
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

        for i in range(2):
            labeling_layout.insertWidget(2 * i, QLabel(f"Trajectory {i + 1}"))
            trajectory_input = QLineEdit()
            trajectory_input.returnPressed.connect(self.on_enter_pressed)
            labeling_layout.insertWidget(2 * i + 1, trajectory_input)

        return labeling_layout
    
    def create_trajID_input(self, labeling_layout, numLayout):
        for i in range(numLayout):
            labeling_layout.insertWidget(2 * i, QLabel(f"Trajectory {i + 1}"))
            trajectory_input = QLineEdit()
            trajectory_input.returnPressed.connect(self.on_enter_pressed)
            labeling_layout.insertWidget(2 * i + 1, trajectory_input)

        return labeling_layout
    
    def delete_trajID_input(self, labeling_layout, numLayout):
        for i in range(numLayout):
            for j in range(2):
                index_to_remove = 2 * i + j
                item = labeling_layout.itemAt(index_to_remove)
                
                if item is not None:
                    widget = item.widget()
                    labeling_layout.removeWidget(widget)
                    widget.deleteLater()

        return labeling_layout
    
    def on_enter_pressed(self):
        line_edit_now = self.sender()
        traj_ID = int(line_edit_now.text())

        print("traj_ID:", traj_ID)