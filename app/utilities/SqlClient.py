# pip install mysqlclient
import MySQLdb
from configurations.configs import Creds
import logging


class dbMysql:
    # , host: str = 'localhost', user: str = None, passwd: str = None, db: str = None, conv: bool = True
    def __init__(self):
        self.host = Creds.MYSQL_HOST
        self.db = Creds.MYSQL_DB
        self.password = Creds.MYSQL_PASSWORD
        self.user = Creds.MYSQL_USER
        # conv = conversions.copy()#
        # if conv:
        #     conv[246] = float  # convert decimals to floats
        #     conv[7] = str  # convert dates to strings
        #     conv[10] = str
        # self.conn.cursor()
        self.conn = MySQLdb.connect(host=self.host,  # your host, usually localhost
                                    user=self.user,  # your username
                                    passwd=self.password,  # your password
                                    db=self.db,  # conv=conv
                                    )

    def close(self):
        return self.conn.close()

    def commit(self):
        return self.conn.commit()

    def mysql_cursor(self):
        return self.conn.cursor()

    def INSERT(self, query):
        cursor = self.mysql_cursor()
        return_body = {}
        try:
            cursor.execute(query)
            self.commit()
            logging.info('Data inserted to db')
        except Exception as e:
            logging.error(e)
            return_body['error'] = e
            return_body['failed'] = True
        finally:
            return return_body

    def SELECT(self, query):
        cursor = self.mysql_cursor()
        return_body = {}
        try:
            cursor.execute(query)
            return_body['data'] = self.mysql_fetchall(cursor)
        except Exception as e:
            return_body['error'] = f'{e}'
            return_body['failed'] = True
        finally:
            return return_body

    def SELECT_LOGIN(self, query):
        cursor = self.mysql_cursor()
        return_body = {}
        try:
            cursor.execute(query)
            return_body['data'] = self.mysql_fetchall(cursor)
            if not return_body['data']:
                return_body['error'] = 'No account found'
        except Exception as e:
            return_body['error'] = f'{e}'
            return_body['failed'] = True
        finally:
            return return_body

    def mysql_fetchall(self, cursor):
        row_headers = [x[0] for x in cursor.description]  # this will extract row headers
        rv = cursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json_data

    def if_exist(self, table: str, column: list = [], value: list = []):
        add = ''
        subquery = ''
        if len(column) > 1:
            for i in range(len(column)):
                if i == 1:
                    add = 'AND'
                subquery = f'{subquery} {add} {column[i]} = {value[i]}'
            q = f"select 1 from {table} WHERE {subquery}"
        else:
            q = f"select 1 from {table} WHERE {column[0]} = '{value[0]}' limit 1"
        return self.mysql_execute(q, False)
