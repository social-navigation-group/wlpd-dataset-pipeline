class TrajectoryManager:
    def __init__(self):
        self.traj_starts = {}
        self.trajectories = {}
        self.selected_traj = None
        self.last_clicked_position = None

    def set_trajectories(self, trajectories, traj_starts):
        """Stores trajectories and their start frames."""
        self.trajectories = {traj_id: traj for traj_id, traj in enumerate(trajectories, start=1)}
        self.traj_starts = {traj_id: start for traj_id, start in enumerate(traj_starts, start=1)}

    def get_trajectory(self, traj_id):
        """Returns the trajectory points for a given trajectory ID."""
        return self.trajectories.get(traj_id, [])

    def get_active_trajectories(self, current_frame):
        """Returns the list of trajectories that should be visible at the given frame."""
        active_trajectories = []

        for traj_id, traj_start in self.traj_starts.items():
            if traj_start <= current_frame < traj_start + len(self.trajectories[traj_id]):  
                active_trajectories.append(traj_id)

        return active_trajectories

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
