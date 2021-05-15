import numpy as np
from datetime import datetime as dt



# def sql_to_graph_data(data, tab_name, start_index=2):
#     # start_index = 3 if th_data else 2
#     mdata = {}
#     for item in data:
#         name = ""
#         for i in range(start_index, len(item)):
#             name = name + "%s " % (item[i])
#         if name in mdata:
#             mdata[name].append(item)
#         else:
#             mdata[name] = [item]
#     graph_data = []
#     for k in mdata:
#         if len(mdata[k]):
#             v = np.array(mdata[k])
#             if tab_name == 'threshold_graphs':
#                 graph_data.append(
#                     {'name': k, 'x': v[:, 0], 'y': np.divide(v[:, 1], v[:, 2]) * 100})
#             else:
#                 graph_data.append(
#                     {'name': k, 'x': v[:, 0], 'y': v[:, 1] / 1000.0})
#     return graph_data


def get_style(num):
    return {
        'width': '{}%'.format(num * 10),
        'margin': '0.5%'
    }


def set_title(title):
    return {
        'text': title,
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
