class TrajectoryManager:
    def __init__(self):
        self.selected_traj = None
        self.last_clicked_position = None

    def set_last_clicked_position(self, x, y):
        """Stores the last clicked position in image coordinates."""
        self.last_clicked_position = (x, y)

    def get_last_clicked_position(self):
        """Returns the last clicked position in image coordinates."""
        return self.last_clicked_position

    def set_selected_trajectory(self, selected_traj_id):
        """Stores the selected trajectory ID."""
        self.selected_traj = selected_traj_id

    def get_selected_trajectory(self):
        """Returns the currently selected trajectory ID."""
        return self.selected_traj

    def clear_selection(self):
        """Clears the selected trajectory."""
        self.selected_traj = None
