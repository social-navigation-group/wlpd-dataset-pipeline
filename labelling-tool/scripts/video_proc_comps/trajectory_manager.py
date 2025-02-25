from utils.logging_utils import log_info

class TrajectoryManager:
    def __init__(self, human_config):
        self.traj_starts = {}
        self.trajectories = {}
        self.selected_trajs = []
        self.human_config = human_config

    def set_trajectories(self):
        """Assigns trajectories using stored IDs"""
        self.traj_starts = {}
        self.trajectories = {}

        for humanID in self.human_config.dict.keys():
            traj = self.human_config.get_element(humanID, "trajectories")
            start = self.human_config.get_element(humanID, "traj_start")

            if traj is not None and start is not None:
                traj_id = int(humanID.replace("human", ""))
                self.trajectories[traj_id] = traj
                self.traj_starts[traj_id] = start

    def add_trajectory(self, new_trajectory, start_frame):
        traj_id = self.human_config.get_newID()
        self.trajectories[traj_id] = new_trajectory
        self.traj_starts[traj_id] = start_frame

        self.human_config.set_element(traj_id, "trajectories", new_trajectory)
        self.human_config.set_element(traj_id, "traj_start", start_frame)
        return traj_id
    
    def remove_trajectory(self, traj_id):
        if traj_id in self.trajectories:
            del self.trajectories[traj_id]
            del self.traj_starts[traj_id]
            self.human_config.delete_ID(traj_id)

    def get_active_trajectories(self, current_frame):
        active_trajectories = []

        for traj_id, traj_start in self.traj_starts.items():
            if traj_start <= current_frame < traj_start + len(self.trajectories[traj_id]):  
                active_trajectories.append(traj_id)

        return active_trajectories

    def set_selected_trajectory(self, selected_traj_id):
        if len(self.selected_trajs) < 2:
            if selected_traj_id not in self.selected_trajs:
                self.selected_trajs.append(selected_traj_id)
                log_info(f"[DEBUG] Selected trajectories: {self.selected_trajs}")
        else:
            log_info("Two trajectories already selected. No more can be added.")

    def get_selected_trajectory(self):
        return list(self.selected_trajs)

    def clear_selection(self):
        self.selected_trajs = []