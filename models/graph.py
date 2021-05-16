import plotly.graph_objects as go
from utils.utils import set_title


class Graph:
    def get_figure(self):
        fig = go.Figure()
        fig.update_layout(dict(
            title=set_title(self.title)),
            xaxis_title=self.x_axis,
            yaxis_title=self.y_axis,
        )
        return fig

    def update_fig_layout(self, fig):
        fig.update_layout(
            title=set_title(self.title),
            xaxis_title=self.x_axis,
            yaxis_title=self.y_axis,
            legend_title="Legend Title",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=15,
            #     color="RebeccaPurple"
            # )
        )
        return fig

    def __init__(self, title, x_axis, y_axis):
        self.title = title
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.x = []
        self.y = []
        self.avg = []
        self.text = []
        self.marker_color = []
        self.marker_size = []
