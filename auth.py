import sqlite3
from flask import session


DB_FILE_PATH = 'data/data.db'

class Auth:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def create_user(self, username, password):
        '''Create a user with given password'''
        data = (username, password)
        self.cursor.execute('insert into user (username, password) values (?, ?)', data)
        self.conn.commit()
        self.conn.close()


    def login(self, username, password):
        '''If we have a user with the given user name and password, return True.
        Otherwise, return False.'''
        userdata = (username, password)
        isDataIn = False
        conn = sqlite3.connect(DB_FILE_PATH)
        c = conn.cursor()
        result = c.execute('SELECT user.username, user.password FROM user')
        row = result.fetchall()
        if userdata in row:
            isDataIn = True
            session['username'] = username

        self.conn.close()
        return isDataIn

    def logout(self):
        session.pop('username', None)


    def is_logged_in(self):
        return 'username' in session


    def get_current_user(self):
        x = session['username']
        name = (x,)
        self.cursor.execute('''SELECT user.user_id FROM user WHERE username = (?)''', name)
        y = self.cursor.fetchone()
        self.conn.close()
        userid = int(y[0])
        return userid
        

    def has_user(self, username):
        self.cursor.execute('select count(1) from user where username = ?', (username,))
        row = self.cursor.fetchone()
        count = row[0]
        self.conn.close()
        return count > 0

