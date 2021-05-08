from utils import utils
# from . import params

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from commons.utils import get_data


def get_mess_graph(par=None):

    select_query= "select * from events_mess ;"
    rows = get_data(select_query)
    data={
        'x' : [],
        'y' : [],
        'name' : 'Sleep Duration'
    }
    for row in rows:
        data['x'].append(row['date'])
        data['y'].append(row['time'])
    
    fig = go.Figure()
    
    fig.update_layout(legend_title_text='Mess',
                        yaxis_title='Time (24 hour)', xaxis_title='Date',
                        title=utils.set_title("Mess"), uirevision='events_mess')
    fig.update_yaxes(rangemode="tozero")
    
    fig.add_trace(go.Scatter(
        x=data['x'],
        y=data['y'],
        name=data['name'],
        marker=dict(size=8),
        mode='markers'
    ))
    return fig

content = html.Div([
    dcc.Graph(id="mess_graph", figure=get_mess_graph())

], className="panel panel-default")


