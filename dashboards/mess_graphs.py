import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from commons.calendar_service import calendar_service
from models.graph import Graph
from models.calendar_event import CalendarEvent
from datetime import datetime, date, timedelta
from utils.graph_utils import get_events_by_month, get_events_by_week


class MessGraphs:
    MESS_CALENDAR_ID = "cjc4ns2rsn9m6b4mvfa4u4k5a8@group.calendar.google.com"
    MESS_EVENTS_GRAPH_ID = "mess_events_graph"
    WEEKLY_MESS_EVENTS_GRAPH_ID = "weekly_mess_events_graph"
    MONTHLY_MESS_EVENTS_GRAPH_ID = "monthly_mess_events_graph"

    def __init__(self, start_date: str, end_date: str):
        self.start_date = date.fromisoformat(start_date)
        self.end_date = date.fromisoformat(end_date)
        self.mess_events = calendar_service.get_events(self.MESS_CALENDAR_ID, start_date, end_date)
        self.content = html.Div([
                        dcc.Graph(id=self.MESS_EVENTS_GRAPH_ID, figure=self.get_mess_graph()),
                        dcc.Graph(id=self.WEEKLY_MESS_EVENTS_GRAPH_ID, figure=self.get_weekly_mess_graph()),
                        dcc.Graph(id=self.MONTHLY_MESS_EVENTS_GRAPH_ID, figure=self.get_monthly_mess_graph()),
        ], className="panel panel-default")

    def get_mess_graph(self):
        title = f"Mess Events| Total Events = {len(self.mess_events)}"
        graph = Graph(title, "Time", "Date")
        for event in self.mess_events:
            graph.x.append(event.start)
            graph.y.append(event.start.hour)
            graph.text.append(event.summary)

        fig = graph.get_figure()
        fig.add_trace(go.Scatter(
            x=graph.x,
            y=graph.y,
            name=graph.title,
            text=graph.text,
            marker=dict(size=8),
            mode='markers'
        ))
        return fig

    @staticmethod
    def get_weekly_events(events: [CalendarEvent]) -> dict[str, [CalendarEvent]]:
        weekly_segregated_events = {}
        for event in events:
            week = "Week " + str(event.start.date().isocalendar()[1])
            if week not in weekly_segregated_events:
                weekly_segregated_events[week] = [event]
            else:
                weekly_segregated_events[week].append(event)
        return weekly_segregated_events

    @staticmethod
    def get_events_by_month(events):
        events_by_month = {}
        for event in events:
            month = str(event.start.date().strftime("%b"))
            if month not in events_by_month:
                events_by_month[month] = [event]
            else:
                events_by_month[month].append(event)
        return events_by_month

    def get_weekly_mess_graph(self) -> go.Figure():
        delta = self.end_date- self.start_date
        total_days = delta.days
        avg = len(self.mess_events) / total_days * 7.0
        graph = Graph(f"Weekly Mess Events | Avg: {avg} ", "Frequency", "Week No")
        weekly_segregated_events = self.get_weekly_events(self.mess_events)
        for week, events in weekly_segregated_events.items():
            graph.x.append(week)
            graph.y.append(len(events))

        fig = go.Figure([go.Bar(x=graph.x, y=graph.y, name=graph.title)])
        # fig = graph.update_fig_layout(fig)
        return fig

    def get_monthly_mess_graph(self):
        delta = self.end_date - self.start_date
        total_days = delta.days
        avg = len(self.mess_events) / total_days * 30.0
        graph = Graph(f"Monthly Mess Events | Avg: {avg}", "Frequency", "Month")
        events_by_month = self.get_events_by_month(self.mess_events)
        for month, events in events_by_month.items():
            graph.x.append(month)
            graph.y.append(len(events))

        fig = go.Figure([go.Bar(x=graph.x, y=graph.y, name=graph.title)])
        # fig = graph.update_fig_layout(fig)
        return fig

