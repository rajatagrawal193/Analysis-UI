import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from datetime import timedelta, date
from models.graph import Graph
from commons.calendar_service import calendar_service
from utils.graph_utils import generate_monthly_frequency_graph, generate_weekly_monthly_trends


class WorktimeGraphs:
    WORKTIME_CALENDAR_ID = "u7mordbnuo8gstjscejj1i94q4@group.calendar.google.com"
    WORKTIME_GRAPHS_CONTENT_ID = "worktime_graphs_content"
    WORKTIME_EVENTS_GRAPH_ID = "worktime_events_graph"
    WEEKLY_WORKTIME_EVENTS_GRAPH_ID = "weekly_worktime_events_graph"
    MONTHLY_WORKTIME_EVENTS_GRAPH_ID = "monthly_worktime_events_graph"
    LATE_NIGHT_SHIFT = 5

    def __init__(self, start_date, end_date):
        self.start_date = date.fromisoformat(start_date)
        self.end_date = date.fromisoformat(end_date)
        self.worktime_events = calendar_service.get_events(self.WORKTIME_CALENDAR_ID, start_date, end_date)
        self.shift_late_night_entries()
        self.content = html.Div(id=self.WORKTIME_GRAPHS_CONTENT_ID, children=[
            dcc.Graph(id=self.WORKTIME_EVENTS_GRAPH_ID, figure=self.get_worktime_events_graph()),
            dcc.Graph(id=self.WEEKLY_WORKTIME_EVENTS_GRAPH_ID, figure=self.get_weekly_worktime_graph()),
            dcc.Graph(id=self.MONTHLY_WORKTIME_EVENTS_GRAPH_ID, figure=self.get_monthly_worktime_graph()),
        ], className="panel panel-default")

    def shift_late_night_entries(self):
        for event in self.worktime_events:
            event.date = event.start.date()-timedelta(days=1) if event.start.hour <= 5.0 else event.start.date()

    def get_worktime_events_graph(self):
        graph = Graph("Worktime Events", "Date", "Time")
        for event in self.worktime_events:
            graph.x.append(event.start.date())
            start_value = event.start.hour + event.start.minute / 60.0
            graph.y.append(start_value)
            graph.text.append(event.summary)
            graph.marker_size.append(event.duration_in_minutes / 5.0)

        fig = go.Figure()
        # fig = graph.update_fig_layout(fig)

        fig.add_trace(go.Scatter(
            x=graph.x,
            y=graph.y,
            mode="markers",
            text=graph.text,
            marker=dict(size=graph.marker_size),
            textposition="top center"
        ))

        return fig

    def get_weekly_worktime_graph(self):
        # return go.Figure()
        return generate_weekly_monthly_trends("Worktime", self.worktime_events, self.start_date, self.end_date, "Weekly", duration=True )

    def get_monthly_worktime_graph(self):
        # return go.Figure()
        return generate_weekly_monthly_trends("Worktime", self.worktime_events, self.start_date, self.end_date, "Daily", duration=True)