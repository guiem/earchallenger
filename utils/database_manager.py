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
        if hasattr(self, 'conn'):
            self.conn.close()

class EarChallengerDB(DatabaseManager):

    def __init__(self,db):
        super(EarChallengerDB, self).__init__(db)
        self.query('''
            CREATE TABLE IF NOT EXISTS stats(id INTEGER PRIMARY KEY, datestamp TEXT,correct INTEGER, num_trials INTEGER, num_hints INTEGER, num_notes INTEGER, instrument TEXT, sequence TEXT, user_rating INTEGER)
            ''')
        self.query('''
           CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY, setting TEXT, value TEXT, type TEXT)
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

    def get_setting(self,setting_name):
        res = self.query("""SELECT value,type FROM settings WHERE setting = '%s'""" %(setting_name,))
        fetched = res.fetchone()
        if fetched:
            value = fetched[0]
            type = fetched[1]
            return eval(type+'('+str(value)+')')
        return None

    def set_setting(self,setting_name,value,type):
        res = self.query("""SELECT id FROM settings WHERE setting = '%s'""" %(setting_name,))
        fetched = res.fetchone()
        real_value = eval(type+'('+str(value)+')')
        if fetched:
            self.query("""UPDATE settings SET value = '%s' WHERE setting = '%s'""" %(real_value,setting_name))
        else:
            self.query("""INSERT INTO settings(setting,value,type) VALUES('%s','%s','%s')""" %(setting_name,real_value,type))
