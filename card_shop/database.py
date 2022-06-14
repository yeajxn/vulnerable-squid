import sqlite3

def connector():
    return sqlite3.connect('/home/code/Documents/card.db')

def getUser(userID=None, username=None, email=None):
    c = connector()
    if not (userID or username or email):
        return
    names = {'userID':userID, 'username':username, 'email':email}
    sql = 'SELECT * FROM user WHERE'
    add_or = False
    for key in names:
        if names[key]:
            if add_or: sql += ' OR'
            if type(names[key]) is int:
                sql += f' {key}={names[key]}'
            else:
                sql += f' {key}="{names[key]}"'
            add_or = True
    user = c.execute(sql).fetchone()
    return User(user[0], user[1], user[2], user[3], user[4], user[5])

class User():
    def __init__(self, userID, username, email, name, password, user_type, create_user = None):
        self.__userID = userID
        self.__username = username
        self.__email = email
        self.__name = name
        self.__password = password
        self.__user_type = user_type
        self.__conn = connector()
        if create_user: self._create_user(username, email, password)
    
    def _create_user(self, username, email, password):
        sql = f'INSERT INTO user (username, email, password) VALUES ("{username}", "{email}", "{password}")'
        self.__conn.execute(sql)

    @property
    def userID(self):
        return self.__userID
    
    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @property
    def name(self):
        return self.__name

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new):
        self.__conn.execute(f'UPDATE user SET password="{new}" WHERE userID={self.__userID}')
        self.__conn.commit()
        self.__password = new

    @property
    def user_type(self):
        return self.__user_type

# db = sqlite3_db('/home/code/Documents/card.db')
# user = db.getUser(username="admin")
# print(user.password)