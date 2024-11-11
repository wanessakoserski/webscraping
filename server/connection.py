import pyodbc

class ServerConnection:
    def __init__(self, database: str):
        self.server = "DESKTOP-EAP8059"
        self.database = database


    def _get_server_connection(self):
        sqlserver_conncetion = (
            "Driver={SQL Server};"
            fr"Server={self.server};"
            f"Database={self.database};"
        )

        return sqlserver_conncetion


    def check_table_exists(self, table: str) -> bool:
        try: 
            connection = pyodbc.connect(self._get_server_connection())
            cursor = connection.cursor()

            query = f"""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_NAME = '{table}'
            """
            cursor.execute(query)

            exists = cursor.fetchone()[0] > 0

            cursor.close()
            connection.close()

            return exists
        except pyodbc.Error as ex:
            print("Server Error: ", ex)
    

    def create_table(self, table: str, columns: str) -> bool:
        try:
            connection = pyodbc.connect(self._get_server_connection())
            cursor = connection.cursor()

            query = f"""
            CREATE TABLE {table} (
                {columns}
            )
            """
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return True
        except pyodbc.Error as ex:
            print("Server Error: ", ex)

    
    def drop_table(self, table: str) -> bool:
        try: 
            if self.check_table_exists(table):
                connection = pyodbc.connect(self._get_server_connection())
                cursor = connection.cursor()

                query = f"DROP TABLE {table}"
                cursor.execute(query)
                connection.commit()

                cursor.close()
                connection.close()

                print(f"Drop table {table}")

                return True
            else:
                print(f"Table {table} does not exist")

                return False
        except pyodbc.Error as ex:
            print("Server Error: ", ex)


    def select(self, table: str, columns='*', joins=None, where=None, group_by=None, order_by=None, limit=None) -> list:
        try:
            connection = pyodbc.connect(self._get_server_connection())
            cursor = connection.cursor()

            query = f"SELECT {columns} FROM {table}"

            if joins:
                query += f" {joins}"

            if where:
                query += f" WHERE {where}"

            if group_by:
                query += f" GROUP BY {group_by}"

            if order_by:
                query += f" ORDER BY {order_by}"

            if limit:
                query += f" OFFSET 0 ROW FETCH NEXT {limit} ROWS ONLY"

            cursor.execute(query)
            rows = cursor.fetchall()

            cursor.close()
            connection.close()

            return rows
        except pyodbc.Error as ex:
            print("Server Error: ", ex)


    def insert(self, table: str, columns: str, values: str) -> bool:
        try:
            connection = pyodbc.connect(self._get_server_connection())
            cursor = connection.cursor()

            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return True
        except pyodbc.Error as ex:
            print("Server Error: ", ex)


    def update(self, table: str, set: str, where=None) -> bool:
        try:
            connection = pyodbc.connect(self._get_server_connection())
            cursor = connection.cursor()

            query = f"UPDATE {table} SET {set}"
            if where:
                query += f" WHERE {where}"
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return True
        except pyodbc.Error as ex:
            print("Server Error: ", ex)  


    def delete(self, table: str, where: str) -> bool:
        try:
            connection = pyodbc.connect(self._get_server_connection())
            cursor = connection.cursor()

            query = f"DELETE FROM {table} WHERE {where}"
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()
        except pyodbc.Error as ex:
            print("Server Error: ", ex) 
        