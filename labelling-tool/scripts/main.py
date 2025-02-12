import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    resources_path = os.path.join(os.path.dirname(__file__), "..", "resources")
    window = MainWindow(resources_path)
    window.show()
    sys.exit(app.exec())
