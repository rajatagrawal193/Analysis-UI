from utils import utils
# from . import params

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from commons.utils import get_data


def get_major_events_graph(par=None):
 
    select_query= "select * from events_lifeevents where date<= '2020-12-31' and date>= '2020-01-01'order by date ;"
    rows = get_data(select_query)
    data={
        'x' : [],
        'y' : [],
        'hover' : [],
        'duration' : [],
        'name' : 'Sleep Duration'
    }
    for row in rows:
        data['x'].append(row['date'])
        data['y'].append(row['date'])
        data['hover'].append(row['description'])
        data['duration'].append(row['duration']*5)
    
    fig = go.Figure()
    
    fig.update_layout(legend_title_text='Timeline', height= 920,
                        yaxis_title='Time (24 hour)', xaxis_title='Date',
                        title=utils.set_title("Timeline"), uirevision='events_lifeevents')
    fig.update_yaxes(rangemode="tozero")
    
    fig.add_trace(go.Scatter(
        x=data['x'],
        y=data['y'],
        name=data['name'],
        text=data['hover'],
        marker_size = data['duration'],
        # marker=dict(size=8),
        mode='markers'
    ))
    return fig

content = html.Div([
    dcc.Graph(id="major_events_graph", figure=get_major_events_graph())

], className="panel panel-default")


