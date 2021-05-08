from utils import utils
# from . import params

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from commons.utils import get_data


def get_daily_routine_graph(par=None):

    # select_query= "select * from events_dayreview where date >= '2021-01-25';"
    select_query= "select * from events_dayreview order by date;"

    rows = get_data(select_query)
    
    fig = go.Figure()
    
    fig.update_layout(legend_title_text='Routine Items',
                        yaxis_title='Time (24 hour)', xaxis_title='Date',
                        title=utils.set_title("Daily Routine"), uirevision='events_dayreview')
    fig.update_yaxes(rangemode="tozero")
    
    field_map = {
        'wokeup' : 'Wake up time',
        'workout' : 'Workout',
        # 'breakfast' : 'Breakfast at',
        # 'lunch' : 'Lunch at',
        # 'dinner' : 'Dinner at',
        # 'mess_pre_sleep' : 'Mess', 
        # 'sleep_start' : 'Slept at',

    }
    graph_data = {}
    for row in rows:
        for key in field_map.keys():
            if key not in graph_data:
                graph_data[key] ={
                    'x': [],
                    'y': [],
                    
                }
            graph_data[key]['x'].append(row['date'])
            graph_data[key]['y'].append(row[key])


    for key, data in graph_data.items():
        fig.add_trace(go.Scatter(
            x=data['x'],
            y=data['y'],
            name=field_map[key],
            mode='lines+markers'
            # connectgaps=True 
        ))
    return fig

content = html.Div([
    dcc.Graph(id="daily_routine_graph", figure=get_daily_routine_graph())

], className="panel panel-default")


