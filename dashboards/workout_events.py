from utils import utils
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from datetime import timedelta, date
from models.graph import Graph
from commons.calendar_service import calendar_service
from utils.graph_utils import generate_monthly_frequency_graph, generate_trend


class WorkoutGraphs:

    WORKOUT_CALENDAR_ID = "kfb7kr4iegnkieils995vrbeck@group.calendar.google.com"
    WORKOUT_GRAPHS_CONTENT_ID = "workout_graphs_content"
    WORKOUT_EVENTS_GRAPH_ID = "workout_events_graph"
    WEEKLY_WORKOUT_EVENTS_GRAPH_ID = "weekly_workout_events_graph"
    MONTHLY_WORKOUT_EVENTS_GRAPH_ID = "monthly_workout_events_graph"

    def __init__(self, start_date, end_date):
        self.start_date = date.fromisoformat(start_date)
        self.end_date = date.fromisoformat(end_date)
        self.workout_events = calendar_service.get_events(self.WORKOUT_CALENDAR_ID, start_date, end_date)
        self.content = html.Div(id=self.WORKOUT_GRAPHS_CONTENT_ID, children=[
            dcc.Graph(id=self.WORKOUT_EVENTS_GRAPH_ID, figure=self.get_workout_events_graph()),
            dcc.Graph(id=self.WEEKLY_WORKOUT_EVENTS_GRAPH_ID, figure=self.get_weekly_workout_graph()),
            dcc.Graph(id=self.MONTHLY_WORKOUT_EVENTS_GRAPH_ID, figure=self.get_monthly_workout_graph()),
        ], className="panel panel-default")

    def get_workout_events_graph(self):
        graph = Graph("Workout Events", "Date", "Time")
        for event in self.workout_events:
            graph.x.append(event.start.date())
            start_value = event.start.hour + event.start.minute / 60.0
            graph.y.append(start_value)
            graph.text.append(event.summary)
            graph.marker_size.append(event.duration_in_minutes / 2.5)

        fig = go.Figure()
        fig = graph.update_fig_layout(fig)

        fig.add_trace(go.Scatter(
            x=graph.x,
            y=graph.y,
            mode="markers",
            text=graph.text,
            marker=dict(size=graph.marker_size),
            textposition="top center"
        ))

        return fig

    def get_weekly_workout_graph(self):
        # return go.Figure()
        return generate_trend("Workout", self.workout_events, self.start_date, self.end_date, "Weekly", duration=False)

    def get_monthly_workout_graph(self):
        # return go.Figure()
        return generate_trend("Workout", self.workout_events, self.start_date, self.end_date, "Monthly", duration=False)
