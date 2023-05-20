from typing import Protocol

from model import BasicModel
from point_dto import PointDTO
from config_load import config_data

class View(Protocol):
    points_list: list[PointDTO]

    def create_ui(self, presenter, y_data):
        ...


class MainWindow(Protocol):
    mpl_canvas: View

    def create_ui(self, presenter, points_list: list[PointDTO]):
        ...


class Presenter:
    def __init__(self, view: MainWindow):
        self.view = view
        self.mpl_view = view.mpl_canvas
        self.model = BasicModel('DecisionTreeRegressor')

    def find_legend_points(self):
        first_index = None
        second_index = None
        for i in range(config_data["dataset_size"]):
            if self.model.points_list[i].label == 'in max deviation interval':
                first_index = i
            elif self.model.points_list[i].label == 'out of max deviation interval':
                second_index = i
        return [first_index, second_index]

    def handle_on_motion(self, event):
        if event.inaxes:
            annotation = self.mpl_view.ax.texts[0]
            annotation.set_text(
                f'x={event.xdata:.2f}, y={event.ydata:.2f}'
            )
            self.mpl_view.draw()


    def run(self):
        self.view.create_ui(self, self.model.points_list, self.find_legend_points())
