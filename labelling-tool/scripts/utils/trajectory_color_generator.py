import random
import numpy as np
from .logging_utils import log_info

class TrajectoryColorGenerator:
    def __init__(self):
        self.active_colors = {}
        self.predefined_color_pallet = [
            (255, 255, 255),  # White
            (0, 255, 255),    # Cyan
            (255, 0, 255),    # Magenta
            (255, 255, 0),    # Yellow
            (255, 0, 0),      # Red
            (255, 192, 203),  # Pink
            (0, 0, 255),      # Blue
            (128, 0, 128),    # Purple
            (255, 165, 0),    # Orange
            (0, 128, 128)     # Teal
        ]
        self.unused_colors = self.predefined_color_pallet.copy()
    
    def get_color(self, traj_id):
        if traj_id in self.active_colors:
            return self.active_colors[traj_id]
        
        if self.unused_colors:
            color = self.unused_colors.pop(0)
        else:
            color = self._generate_random_color()
        
        self.active_colors[traj_id] = np.array(color, dtype = np.uint8)
        return self.active_colors[traj_id]
        
    def _generate_random_color(self):
        while True:
            color = tuple(random.randint(50, 255) for _ in range(3))
            if not any(np.array_equal(color, v) for v in self.active_colors.values()):
                return color
    
    def release_color(self, traj_id):
        if traj_id in self.active_colors:
            color = self.active_colors.pop(traj_id)
            if color in self.predefined_color_pallet:
                self.unused_colors.append(color)

    def get_active_colors(self):
        return self.active_colors