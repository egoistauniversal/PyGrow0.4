import sqlite3
import sys


class Database:
    def __init__(self):
        try:
            self.connection = sqlite3.connect('database/db.sqlite')
            self.cur = self.connection.cursor()
        except sqlite3.Error as e:
            sys.exit(e)

    def query_select_all_modules(self):
        try:
            self.cur.execute('SELECT programs.program_id, programs.module_id, programs.name, programs.pin, '
                             'programs.time_on, programs.time_off, programs.state, programs.automatic '
                             'FROM programs '
                             'WHERE programs.enabled=1')
        except sqlite3.Error as e:
            sys.exit(e)

        return self.cur.fetchall()
