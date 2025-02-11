from human_controls import HumanControls
from trajectory_controls import TrajectoryControls
from PyQt6.QtWidgets import QDialog, QWidget, QTabWidget, QVBoxLayout

class TabDialog(QDialog):
    def __init__(self, video_controls, parent: QWidget = None):
        super().__init__(parent)

        self.video_controls = video_controls
        self.video_player = self.video_controls.get_video_player()

        tab_widget = QTabWidget()
        tab_widget.addTab(TrajectoryControls(self.video_player, self), "Trajectory")
        tab_widget.addTab(HumanControls(self.video_player, self), "Human")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)
