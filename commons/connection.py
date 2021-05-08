from db import connection, config

metrics_db = connection.Connection(config.DATABASE['metrics'])
