import plotly.graph_objects as go
from utils.utils import set_title


class Graph:
    def get_figure(self):
        fig = go.Figure()
        fig.update_layout(legend_title_text=self.title,
                          yaxis_title=self.y_axis, xaxis_title=self.x_axis,
                          title=set_title(self.title))
        return fig

    def update_fig_layout(self, fig):
        fig.update_layout(legend_title_text=self.title,
                          yaxis_title=self.y_axis, xaxis_title=self.x_axis,
                          title=set_title(self.title))
        return fig

    def __init__(self, title, x_axis, y_axis):
        self.title = title
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.x = []
        self.y = []
        self.text = []
        self.marker_color = []
        self.marker_size = []
