from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtCore import Qt

class ZoomableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = None
        self._scale = 1.0

    def setPixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self._scale = 1.0
        super().setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def wheelEvent(self, event: QWheelEvent):
        if self._pixmap is None:
            return
        # 滚轮缩放因子
        angle = event.angleDelta().y()
        if angle > 0:
            self._scale *= 1.1
        else:
            self._scale /= 1.1

        # 缩放范围限制
        self._scale = max(0.1, min(self._scale, 10))

        scaled_pixmap = self._pixmap.scaled(
            self._pixmap.size() * self._scale,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        super().setPixmap(scaled_pixmap)
