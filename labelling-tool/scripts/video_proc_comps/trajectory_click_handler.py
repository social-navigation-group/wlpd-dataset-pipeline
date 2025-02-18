from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush
from utils.logging_utils import log_info
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem

class TrajectoryClickHandler(QGraphicsView):
    def __init__(self, trajectory_manager, trajectories, scene, parent = None):
        super().__init__(parent)
        self.scenes = scene
        self.trajectory_items = []
        self.selection_threshold = 50
        self.trajectory_manager = trajectory_manager  

        log_info(f"[DEBUG] Initializing {len(trajectories)} trajectories")

        for traj_id, traj in enumerate(trajectories, start = 1):
            traj_graphics = []
            log_info(f"Adding trajectory {traj_id} with {len(traj)} points.")

            for point_x, point_y in traj:
                point_item = QGraphicsEllipseItem(point_x - 3, point_y - 3, 6, 6)
                self.scenes.addItem(point_item)
                traj_graphics.append(point_item)

            self.trajectory_items.append((traj_id, traj_graphics))
            log_info(f"Stored {len(self.trajectory_items)} trajectories")
    
    def mousePressEvent(self, event):
        """Handles mouse click events and selects the closest trajectory."""
        scene_pos = self.mapToScene(event.position().toPoint())
        log_info(f"User clicked at Scene Coordinates: ({scene_pos.x()}, {scene_pos.y()})")

        # Draw a red marker at the clicked position
        click_marker = QGraphicsEllipseItem(scene_pos.x() - 5, scene_pos.y() - 5, 10, 10)
        click_marker.setPen(QPen(Qt.GlobalColor.red, 2))
        click_marker.setBrush(QBrush(Qt.GlobalColor.red))
        self.scenes.addItem(click_marker)

        for item in self.scenes.items(scene_pos):
            if isinstance(item, QGraphicsPixmapItem):
                pixmap_item = item
                pixmap_rect = pixmap_item.pixmap().rect()
                item_pos = pixmap_item.mapFromScene(scene_pos)

                orig_x = int((item_pos.x() / pixmap_item.boundingRect().width()) * pixmap_rect.width())
                orig_y = int((item_pos.y() / pixmap_item.boundingRect().height()) * pixmap_rect.height())

                log_info(f"Mapped Click to Image Coordinates: ({orig_x}, {orig_y})")

                selected_traj_id, nearest_x, nearest_y = self.find_nearest_trajectory(orig_x, orig_y)

                # Draw a blue marker at the nearest trajectory point
                if nearest_x is not None and nearest_y is not None:
                    traj_marker = QGraphicsEllipseItem(nearest_x - 5, nearest_y - 5, 10, 10)
                    traj_marker.setPen(QPen(Qt.GlobalColor.blue, 2))
                    traj_marker.setBrush(QBrush(Qt.GlobalColor.blue))
                    self.scenes.addItem(traj_marker)

                if selected_traj_id is not None:
                    log_info(f"Selected trajectory ID: {selected_traj_id}")
                    self.trajectory_manager.set_selected_trajectory(selected_traj_id)
                    self.highlight_selected_trajectory(selected_traj_id)
                else:
                    log_info("No trajectory selected")
                    self.trajectory_manager.clear_selection()

        super().mousePressEvent(event)

    def find_nearest_trajectory(self, x, y):
        """Finds the closest trajectory point."""
        min_distance = float("inf")
        selected_traj_id = None
        nearest_x, nearest_y = None, None

        log_info(f"Checking click at ({x}, {y}) against all trajectories:")

        for traj_id, traj_points in self.trajectory_items:  
            log_info(f"Checking Trajectory {traj_id}")

            for idx, point_item in enumerate(traj_points):  
                if isinstance(point_item, QGraphicsEllipseItem):
                    point_scene_pos = point_item.sceneBoundingRect().center()
                    mapped_pos = self.mapFromScene(point_scene_pos)

                    point_x, point_y = mapped_pos.x(), mapped_pos.y()
                    distance = ((x - point_x) ** 2 + (y - point_y) ** 2) ** 0.5

                    if traj_id == 1:
                        log_info(f" [DEBUG] [1] Point {idx}: Scene ({point_scene_pos.x():.2f}, {point_scene_pos.y():.2f}), "
                                f"Mapped ({point_x:.2f}, {point_y:.2f}), Distance: {distance:.2f}")

                    log_info(f" ? [{traj_id}] Point {idx}: Mapped ({point_x:.2f}, {point_y:.2f}), Distance: {distance:.2f}")

                    if distance < min_distance:
                        min_distance = distance
                        selected_traj_id = traj_id
                        nearest_x, nearest_y = point_x, point_y  

        log_info(f"Closest trajectory found: ID {selected_traj_id}, Min Distance: {min_distance:.2f}")

        if selected_traj_id is not None and min_distance < self.selection_threshold:
            log_info(f"Nearest trajectory confirmed: ID {selected_traj_id}")
            return selected_traj_id, nearest_x, nearest_y
        else:
            log_info("No trajectory found within selection threshold.")
            return None, None, None

    def highlight_selected_trajectory(self, traj_id):
        """ Highlights the selected trajectory by changing its appearance """
        log_info(f"Highlighting trajectory {traj_id}")

        for i, traj_items in enumerate(self.trajectory_items, start = 1):  
            for item in traj_items:
                if isinstance(item, QGraphicsEllipseItem):
                    if i == traj_id:
                        log_info(f"Setting Trajectory {traj_id} to GREEN")
                        item.setPen(QPen(Qt.GlobalColor.green, 3))
                        item.setBrush(QBrush(Qt.GlobalColor.green))
                    else:
                        item.setPen(QPen(Qt.GlobalColor.blue, 1))
                        item.setBrush(QBrush(Qt.GlobalColor.blue))
        
        self.scenes.update()
        self.update()
