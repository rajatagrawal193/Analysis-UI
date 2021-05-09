from dashboards.graph import Graph
from utils import utils
# from . import params

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from GoogleAPI.google_calendar import CalendarService


def filter_sleep_entries(sleep_entries):
    return [item for item in sleep_entries if not (7.0 < item.start.hour < 20.0)]


def get_sleep_duration_graph(start_date, end_date):
    calendar_service = CalendarService()
    sleep_calendar_id = "gc1r2v6buaavim8o14bkd61r7g@group.calendar.google.com"
    sleep_events = calendar_service.get_events(sleep_calendar_id, start_date, end_date)
    sleep_events = filter_sleep_entries(sleep_events)

    # data ={'x': [], 'y': [], 'text': []}
    graph = Graph("Sleep Duration Graph", "Date", "Time")

    for event in sleep_events:
        graph.x.append(event.end.date() - timedelta(days=1))
        difference = event.end - event.start
        duration = difference.total_seconds()
        duration_in_hour = duration / 3600.0
        graph.y.append(duration_in_hour)

    fig = go.Figure([go.Bar(x=graph.x, y=graph.y)])
    return fig


def get_sleep_time_graph(start_date, end_date):
    print(start_date, end_date)
    calendar_service = CalendarService()
    sleep_calendar_id = "gc1r2v6buaavim8o14bkd61r7g@group.calendar.google.com"
    sleep_events = calendar_service.get_events(sleep_calendar_id, start_date, end_date)
    sleep_events = filter_sleep_entries(sleep_events)
    # data = {'x': [], 'y': [], 'y2': [], 'hover_text': [], 'hover_text2': [],'color': [], 'name': 'Sleep Duration'}
    bed_time_graph = Graph("Bed Time Graph", "Date", "Time")
    getup_time_graph = Graph("Get-up Time Graph", "Date", "Time")

    for event in sleep_events:
        bed_time_graph.x.append(event.end.date() - timedelta(days=1))
        start_value = event.start.hour + event.start.minute / 60.0
        end_value = event.end.hour + event.end.minute / 60.0
        y_value = start_value if start_value > 12 else start_value + 24
        bed_time_graph.y.append(y_value)
        getup_time_graph.y.append(end_value+24.0)
        bed_time_graph.text.append(event.start.strftime("%I:%M"))
        getup_time_graph.text.append(event.end.strftime("%I:%M"))

    fig = go.Figure()

    fig.update_layout(legend_title_text='Sleep Pattern',
                      yaxis_title='Time', xaxis_title='Date',
                      title=utils.set_title("Sleep Pattern"))
    # fig.update_yaxes(rangemode="tozero")
    fig.update_yaxes(
        ticktext=["10 PM", "12 AM", "2AM", "5AM", "9AM"],
        tickvals=[22, 24, 26, 29, 33],
    )
    fig.add_trace(go.Scatter(
        x=bed_time_graph.x,
        y=bed_time_graph.y,
        mode="lines+markers+text",
        text=bed_time_graph.text,
        name=getup_time_graph.title,
        # marker=dict(color=gra),
        textposition="top center"
    ))
    fig.add_trace(go.Scatter(
        x=getup_time_graph.x,
        y=getup_time_graph.y,
        mode="lines+markers+text",
        text=getup_time_graph.text,
        name=getup_time_graph.title,
        marker=dict(color='Red'),
        textposition="top center"
    ))

    return fig


content = html.Div([
    dcc.Graph(id="sleep_pattern_graph", figure=get_sleep_time_graph((date.today()-timedelta(days=31)).isoformat(),
                                                                    date.today().isoformat())),
    dcc.Graph(id="sleep_duration_graph", figure=get_sleep_duration_graph((date.today()-timedelta(days=31)).isoformat(),
                                                                    date.today().isoformat()))

], className="panel panel-default")


