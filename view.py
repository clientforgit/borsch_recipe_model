from typing import Protocol

import matplotlib

from PyQt5 import QtGui, QtWidgets, QtCore
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.collections import PathCollection
from matplotlib.backend_bases import MouseEvent
from config_load import config_data
from point_dto import PointDTO

matplotlib.use('qt5agg')

class Presenter(Protocol):
    def handle_on_motion(self, event):
        ...


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.scatter = None
        self.annotation = None
        self.bg = None
        self.fig, self.ax = plt.subplots()
        super(MplCanvas, self).__init__(self.fig)

    def create_ui(self, presenter: Presenter, points: list[PointDTO]):
        self.plot_init(points)
        self.connect_events(presenter)

    def plot_init(self, points: list[PointDTO], legend_points: list[int]):
        self.ax.grid()
        self.scatter = self.ax.scatter(
            [point.calories for point in points],
            [point.price for point in points],
            c=[point.color for point in points],
            s=config_data["point_size"],
            label=[point.label for point in points],
        )
        self.set_legend()
        self.annotation = self.ax.annotate(
            text='',
            xy=(3000, 10),
            xytext=(15, 15),
            textcoords='offset points',
            bbox={'boxstyle': 'round', 'fc': 'w'},
            arrowprops={'arrowstyle': '->'}
        )
        self.annotation.set_visible(False)
        self.ax.margins(0.05)
        self.ax.set_axisbelow(True)

    def set_legend(self):
        handles, labels = self.scatter.legend_elements()
        labels = ['in max deviation interval', 'out of max deviation interval']
        self.annotation = self.ax.legend(handles, labels, loc="upper left")

    @staticmethod
    def connect_events(presenter: Presenter):
        plt.connect('motion_notify_event', presenter.handle_on_motion)

    def update_annotation(self, index):
        if not self.annotation.get_visible():
            location = self.scatter.get_offsets()[index['ind'][0]]
            self.annotation.xy = location
            text_label = '({:.0f}, {:.2f})'.format(*location)
            self.annotation.set_text(text_label)
            self.annotation.set_visible(True)
            self.fig.canvas.draw_idle()


    def disable_annotation(self):
        if self.annotation.get_visible():
            self.annotation.set_visible(False)
            self.fig.canvas.draw_idle()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.mpl_canvas = MplCanvas()
        self.main_layout = None
        self.variables_layout = None
        self.tabs = None

    def create_ui(self, presenter: Presenter, points: list[PointDTO], model_characteristics: dict):
        self.mpl_canvas.create_ui(presenter, points)
        self.setFixedHeight(config_data["window_height"])
        self.setFixedWidth(config_data["window_width"])

        layout = QtWidgets.QVBoxLayout()
        self.__add_variables_layout()
        self.__add_tabs(model_characteristics)

        layout.addWidget(self.mpl_canvas)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def __add_tabs(self, model_characteristics: dict):
        self.tabs = QtWidgets.QTabWidget()
        tab1 = QtWidgets.QWidget()
        self.tabs.addTab(tab1, "DecisionTreeRegressor")
        self.add_tabs_content(tab1, model_characteristics)

    def add_tabs_content(self, tab, model_characteristics: dict):
        tab_layout = QtWidgets.QVBoxLayout()
        self.__add_tabs_characteristics(tab_layout, model_characteristics)
        self.__add_mpl_plots_control(tab_layout)
        tab.setLayout(tab_layout)

    def __add_tabs_characteristics(self, tab_layout, model_characteristics: dict):
        characteristics_layout = QtWidgets.QHBoxLayout()
        characteristics_layout.addWidget(QtWidgets.QLabel(f"ROC AUC : {self.model_characteristics['ROC AUC']}"))
        characteristics_layout.addWidget(QtWidgets.QLabel(f"MSE: {self.model_characteristics['MSE']}"))
        characteristics_layout.addWidget(QtWidgets.QLabel(f"R2: {self.model_characteristics['R2']}"))
        tab_layout.addLayout(characteristics_layout)

    def __add_variables_layout(self):
        variables_section = QtWidgets.QHBoxLayout()

        deviation_label = QtWidgets.QLabel()
        deviation_label.setText('Max deviation: ')

        deviation_line_edit = QtWidgets.QLineEdit()
        deviation_line_edit.setFixedWidth(config_data["line_edit_width"])
        deviation_line_edit.setValidator(QtGui.QDoubleValidator())
        deviation_line_edit.setText(str(config_data["max_deviation"]))

        dataset_size_label = QtWidgets.QLabel()
        dataset_size_label.setText('Dataset size: ')

        size_line_edit = QtWidgets.QLineEdit()
        size_line_edit.setFixedWidth(config_data["line_edit_width"])
        size_line_edit.setValidator(QtGui.QIntValidator())
        size_line_edit.setText(str(config_data["dataset_size"]))

        variables_section.addWidget(deviation_label)
        variables_section.addWidget(deviation_line_edit)
        variables_section.addWidget(dataset_size_label)
        variables_section.addWidget(size_line_edit)
        variables_section.addStretch()
        self.main_layout.addLayout(variables_section)