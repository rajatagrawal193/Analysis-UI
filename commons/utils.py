
from .connection import metrics_db

def get_data(query):
    return metrics_db.fetchall(query)
