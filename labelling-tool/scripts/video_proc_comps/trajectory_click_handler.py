from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush
from utils.logging_utils import log_info
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem

class TrajectoryClickHandler(QGraphicsView):
    def __init__(self, trajectory_manager, trajectories, scene, current_frame, parent = None):
        super().__init__(parent)
        self.graphics_scene = scene
        self.trajectory_items = []
        # self.selection_threshold = 90
        self.current_frame = current_frame
        self.trajectory_manager = trajectory_manager  

        # log_info(f"[DEBUG] Initializing {len(trajectories)} trajectories")

        for traj_id, traj in enumerate(trajectories, start = 1):
            # log_info(f"[DEBUG] ClickHandler - Storing Traj {traj_id}: {traj[:5]} (first 5 points)")

            traj_graphics = []
            active_traj = traj[:max(1, self.current_frame)]
            # log_info(f"Adding trajectory {traj_id} with {len(active_traj)} active points.")

            for point_x, point_y in active_traj:
                point_item = QGraphicsEllipseItem(point_x - 3, point_y - 3, 6, 6)
                self.graphics_scene.addItem(point_item)
                traj_graphics.append(point_item)

            self.trajectory_items.append((traj_id, traj_graphics))
            log_info(f"Stored {len(self.trajectory_items)} trajectories (Active Points: {len(active_traj)})")

        # log_info(f"[DEBUG] ClickHandler - Trajectory 2 First Points: {self.trajectory_items[1][:5]}")
        # log_info(f"[DEBUG] ClickHandler - Traj 2: Total Points: {len(self.trajectory_items[1])}")

    
    def mousePressEvent(self, event):
        """Handles mouse click events and selects the closest trajectory."""
        scene_pos = self.mapToScene(event.position().toPoint())
        log_info(f"User clicked at Scene Coordinates: ({scene_pos.x()}, {scene_pos.y()})")

        # mapped_click = self.mapFromScene(scene_pos)
        # log_info(f"[DEBUG] Mapped Click Back to Scene: ({mapped_click.x()}, {mapped_click.y()})")

        # Draw a red marker at the clicked position
        # click_marker = QGraphicsEllipseItem(scene_pos.x() - 5, scene_pos.y() - 5, 10, 10)
        # click_marker.setPen(QPen(Qt.GlobalColor.red, 2))
        # click_marker.setBrush(QBrush(Qt.GlobalColor.red))
        # self.graphics_scene.addItem(click_marker)

        for item in self.graphics_scene.items(scene_pos):
            if isinstance(item, QGraphicsPixmapItem):
                pixmap_item = item
                pixmap_rect = pixmap_item.pixmap().rect()
                item_pos = pixmap_item.mapFromScene(scene_pos)

                orig_x = int((item_pos.x() / pixmap_item.boundingRect().width()) * pixmap_rect.width())
                orig_y = int((item_pos.y() / pixmap_item.boundingRect().height()) * pixmap_rect.height())

                # log_info(f"[DEBUG] ClickHandler - Bounding Box: {pixmap_item.boundingRect()}")
                # log_info(f"Mapped Click to Image Coordinates: ({orig_x}, {orig_y})")

                selected_traj_id, nearest_x, nearest_y = self.find_nearest_trajectory(orig_x, orig_y)

                # Draw a blue marker at the nearest trajectory point
                # if nearest_x is not None and nearest_y is not None:
                    # traj_marker = QGraphicsEllipseItem(nearest_x - 5, nearest_y - 5, 10, 10)
                    # traj_marker.setPen(QPen(Qt.GlobalColor.blue, 2))
                    # traj_marker.setBrush(QBrush(Qt.GlobalColor.blue))
                    # self.graphics_scene.addItem(traj_marker)

                if selected_traj_id is not None:
                    log_info(f"Selected trajectory ID: {selected_traj_id}")
                    self.trajectory_manager.set_selected_trajectory(selected_traj_id)
                    self.highlight_selected_trajectory(selected_traj_id)
                else:
                    log_info("No trajectory selected")
                    self.trajectory_manager.clear_selection()

        super().mousePressEvent(event)
    
    def find_nearest_trajectory(self, x, y):
        """Selects only the trajectory point that the user directly clicks on."""
        active_trajectories = self.trajectory_manager.get_active_trajectories(self.current_frame)
        # log_info(f"Checking click at ({x}, {y}) against active trajectories: {active_trajectories}")

        for traj_id, traj_points in self.trajectory_items:
            if traj_id not in active_trajectories:
                continue

            for point_item in traj_points:
                if isinstance(point_item, QGraphicsEllipseItem):
                    point_scene_pos = point_item.sceneBoundingRect()

                    if point_scene_pos.contains(x, y):
                        log_info(f"? Click was inside trajectory {traj_id} at ({x}, {y}). Selecting immediately.")
                        return traj_id, point_scene_pos.center().x(), point_scene_pos.center().y()

        log_info("? No trajectory point was clicked. No selection made.")
        return None, None, None

    def update_trajectories(self, current_frame):
        """Dynamically updates trajectory points based on the current frame while preserving the highlighted trajectory."""
        # log_info(f"[DEBUG] Updating Trajectories at Frame {current_frame}")

        active_trajectories = self.trajectory_manager.get_active_trajectories(current_frame)  
        selected_traj_id = self.trajectory_manager.get_selected_trajectory()  

        for traj_id, (_, traj_graphics) in enumerate(self.trajectory_items, start = 1):
            if traj_id not in active_trajectories:
                for item in traj_graphics:
                    self.graphics_scene.removeItem(item)
                traj_graphics.clear()
                continue  

            active_traj = self.trajectory_manager.get_trajectory(traj_id)[: max(1, current_frame)]
            if len(active_traj) == len(traj_graphics):  
                continue  

            for item in traj_graphics:
                self.graphics_scene.removeItem(item)
            traj_graphics.clear()

            for point_x, point_y in active_traj:
                point_item = QGraphicsEllipseItem(point_x - 3, point_y - 3, 6, 6)
                if traj_id == selected_traj_id:
                    point_item.setPen(QPen(Qt.GlobalColor.green, 3))
                    point_item.setBrush(QBrush(Qt.GlobalColor.green))
                '''else:
                    point_item.setPen(QPen(Qt.GlobalColor.blue, 1))
                    point_item.setBrush(QBrush(Qt.GlobalColor.blue))'''

                self.graphics_scene.addItem(point_item)
                traj_graphics.append(point_item)

            log_info(f"[DEBUG] Updated Trajectory {traj_id}: {len(traj_graphics)} points")

        self.graphics_scene.update()
        self.update()
    
    def highlight_selected_trajectory(self, selected_traj_id):
        log_info(f"Highlighting trajectory {selected_traj_id}")

        if selected_traj_id is not None:
            for traj_id_iter, traj_items in self.trajectory_items:
                if traj_id_iter == selected_traj_id:
                    for item in traj_items:
                        if isinstance(item, QGraphicsEllipseItem):
                            log_info(f"Setting Trajectory {selected_traj_id} to GREEN")
                            item.setPen(QPen(Qt.GlobalColor.green, 3))
                            item.setBrush(QBrush(Qt.GlobalColor.green))

        self.graphics_scene.update()
        self.update()
