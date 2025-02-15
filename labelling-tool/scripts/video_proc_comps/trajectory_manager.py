class TrajectoryManager:
    def __init__(self):
        self.last_clicked_position = None

    def set_last_clicked_position(self, x, y):
        """Stores the last clicked position in image coordinates."""
        self.last_clicked_position = (x, y)

    def get_last_clicked_position(self):
        """Returns the last clicked position in image coordinates."""
        return self.last_clicked_position