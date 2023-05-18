"""
PySide6 viewer wrapping vispy canvas. This is a separate process from the
controller to avoid blocking the main thread.
"""

from multiprocessing.connection import Connection

import numpy as np
from PySide6.QtCore import QObject, Qt, QThread, Signal, Slot
from PySide6.QtWidgets import QMainWindow
from vispy import app, scene
from vispy.app import use_app


class CanvasWrapper:
    def __init__(self):
        self._initialize_canvas()
        self.lines = {}

    @Slot(str, np.ndarray, list, float)
    def add_line(self, name, t, ys, offset):
        self.remove_line(name)
        colors = ["r", "b", "g"]
        self.lines[name] = {
            "line": [
                scene.Line(
                    np.column_stack((t, y + offset)),
                    color=color,
                    parent=self.view.scene,
                )
                for y, color in zip(ys, colors)
            ],
            "text": scene.Text(
                name,
                pos=(t[-1], offset),
                anchor_x="left",
                color="white",
                parent=self.view.scene,
            ),
            "t_range": (t[0], t[-1]),
            "y_range": (np.min(ys) + offset, np.max(ys) + offset),
        }

    @Slot(str)
    def remove_line(self, name):
        if name not in self.lines:
            return
        for line in self.lines[name]["line"]:
            line.parent = None
        self.lines[name]["text"].parent = None
        del self.lines[name]

    def get_range(self):
        t_range = [np.inf, -np.inf]
        y_range = [np.inf, -np.inf]
        for line in self.lines.values():
            t_range[0] = min(t_range[0], line["t_range"][0])
            t_range[1] = max(t_range[1], line["t_range"][1])
            y_range[0] = min(y_range[0], line["y_range"][0])
            y_range[1] = max(y_range[1], line["y_range"][1])
        return t_range, y_range

    @Slot()
    def clear(self):
        for name in list(self.lines.keys()):
            self.remove_line(name)

    @Slot()
    def autoscale(self):
        if len(self.lines) == 0:
            return
        t_range, y_range = self.get_range()
        self.view.camera.set_range(t_range, y_range)

    def _initialize_canvas(self):
        canvas = scene.SceneCanvas()
        self.canvas = canvas
        grid = canvas.central_widget.add_grid(margin=10)

        title = scene.Label('"F" fit screen "C" clear all', color="white")
        title.height_max = 40
        grid.add_widget(title, row=0, col=0, col_span=2)

        yaxis = scene.AxisWidget(
            orientation="left",
            axis_label="Y Axis",
            axis_font_size=12,
            axis_label_margin=50,
            tick_label_margin=5,
        )
        yaxis.width_max = 80
        grid.add_widget(yaxis, row=1, col=0)

        xaxis = scene.AxisWidget(
            orientation="bottom",
            axis_label="t",
            axis_font_size=12,
            axis_label_margin=50,
            tick_label_margin=25,
        )

        xaxis.height_max = 80
        grid.add_widget(xaxis, row=2, col=1)

        right_padding = grid.add_widget(row=1, col=2, row_span=1)
        right_padding.width_max = 50

        view = grid.add_view(row=1, col=1, border_color="white")
        view.camera = "panzoom"
        scene.GridLines(parent=view.scene)
        self.view = view

        xaxis.link_view(view)
        yaxis.link_view(view)

        @canvas.events.key_press.connect
        def on_key_press(event):
            if event.text == "f":
                self.autoscale()
            if event.text == "c":
                self.clear()


class WaveViewerWindow(QMainWindow):
    closing = Signal()

    def __init__(self, canvas_wrapper: CanvasWrapper) -> None:
        super().__init__()
        self.setWindowTitle("Wave Viewer")
        self._canvas_wrapper = canvas_wrapper
        self.setCentralWidget(canvas_wrapper.canvas.native)

    def closeEvent(self, event):
        self.closing.emit()
        return super().closeEvent(event)


class DataSource(QObject):
    add_line = Signal(str, np.ndarray, list, float)
    remove_line = Signal(str)
    clear = Signal()
    autoscale = Signal()
    finished = Signal()

    def __init__(self, conn: Connection) -> None:
        super().__init__()
        self.conn = conn
        self._should_stop = False

    @Slot()
    def run(self):
        while not self._should_stop:
            if self.conn.poll(0.1):
                msg = self.conn.recv()
            else:
                continue
            if msg["type"] == "add_line":
                self.add_line.emit(msg["name"], msg["t"], msg["ys"], msg["offset"])
            elif msg["type"] == "remove_line":
                self.remove_line.emit(msg["name"])
            elif msg["type"] == "clear":
                self.clear.emit()
            elif msg["type"] == "autoscale":
                self.autoscale.emit()
            else:
                raise ValueError(f"Unknown message type: {msg['type']}")
        self.finished.emit()

    @Slot()
    def stop(self):
        self._should_stop = True


def main(rconn: Connection):
    app = use_app("PySide6")
    app.create()
    canvas_wrapper = CanvasWrapper()
    window = WaveViewerWindow(canvas_wrapper)
    thread = QThread(parent=window)
    source = DataSource(rconn)
    source.moveToThread(thread)
    thread.started.connect(source.run)
    source.add_line.connect(canvas_wrapper.add_line)
    source.remove_line.connect(canvas_wrapper.remove_line)
    source.clear.connect(canvas_wrapper.clear)
    source.autoscale.connect(canvas_wrapper.autoscale)
    window.closing.connect(source.stop, Qt.DirectConnection)
    source.finished.connect(thread.quit, Qt.DirectConnection)
    thread.finished.connect(source.deleteLater)
    window.show()
    thread.start()
    app.run()
    thread.wait(5000)


if __name__ == "__main__":
    app = use_app("PySide6")
    app.create()
    canvas_wrapper = CanvasWrapper()
    win = WaveViewerWindow(canvas_wrapper)
    win.show()
    app.run()
