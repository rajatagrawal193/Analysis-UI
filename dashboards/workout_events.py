from utils import utils
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from datetime import timedelta, date
from models.graph import Graph
from commons.calendar_service import calendar_service


class WorkoutGraphs:

    @staticmethod
    def get_workout_events_graph(start_date, end_date):
        print(start_date, end_date)
        workout_calendar_id = "kfb7kr4iegnkieils995vrbeck@group.calendar.google.com"
        workout_events = calendar_service.get_events(workout_calendar_id, start_date, end_date)
        graph = Graph("Workout Events", "Date", "Time")
        for event in workout_events:
            graph.x.append(event.start.date())
            start_value = event.start.hour + event.start.minute / 60.0
            end_value = event.end.hour + event.end.minute / 60.0
            graph.y.append(start_value)
            time_in_am_pm = event.start.strftime("%I:%M")
            graph.text.append(event.summary)
            graph.marker_size.append(event.duration_in_minutes/2.5)


        fig = go.Figure()

        fig.update_layout(legend_title_text=graph.title,
                          yaxis_title=graph.y_axis, xaxis_title=graph.x_axis,
                          title=utils.set_title(graph.title))
        # fig.update_yaxes(rangemode="tozero")
        # fig.update_yaxes(
        #     ticktext=["10 PM", "12 AM", "2AM", "5AM", "9AM"],
        #     tickvals=[22, 24, 26, 29, 33],
        # )
        fig.add_trace(go.Scatter(
            x=graph.x,
            y=graph.y,
            mode="markers",
            text=graph.text,
            marker=dict(size=graph.marker_size),
            textposition="top center"
        ))

        return fig

    def __init__(self):
        self.CONTENT = html.Div([
            dcc.Graph(id="workouts_graph", figure=self.get_workout_events_graph((date.today()-timedelta(days=31)).isoformat(),
                                                                           date.today().isoformat())),
        ], className="panel panel-default")


