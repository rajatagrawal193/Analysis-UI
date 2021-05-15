from models.calendar_event import CalendarEvent
from models.graph import Graph
import plotly.graph_objects as go
from datetime import date

def get_events_by_week(events: [CalendarEvent]) -> dict[str, [CalendarEvent]]:
    weekly_segregated_events = {}
    for event in events:
        year, week_no, week_day_no = event.start.date().isocalendar()
        week_start = date.fromisocalendar(year, week_no, 1).strftime("%b %d")
        week_end = date.fromisocalendar(year, week_no, 7).strftime("%b %d")

        # week = f"{week_no} Week {week_start}-{week_end}"
        week = f"{week_start}-{week_end}"

        if week not in weekly_segregated_events:
            weekly_segregated_events[week] = [event]
        else:
            weekly_segregated_events[week].append(event)
    return weekly_segregated_events


def get_events_by_month(events):
    events_by_month = {}
    for event in events:
        month = str(event.start.date().strftime("%b '%y"))
        if month not in events_by_month:
            events_by_month[month] = [event]
        else:
            events_by_month[month].append(event)
    return events_by_month


def generate_weekly_frequency_graph(title, calendar_events, start_date, end_date) -> go.Figure():
    delta = end_date - start_date
    total_days = delta.days
    avg = len(calendar_events) / total_days * 7.0
    graph = Graph(f"Weekly {title} Events | Avg: {avg} ", "Frequency", "Week No")
    weekly_segregated_events = get_events_by_week(calendar_events)
    for week, events in weekly_segregated_events.items():
        graph.x.append(week)
        graph.y.append(len(events))

    fig = go.Figure(data=[go.Bar(x=graph.x, y=graph.y, name=graph.title)], layout=dict(title=dict(text=graph.title)))
    # fig = graph.update_fig_layout(fig)
    return fig


def generate_monthly_frequency_graph(title, calendar_events, start_date, end_date):
    delta = end_date - start_date
    total_days = delta.days
    avg = len(calendar_events) / total_days * 30.0
    graph = Graph(f"Monthly {title} Events | Avg: {avg}", "Frequency", "Month")
    events_by_month = get_events_by_month(calendar_events)
    for month, events in events_by_month.items():
        graph.x.append(month)
        graph.y.append(len(events))

    fig = go.Figure(data=[go.Bar(x=graph.x, y=graph.y, name=graph.title)], layout=dict(title=dict(text=graph.title)))
    # fig = graph.update_fig_layout(fig)
    return fig

