from typing import Protocol

import matplotlib

from PyQt5 import QtGui, QtWidgets, QtCore
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from config_load import config_data
from point_dto import PointDTO

matplotlib.use('qt5agg')

class Presenter(Protocol):
    def handle_on_motion(self, event):
        ...


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.points_list = []
        fig, self.ax = plt.subplots()
        super(MplCanvas, self).__init__(fig)

    def create_ui(self, presenter: Presenter, points: list[PointDTO], legend_points: list[int]):
        self.plot_init(points, legend_points)
        self.connect_events(presenter)

    def plot_init(self, points: list[PointDTO], legend_points: list[int]):
        for point in points:
            point = self.ax.scatter(
                point.calories,
                point.price,
                c=point.color,
                s=config_data["point_size"],
                label=point.label
            )
            self.points_list.append(point)
        self.ax.grid()
        self.set_legend(legend_points)
        annotation = self.ax.annotate(
            text='',
            xy=(3000, 10),
            xytext=(15, 15),
            textcoords='offset points',
            bbox={'boxstyle': 'round', 'fc':'w'},
            arrowprops={'arrowstyle': '->'}
        )
        annotation.set_visible(True)
        self.ax.margins(0)
        self.draw()

    def set_legend(self, legend_points: list[int]):
        final = []
        if isinstance(legend_points[0], int):
            final.append(self.points_list[legend_points[0]])
        if isinstance(legend_points[1], int):
            final.append(self.points_list[legend_points[1]])
        self.ax.legend(handles=final)

    def connect_events(self, presenter: Presenter):
        plt.connect('motion_notify_event', presenter.handle_on_motion)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.mpl_canvas = MplCanvas()

    def create_ui(self, presenter: Presenter, points: list[PointDTO], legend_points: list[int]):
        self.mpl_canvas.create_ui(presenter, points, legend_points)
        self.setFixedHeight(config_data["window_height"])
        self.setFixedWidth(config_data["window_width"])
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        # toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(toolbar)
        label = QtWidgets.QLabel()
        layout.addWidget(label)
        layout.addWidget(self.mpl_canvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()
