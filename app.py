from dashboards import sleep_time, routine, mess, major_events, sleep_pattern, workout_events
from dashboards.workout_events import WorkoutGraphs
from layout import get_layout
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration
# from utils import inputs, utils
from commons.cache import cache
from commons.utils import get_data
import json
from datetime import datetime, timezone
# sentry_sdk.init(
#     dsn="https://4d893c46568c4722bc841f43a16ac642@errors.unacademy.com/42",
#     integrations=[FlaskIntegration()]
# )

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

workout_graphs = WorkoutGraphs()

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname'), Input('session_id', 'children')])
def display_dashboard(pathname, session_id):
    if pathname == '/':
        return sleep_time.content
    elif pathname == '/sleep-time':
        return sleep_time.content
    elif pathname == '/routine':
        return routine.content
    elif pathname == '/mess':
        return mess.content
    elif pathname == '/major_events':
        return major_events.content
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
    return sleep_pattern.get_sleep_time_graph(start_date, end_date), sleep_pattern.get_sleep_duration_graph(start_date,end_date)


@app.callback(
    [Output("workout_events_graph", 'figure')],
    [Input(component_id='date-picker', component_property='start_date'),
        Input(component_id='date-picker', component_property='end_date'),]
)
def update_workout_events_graph(start_date, end_date):
    return workout_graphs.get_workout_events_graph(start_date, end_date)

if __name__ == '__main__':
    app.run_server(debug=True)
