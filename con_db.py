import os

from dotenv import load_dotenv
from mysql import connector

load_dotenv()


class MariaDB:
    def __init__(self, host=os.getenv('DB_HOST'),
                 database=os.getenv('DB_NAME'),
                 user=os.getenv('DB_USER'),
                 password=os.getenv('DB_PASSWORD')):
        self._host = host
        self._database = database
        self._user = user
        self._password = password

    def updateServerStatus(self, data, types, where):
        try:
            fd = ''
            for key, value in data.items():
                if types[key] == 'str':
                    value_str = f"'{value}'"
                else:
                    value_str = f"{value}"
                fd += f"{key}={value_str},"
            fields = fd.rstrip(',')

            sql = f"UPDATE tbl_server SET {fields} WHERE {where}"
            res = self.update_sql(sql)
            return res
        except Exception as e:
            print(f"{e}")
            return 0

    def update_sql(self, query):
        conn = connector.connect(host=self._host, database=self._database, user=self._user, password=self._password)
        try:
            _cursor = conn.cursor()

            conn.start_transaction()
            _cursor.execute(query)
            res = _cursor.rowcount
            _cursor.close()
            conn.commit()

            conn.close()
            return res
        except connector.Error as error:
            conn.rollback()
            return 0
