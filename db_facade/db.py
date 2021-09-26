import logging
import time

import psycopg2
from pgcopy import CopyManager


# from .db_clients import postgresql
print(locals())


class Postgresql_Client():

    @staticmethod
    def get_connection(db_url):
        connection = psycopg2.connect(db_url)
        return connection

    @staticmethod
    def execute_query(db_connection, query, data):
        cursor = db_connection.cursor()
        cursor.execute(query, data)
        db_connection.commit()
        cursor.close()

    @staticmethod
    def insert_rows(db_connection, table_name, rows):
        """
        Insert multiple rows of data.
        Args:
            db_connection: postgresql connection object
            table_name (str): Name of the table
            data (list(dict))
        """
        cursor = db_connection.cursor()

        first_row = rows[0]
        column_names = list(first_row)

        values = list(map(lambda row: tuple(row.values()), rows))

        try:
            copyManager = CopyManager(db_connection, table_name, column_names)
            copyManager.copy(values)
            db_connection.commit()
            cursor.close()

        except (Exception, psycopg2.Error) as error:
            cursor.close()
            raise error

    @staticmethod
    def fetch_many(db_connection, table_name, limit=None):

        query = None

        if (limit):
            query = f'SELECT * FROM {table_name} LIMIT {limit}'
        else:
            query = f'SELECT * FROM {table_name}'

        cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        result = cursor.fetchmany(limit)
        cursor.close()

        return result

    @staticmethod
    def is_connection_open(db_connection):
        if db_connection.closed == 0:
            return True

        return False



class DB():

    _connectors = {"postgresql": Postgresql_Client.get_connection}
    _inserters = {"postgresql": Postgresql_Client.insert_rows}
    _fetchers = {"postgresql": Postgresql_Client.fetch_many}
    _executers = {"postgresql": Postgresql_Client.execute_query}
    _connection_status_providers = {"postgresql": Postgresql_Client.is_connection_open}

    def __init__(self, url, db="postgresql"):
        self.db = db
        self.url = url
        self.connection = self.connect()

    def connect(self):
        connector = self._connectors[self.db]
        return connector(self.url)

    def insert_many(self, table_name, data):
        try:
            inserter = self._inserters[self.db]
            inserter(self.connection, table_name, data)
        except Exception as e:
            logging.error(
                f'DB - {self.db} - Insert many failed with error:{e}'
            )

    def fetch_many(self, table_name, limit=None):
        try:
            fetcher = self._fetchers[self.db]
            fetcher(self.connection, table_name, limit)
        except Exception as e:
            logging.error(
                f'DB - {self.db} - Fetch many failed with error:{e}'
            )

    def execute_query(self, query, data=None):
        try:
            executer = self._executers[self.db]
            executer(self.connection, query, data)
        except Exception as e:
            logging.error(
                f'DB - {self.db} - Execute query failed with error:{e}'
            )

    def is_connection_open(self):
        connection_status_provider = self._connection_status_providers[self.db]
        return connection_status_provider(self.connection)

    def keep_connection_open(self):

        while True:
            # Wait 5 mins
            time.sleep(60 * 5)

            if not self.is_connection_open():
                try:
                    self.retry_to_connect()
                except:
                    return

    def retry_to_connect(self):
        retry_limit = 10
        for retry_count in range(retry_limit):
            try:
                logging.info(
                    f'DB - {self.db} - Retrying to connect ({retry_count}/{retry_limit})'
                )
                self.connection = self.connect()
                if self.is_connection_open():
                    return

                # Wait 5 mins
                time.sleep(60 * 5)

            except Exception as e:
                logging.error(
                    f'DB - {self.db} - Failed while retrying to connect, with error:{e}'
                )
                raise Exception('Retry Failed!')

        logging.error(f'DB - {self.db} - Reached retry limit')
        raise Exception('Reached retry limit')
