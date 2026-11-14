from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor
from core.widget import Widget
from services.sync_engine import SyncEngine


class LyricsWidget(Widget):
    def __init__(self, widget_id: str, always_on_top: bool = False):
        super().__init__(widget_id, always_on_top)
        self.current_line = ""
        self.next_line = ""
        self.engine = SyncEngine()
        self.engine.line_changed.connect(self.show_line)
        self.engine.no_lyrics.connect(self.show_message)

    def start(self):
        self.engine.start()

    def stop(self):
        self.engine.stop()

    def show_line(self, current: str, next_line: str):
        self.current_line = current
        self.next_line = next_line
        self.update()                   # redraw with the new lines

    def show_message(self, text: str):
        self.show_line(text, "")

    def draw_content(self, painter):
        half = self.height() // 2
        painter.setPen(QColor("white"))
        painter.drawText(QRect(0, 0, self.width(), half), Qt.AlignmentFlag.AlignCenter, self.current_line)
        painter.setPen(QColor("gray"))
        painter.drawText(QRect(0, half, self.width(), half), Qt.AlignmentFlag.AlignCenter, self.next_line)