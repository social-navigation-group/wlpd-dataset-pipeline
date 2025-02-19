import cv2
import time
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from utils.logging_utils import log_info, log_error

class TrajectoryWorker(QThread):
    update_overlay = pyqtSignal(np.ndarray)

    def __init__(self, trajectory_manager, trajectories, traj_starts, colors, video_width, video_height, total_frames, video_fps=30, cache_size=30):
        super().__init__()
        self.running = True
        self.colors = colors
        self.frame_number = -1
        self.overlay_cache = {} 
        self.video_fps = video_fps
        self.cache_size = cache_size  # Buffer only 30 frames (~1 sec)
        # self.traj_starts = traj_starts
        self.video_width = video_width
        self.video_height = video_height
        self.trajectories = trajectories
        self.total_frames = total_frames
        self.trajectory_manager = trajectory_manager

    def run(self):
        """Runs the thread and updates overlay when frame changes."""
        last_frame = -1  

        while self.running:
            if self.frame_number < 0 or self.frame_number == last_frame:
                time.sleep(1 / self.video_fps)  
                continue
            last_frame = self.frame_number  

            if self.frame_number in self.overlay_cache:
                overlay = self.overlay_cache[self.frame_number]
            else:
                overlay = self._generate_overlay(self.frame_number)
                self.overlay_cache[self.frame_number] = overlay

            self.update_overlay.emit(overlay)
            self._preload_future_frames(self.frame_number)

    def _generate_overlay(self, frame_idx):
        """Generates trajectory overlay and labels for a frame."""
        overlay = np.zeros((self.video_height, self.video_width, 3), dtype = np.uint8)
        active_trajectories = self.trajectory_manager.get_active_trajectories(frame_idx)

        for i, traj in enumerate(self.trajectories):
            if (i + 1) not in active_trajectories:
                continue

            # traj_start = self.traj_starts[i]
            traj_start = self.trajectory_manager.traj_starts[i + 1]
            frame_offset = frame_idx - traj_start

            if frame_offset < 0 or frame_offset >= len(traj):
                continue  

            # log_info(f"[DEBUG] TrajectoryWorker - Trajectory {i+1}: First Points {traj[:5]}")
            # log_info(f"[DEBUG] TrajectoryWorker - Trajectory {i+1}: Total Points {len(traj)}")
            log_info(f"[DEBUG] Overlay - Drawing Trajectory {i+1}: Frame {frame_idx}, Active Points: {frame_offset+1}")

            try:
                # past_points = traj[:frame_offset + 1]  
                active_traj = traj[: max(1, frame_offset + 1)]
                if len(active_traj) > 1:
                    for j in range(len(active_traj) - 1):
                        pt1 = self.scale_point(active_traj[j])
                        pt2 = self.scale_point(active_traj[j + 1])
                        cv2.line(overlay, pt1, pt2, self.colors[i % len(self.colors)].tolist(), 2)
                        
                        last_point = self.scale_point(active_traj[-1])
                        cv2.putText(overlay, str(i + 1), last_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 146, 35), 1, lineType=cv2.LINE_AA)
            except Exception as e:
                log_error(f"Error processing trajectory {i} at frame {frame_idx}: {e}")

        return overlay

    def _preload_future_frames(self, current_frame):
        """Preloads a small rolling buffer of frames in the background."""
        max_preload = min(self.total_frames, current_frame + self.cache_size)

        for frame_idx in range(current_frame + 1, max_preload):
            if frame_idx not in self.overlay_cache:
                self.overlay_cache[frame_idx] = self._generate_overlay(frame_idx)

        keys = list(self.overlay_cache.keys())
        if len(keys) > self.cache_size:
            for key in keys[:-self.cache_size]:  
                del self.overlay_cache[key]

    def scale_point(self, point):
        try:
            x, y = point
            scaled_x = int(x * self.video_width) if x <= 1 else int(round(x))
            scaled_y = int(y * self.video_height) if y <= 1 else int(round(y))
            return max(0, min(self.video_width - 1, scaled_x)), max(0, min(self.video_height - 1, scaled_y))
        except Exception as e:
            log_error(f"Error scaling point {point}: {e}")
            return (0, 0)

    def update_frame(self, frame_number):
        """Ensures the thread starts only if necessary."""
        if self.frame_number != frame_number:
            log_info(f"[DEBUG] Updating frame to {frame_number}")
            self.frame_number = frame_number
            if not self.isRunning(): 
                self.start()

    def stop(self):
        """Gracefully stops the thread."""
        if self.isRunning():  
            self.running = False
            self.wait()  
            self.quit()
        log_info("TrajectoryWorker stopped.")
