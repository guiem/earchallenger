import sqlite3
import os

class DatabaseManager(object):

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.cur = self.conn.cursor()
        self.query('''
            CREATE TABLE IF NOT EXISTS stats(id INTEGER PRIMARY KEY, datestamp TEXT,
            correct INTEGER, num_trials INTEGER, num_hints INTEGER, num_notes INTEGER, instrument TEXT, sequence TEXT, user_rating INTEGER)
            ''')
        self.conn.commit()

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur
    
    def __del__(self):
        self.conn.close()