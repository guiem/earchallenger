import sqlite3
import os
import datetime

class DatabaseManager(object):

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.cur = self.conn.cursor()
        self.conn.commit()

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur
    
    def __del__(self):
        self.conn.close()

class EarChallengerDB(DatabaseManager):

    def __init__(self,db):
        super(EarChallengerDB, self).__init__(db)
        self.query('''
            CREATE TABLE IF NOT EXISTS stats(id INTEGER PRIMARY KEY, datestamp TEXT,correct INTEGER, num_trials INTEGER, num_hints INTEGER, num_notes INTEGER, instrument TEXT, sequence TEXT, user_rating INTEGER)
            ''')
        self.conn.commit()

    def insert_stat(self,correct,num_trials,num_hints,num_notes,instrument,sequence,user_rating):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = '''INSERT INTO stats(datestamp,correct,num_trials,num_hints, num_notes,instrument,sequence,user_rating)
            VALUES('%s',%s,%s,%s,%s,'%s','%s',%s)''' % (timestamp,str(correct),str(num_trials),str(num_hints),str(num_notes),instrument,sequence,str(user_rating))
        self.query(query)

    def get_num_games(self):
        res = self.query('''SELECT COUNT(*) FROM stats''')
        return res.fetchone()[0]

