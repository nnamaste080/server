import datetime
import sqlite3
import time


class Worker():
    def __init__(self):
        self.conn = sqlite3.connect('mydb.db')
        self.cursor_obj = self.conn.cursor()
        try:
            self.create_table()
        except sqlite3.OperationalError:
            pass

        # self.create_table()

    def create_table(self):
        # Creating table
        table = """CREATE TABLE workers(
            workername VARCHAR(255) unique NOT NULL,
            benchmark VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL,
            range VARCHAR(255) NOT NULL,
            timestamp integer NOT NULL
            ); """

        self.cursor_obj.execute(table)
        self.conn.commit()

    def insert_worker_data(self, name, benchmark, status, range):
        ts = time.time()
        ts = int(ts)
        cmmd = f"""insert into workers(workername,benchmark,status,range,timestamp) values('{name}','{benchmark}','{status}','{range}','{ts}')"""

        self.cursor_obj.execute(cmmd)

        self.conn.commit()

    def get_all_worker_data(self):
        cmmd = f"""select * from workers"""
        self.cursor_obj.execute(cmmd)

        data = self.cursor_obj.fetchall()

        return list(data)

    def delete_data(self, name):
        cmd = f"""delete from workers where workername='{name}'"""
        self.cursor_obj.execute(cmd)

        self.conn.commit()

    def update_status(self, name, status):
        ts = time.time()
        ts = int(ts)

        cmd = f"""update workers set status='{status}',timestamp='{ts}' where workername='{name}'"""
        self.cursor_obj.execute(cmd)

        self.conn.commit()

    def update_connection(self, name):
        ts = time.time()
        ts = int(ts)

        cmd = f"""update workers set timestamp='{ts}' where workername='{name}'"""
        self.cursor_obj.execute(cmd)

        self.conn.commit()

    def is_exits(self, name):
        cmd = f"""select workername from workers where workername='{name}'"""
        self.cursor_obj.execute(cmd)
        data = self.cursor_obj.fetchall()

        return True if len(list(data)) > 0 else False

    def close_conn(self):
        self.conn.close()


class Job():
    def __init__(self):
        self.conn = sqlite3.connect('mydb.db')
        self.cursor_obj = self.conn.cursor()

    def create_table(self):
        # Creating table
        table = """CREATE TABLE jobs(
            workername VARCHAR(255) unique NOT NULL,
            benchmark VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL,
            range VARCHAR(255) NOT NULL,
            timestamp integer NOT NULL
            ); """

        self.cursor_obj.execute(table)
        self.conn.commit()

    def create(self):
        pass

    def delete(self):
        pass

    def close_conn(self):
        self.conn.close()


# w = Worker()
# w.delete_data('pc3')
# w.close_conn()
