from sqlalchemy import create_engine
from urllib.parse import quote as urlquote


class Connection:

    def __init__(self, config):
        self.username = config['user']
        self.db_type = config['db_type']
        self.password = urlquote(config['password'])
        self.host = config['host']
        self.db = config['db']
        self.port = config['port']
        self.connection = None
        self.engine = create_engine(self.__conn_str__(), pool_size=10, max_overflow=0,
                                    pool_recycle=3600)

    def __conn_str__(self):
        return "{0}://{1}:{2}@{3}:{4}/{5}".format(
            self.db_type, self.username, self.password, self.host, self.port, self.db)

    def initialize(self):
        self.engine = create_engine(self.__conn_str__(), pool_size=10, max_overflow=0,
                                    pool_recycle=3600)

    def connect(self):
        self.connection = self.engine.connect()

    def execute(self, query):
        with self.engine.connect() as connection:
            if query:
                try:
                    return connection.execute(query)
                except Exception as e:
                    print(str(e))
        return None

    def fetchall(self, query):
        proxy = self.execute(query)
        return proxy.fetchall() if proxy else []
