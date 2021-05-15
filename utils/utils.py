# import numpy as np
from datetime import datetime as dt


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
        'anchor': 'top'}
