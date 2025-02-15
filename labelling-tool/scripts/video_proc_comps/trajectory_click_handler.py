
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush
from utils.logging_utils import log_info
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem

class TrajectoryClickHandler(QGraphicsView):
    def __init__(self, trajectory_manager, parent = None):
        super().__init__(parent)
        self.trajectory_manager = trajectory_manager  

    def mousePressEvent(self, event):
        """
        Handles mouse click events and converts view coordinates to image coordinates.
        Gets the position of the click relative to the displayed image.

        Note: A visual marker is drawn on the image for debugging purposes only.
        """
        # Convert mouse click position from the view to scene coordinates
        scene_pos = self.mapToScene(event.position().toPoint())

        # Get the item (image) at the clicked position
        item = self.scene().items(scene_pos)
        if item and isinstance(item[0], QGraphicsPixmapItem):
            pixmap_item = item[0] 
            pixmap_rect = pixmap_item.pixmap().rect()  # Get the original image size

            # Convert scene coordinates to item (image) coordinates
            item_pos = pixmap_item.mapFromScene(scene_pos)

            # Scale the mapped coordinates to match the original image resolution
            orig_x = int((item_pos.x() / pixmap_item.boundingRect().width()) * pixmap_rect.width())
            orig_y = int((item_pos.y() / pixmap_item.boundingRect().height()) * pixmap_rect.height())

            log_info(f"User clicked at Image Coordinates: ({orig_x}, {orig_y})")
            self.trajectory_manager.set_last_clicked_position(orig_x, orig_y)
            self.draw_marker(orig_x, orig_y)

        super().mousePressEvent(event)

    def draw_marker(self, x, y):
        """ Draws a small red circle at the given image coordinates. """
        marker_radius = 5 
        marker = QGraphicsEllipseItem(
            x - marker_radius, y - marker_radius, 
            2 * marker_radius, 2 * marker_radius
        )

        marker.setPen(QPen(Qt.GlobalColor.red, 2))  
        marker.setBrush(QBrush(Qt.GlobalColor.red))

        self.scene().addItem(marker)
