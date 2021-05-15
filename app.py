# from dashboards import sleep_time, routine, mess, major_events, workout_events
from dashboards.sleep_pattern import SleepPattern
from dashboards.workout_events import WorkoutGraphs
from dashboards.mess_graphs import MessGraphs
from layout import get_layout
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from commons.cache import cache
from datetime import datetime, date, timedelta

app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"]
)
cache.init_app(
    app.server, 
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache-directory',
    }
)

app.title = "Unacademy Analytics"
app.config['suppress_callback_exceptions'] = True
server = app.server


app.layout = get_layout()

default_start_date = (date.today() - timedelta(days=31)).isoformat()
default_end_date = (date.today() + timedelta(days=1)).isoformat()
workout_graphs = WorkoutGraphs()
sleep_pattern = SleepPattern(default_start_date, default_end_date )
mess_graphs = MessGraphs(default_start_date, default_end_date)

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname'), Input('session_id', 'children')])
def display_dashboard(pathname, session_id):
    if pathname == '/':
        return sleep_pattern.content
    # elif pathname == '/sleep-time':
    #     return sleep_time.content
    # elif pathname == '/routine':
    #     return routine.content
    elif pathname == '/mess':
        return mess_graphs.content
    # elif pathname == '/major_events':
    #     return major_events.content
    elif pathname == '/sleep_pattern':
        return sleep_pattern.content
    elif pathname == '/workout_events':
        return workout_graphs.CONTENT
    else:
        return html.Div([
            html.Div('You are on page {}'.format(pathname))
        ])


@app.callback(
    [Output("sleep_pattern_graph", 'figure'),
     Output("sleep_duration_graph", 'figure')],
    [Input(component_id='date-picker', component_property='start_date'),
        Input(component_id='date-picker', component_property='end_date'),]
)
def update_sleep_pattern_graph(start_date, end_date):
    sp = SleepPattern(start_date, end_date)
    return sp.get_sleep_time_graph(), sp.get_sleep_duration_graph()


@app.callback(
    Output("workouts_graph", 'figure'),
    [Input(component_id='date-picker', component_property='start_date'),
        Input(component_id='date-picker', component_property='end_date'),]
)
def update_workout_events_graph(start_date, end_date):
    return workout_graphs.get_workout_events_graph(start_date, end_date)


@app.callback(
    [Output(mess_graphs.MESS_EVENTS_GRAPH_ID, 'figure'),
     Output(mess_graphs.WEEKLY_MESS_EVENTS_GRAPH_ID, 'figure'),
     Output(mess_graphs.MONTHLY_MESS_EVENTS_GRAPH_ID, 'figure')],
    [Input(component_id='date-picker', component_property='start_date'),
     Input(component_id='date-picker', component_property='end_date'),]
)
def update_workout_events_graph(start_date, end_date):
    mg = MessGraphs(start_date, end_date)
    return mg.get_mess_graph(), mg.get_weekly_mess_graph(), mg.get_monthly_mess_graph()


if __name__ == '__main__':
    app.run_server(debug=True)
