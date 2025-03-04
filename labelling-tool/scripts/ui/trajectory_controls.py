from video_proc_comps.button_controller import ButtonController
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QGroupBox, QLayout
)

class TrajectoryControls(QWidget):
    def __init__(self, video_player, parent: QWidget):
        super().__init__(parent)
        self.video_player = video_player
        self.is_traj_input_visible = False
        self.button_controller = ButtonController(self)

        # SET THE CONTROLS IN THE LAYOUT
        self.labeling_layout = self.create_labeling_controls()
        self.setLayout(self.labeling_layout)
        
    def create_labeling_controls(self):
        """Creates and returns the labeling control UI."""

        traj_edit_group = QGroupBox("Trajectory Editing: ")
        traj_edit_layout = QVBoxLayout()

        labels = ["Relabel", "Missing", "Break", "Join", "Delete", "Disentangle", "Undo"]
        self.buttons = [QPushButton(label) for label in labels]
        for label, button in zip(labels, self.buttons):
            button.clicked.connect(getattr(self.button_controller, f"on_{label.lower()}_clicked"))
            traj_edit_layout.addWidget(button)

        traj_edit_group.setLayout(traj_edit_layout)

        self.log_labeling = QTextEdit()
        self.log_labeling.setPlaceholderText("Log the labeling here if needed...")
        self.log_submit_button = QPushButton()
        self.log_submit_button.setText("Submit")

        traj_log_group = QGroupBox()
        traj_log_layout = QVBoxLayout()

        log_labeling = QTextEdit()
        log_labeling.setPlaceholderText("Log the labeling here if needed...")
        log_submit_button = QPushButton()
        log_submit_button.setText("Submit")

        traj_log_layout.addWidget(log_labeling)
        traj_log_layout.addWidget(log_submit_button)
        traj_log_group.setLayout(traj_log_layout)

        labeling_layout = QVBoxLayout()
        labeling_layout.addWidget(traj_edit_group)
        labeling_layout.addWidget(traj_log_group)

        return labeling_layout
    
    def create_trajID_input(self, labeling_layout, number, mode):
        self.delete_trajID_input(self.labeling_layout, mode)

        if mode in [2, 7]:
            self.create_apply_button(labeling_layout, 0)
            self.create_cancel_button(labeling_layout, 1)
            self.is_traj_input_visible = True
            return labeling_layout
        
        labeling_layout.insertWidget(0, QLabel(f"Trajectory {number}"))
        horizontal_layout = QHBoxLayout()

        trajectory_input = QLineEdit()
        horizontal_layout.addWidget(trajectory_input)
        
        self.select_button = QPushButton("Select")
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
            }

            QPushButton:disabled {
                background-color: lightgray;
            }
        """)

        self.select_button.clicked.connect(self.button_controller.on_select_pressed)
        horizontal_layout.addWidget(self.select_button)
        labeling_layout.insertLayout(1, horizontal_layout)

        self.create_apply_button(labeling_layout, 2)
        self.create_cancel_button(labeling_layout, 3)
        
        self.is_traj_input_visible = True
        return labeling_layout
    
    def create_apply_button(self, labeling_layout, widget_position):
        self.apply_button = QPushButton("Apply")
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: green;
            }

            QPushButton:disabled {
                background-color: lightgray;
            }
        """)
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.button_controller.on_apply_pressed)
        labeling_layout.insertWidget(widget_position, self.apply_button)
    
    def create_cancel_button(self, labeling_layout, widget_position):
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("background-color: red;")
        self.cancel_button.clicked.connect(self.button_controller.on_cancel_pressed)
        labeling_layout.insertWidget(widget_position, self.cancel_button)
    
    def delete_trajID_input(self, labeling_layout, mode):
        if self.is_traj_input_visible is False: 
            return labeling_layout

        if mode == 2:
            number_of_widgets = 2
            self.delete_widgets(labeling_layout, number_of_widgets)
            self.is_traj_input_visible = False
            return labeling_layout

        number_of_widgets = 4 
        self.delete_widgets(labeling_layout, number_of_widgets)   
        self.is_traj_input_visible = False

        return labeling_layout
    
    def delete_widgets(self, labeling_layout, number_of_widgets):
        for _ in range(number_of_widgets):
            item = labeling_layout.takeAt(0)  

            if item is None:
                continue

            widget = item.widget()
            if widget:
                widget.deleteLater()  
                continue 

            layout = item.layout()
            if layout:
                while layout.count():  
                    sub_item = layout.takeAt(0)
                    sub_widget = sub_item.widget()

                    if sub_widget:
                        sub_widget.deleteLater()
                layout.deleteLater()  
