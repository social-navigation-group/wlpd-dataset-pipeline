import sys
from PyQt6.QtCore import QFileInfo
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QFrame, QVBoxLayout

class HumanControls(QWidget):
    def __init__(self, video_player, parent: QWidget):
        super().__init__(parent)
        self.video_player = video_player

        # SET TESTING IN THE LAYOUT
        self.setLayout(self.just_to_insert_something())
    
    def just_to_insert_something(self):
        if len(sys.argv) >= 2:
           file_name = sys.argv[1]
        else:
           file_name = "."
        
        file_info = QFileInfo(file_name)

        file_name_label = QLabel("File Name:")
        file_name_edit = QLineEdit(file_info.fileName())

        path_label = QLabel("Path:")
        path_value_label = QLabel(file_info.absoluteFilePath())
        path_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        size_label = QLabel("Size:")
        size = file_info.size() / 1024
        size_value_label = QLabel(f"{size} K")
        size_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        last_read_label = QLabel("Last Read:")
        last_read_value_label = QLabel(file_info.lastRead().toString())
        last_read_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        last_mod_label = QLabel("Last Modified:")
        last_mod_value_label = QLabel(file_info.lastModified().toString())
        last_mod_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        main_layout = QVBoxLayout()
        main_layout.addWidget(file_name_label)
        main_layout.addWidget(file_name_edit)
        main_layout.addWidget(path_label)
        main_layout.addWidget(path_value_label)
        main_layout.addWidget(size_label)
        main_layout.addWidget(size_value_label)
        main_layout.addWidget(last_read_label)
        main_layout.addWidget(last_read_value_label)
        main_layout.addWidget(last_mod_label)
        main_layout.addWidget(last_mod_value_label)
        main_layout.addStretch(1)

        if self.video_player:
            main_layout.addWidget(QLabel("Video Player Linked!"))
        
        return main_layout
