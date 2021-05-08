from utils import utils
# from . import params

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from commons.utils import get_data


def get_sleep_time_graph(par=None):

    select_query= "select * from events_sleepentry ;"
    rows = get_data(select_query)
    data={
        'x' : [],
        'y' : [],
        'name' : 'Sleep Duration'
    }
    for row in rows:
        data['x'].append(row['date'])
        data['y'].append(row['duration'])
    
    fig = go.Figure()
    
    fig.update_layout(legend_title_text='Sleep Duration',
                        yaxis_title='Sleep Duration (hours)', xaxis_title='Date',
                        title=utils.set_title("Sleep Duration"), uirevision='events_sleepentry')
    fig.update_yaxes(rangemode="tozero")
    
    fig.add_trace(go.Scatter(
        x=data['x'],
        y=data['y'],
        name=data['name'],
    ))
    return fig

content = html.Div([
    dcc.Graph(id="sleep_time_graph", figure=get_sleep_time_graph())

], className="panel panel-default")


