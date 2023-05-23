from typing import Protocol

from model import BasicModel
from point_dto import PointDTO
from config_load import config_data
from matplotlib.collections import PathCollection
from matplotlib.text import Annotation

class View(Protocol):
    scatter: PathCollection

    def create_ui(self, presenter, y_data):
        ...

    def update_annotation(self, event):
        ...

    def disable_annotation(self):
        ...

class MainWindow(Protocol):
    mpl_canvas: View

    def create_ui(self, presenter, points_list: list[PointDTO]):
        ...


class Presenter:
    def __init__(self, view: MainWindow):
        self.view = view
        self.mpl_view = view.mpl_canvas
        self.annotation_show = False
        self.model = BasicModel('DecisionTreeRegressor')

    def handle_on_motion(self, event):
        if event.inaxes:
            contains, index = self.mpl_view.scatter.contains(event)
            if contains:
                self.mpl_view.update_annotation(index)
                self.annotation_show = True
            else:
                self.mpl_view.disable_annotation()

    def run(self):
        self.view.create_ui(self, self.model.points_list)
