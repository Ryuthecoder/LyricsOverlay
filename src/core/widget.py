from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor 
from PyQt6.QtWidgets import QWidget



class Widget(QWidget):
    moved = pyqtSignal(str, QPoint) # records id and position of widget, used to signal widgetManager

    def __init__(self, widget_id: str, always_on_top: bool = False):
        super().__init__() #sets up QWidget class 
        self.widget_id = widget_id
        self.always_on_top = always_on_top
        self._drag_offset = None

        flags = Qt.WindowType.FramelessWindowHint
        if always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(300,120)

        # abstract: unique for each widget
        def start(self):
            raise NotImplementedError(f"{type(self).__name__} define start()")

        def stop(self):
            raise NotImplementedError(f"{type(self).__name__} define stop()")

        def draw_content(self, painter: QPainter):
            raise NotImplementedError(f"{type(self).__name__} define draw_content()")

        # shared (for drawing)
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(20,20,20,170))
            painter.drawRoundedRect(self.rect(),16,16)
            self.draw_content(painter)
            painter.end()

        # shared (for dragging)
        def mousePressEvent(self,event):
            if event.button() == Qt.MouseButton.LeftButton:
                self._drag_offset = event.globalPosition().toPoint() - self.pos()

        def mouseMoveEvent(self, event):
            if self._drag_offset is not None:
                self.move(event.globalPosition().toPoint() - self._drag_offset)

        def mouseReleaseEvent(self, event):
            if self._drag_offset is not None:
                self._drag_offset = None
                self.moved.emit(self.widget_id, self.pos())
                    
