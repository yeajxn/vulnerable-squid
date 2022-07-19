import mysql.connector
from datetime import datetime
from . import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD
from .hashing import hash_password, check_hash

def connector():
    c = mysql.connector.connect(
        host='mysqldb', 
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD
        )
    return c

def create_db():
    with connector() as c:
        cur = c.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                userID int AUTO_INCREMENT NOT NULL, 
                username varchar(50) UNIQUE NOT NULL, 
                email varchar(100) UNIQUE NOT NULL, 
                name varchar(50), 
                password varchar(100) NOT NULL, 
                user_type varchar(1) NOT NULL,
                PRIMARY KEY (userID)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS card (
                cardID int AUTO_INCREMENT, 
                name varchar(40) NOT NULL, 
                image varchar(100), 
                type varchar(10) NOT NULL, 
                text varchar(180), 
                attack INTEGER, 
                hp INTEGER, 
                price FLOAT NOT NULL, 
                quantity INTEGER NOT NULL,
                PRIMARY KEY (cardID)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cart (
                userID int NOT NULL, 
                cardID int NOT NULL, 
                quantity INTEGER NOT NULL, 
                PRIMARY KEY (userID, cardID), 
                FOREIGN KEY(userID) REFERENCES user (userID), 
                FOREIGN KEY(cardID) REFERENCES card (cardID)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                orderID int NOT NULL, 
                userID int NOT NULL, 
                date DATETIME NOT NULL, 
                total FLOAT NOT NULL, 
                PRIMARY KEY (orderID), 
                FOREIGN KEY(userID) REFERENCES user (userID)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS card_orders (
                orderID int NOT NULL, 
                cardID int NOT NULL, 
                quantity INTEGER NOT NULL, 
                unit_price FLOAT NOT NULL, 
                PRIMARY KEY (orderID, cardID), 
                FOREIGN KEY(orderID) REFERENCES orders (orderID), 
                FOREIGN KEY(cardID) REFERENCES card (cardID)
            )
            """
        )
        c.commit()
        print('Created databases.')   

def reset_db():
    with connector() as c:
        cur = c.cursor()
        cur.execute(
            """
            DROP TABLE IF EXISTS card_orders
            """
        )
        cur.execute(
            """
            DROP TABLE IF EXISTS orders
            """
        )
        cur.execute(
            """
            DROP TABLE IF EXISTS cart
            """
        )
        cur.execute(
            """
            DROP TABLE IF EXISTS card
            """
        )
        cur.execute(
            """
            DROP TABLE IF EXISTS user
            """
        )
        c.commit()
    create_db()
    create_admin()


def create_admin(username="admin"):
    with connector() as c:
        cur = c.cursor()
        cur.execute('SELECT * FROM user WHERE username = %s', (username,))
        admin = cur.fetchone()
        if admin:
            return
        pwd = hash_password('password')
        cur.execute('INSERT INTO user (username, email, password, user_type) VALUES (%s, %s, %s, %s)',
        ("admin", "admin@mail.com.", pwd, "A")
        )
        c.commit()

def commit_query(sql):
    with connector() as c:
        cur = c.cursor()
        cur.execute(sql)
        c.commit()
        return cur.lastrowid

def get_query(sql, multi=True):
    with connector() as c:
        cur = c.cursor()
        cur.execute(sql)
        if multi:
            return cur.fetchall()
        else:
            return cur.fetchone()

from .models import Card, Order, Cart, User, CardOrders

"""
User
"""
def getUser(userID=None, username=None, email=None):
    if userID:
        sql = f'SELECT * FROM user WHERE userID = {userID}'
        user = get_query(sql, False)
    elif not (username or email):
        return
    else:
        names = {'username':username, 'email':email}
        sql = 'SELECT * FROM user WHERE'
        add_or = False
        for key in names:
            if names[key]:
                if add_or: sql += ' OR'
                sql += f' {key}="{names[key]}"'
                add_or = True
        user = get_query(sql, False)
    if user:
        return User(userID=user[0], username=user[1], email=user[2], name=user[3], password=user[4], user_type=user[5])

def create_user(username, email, password, user_type='U'):
    sql = f'INSERT INTO user (username, email, password, user_type) VALUES ("{username}", "{email}", "{password}", "{user_type}")'
    commit_query(sql)
    sql = f'SELECT * FROM user WHERE "username" = "{username}"'
    user = get_query(sql, False)
    return user

def check_login(username:str, password:str):
    sql = f'SELECT userID, password FROM user WHERE username = "{username}"'
    user = get_query(sql, multi=False)
    if user and check_hash(user[1], password):
        return getUser(userID=user[0])


"""
Card
"""
def get_card(id:int):
    if not id:
        return
    sql = f'SELECT * FROM card WHERE "cardID" = {id}'
    card_sql = get_query(sql, False)
    card = Card(card_sql[0], card_sql[1], card_sql[2], card_sql[3], card_sql[4],card_sql[5], card_sql[6], card_sql[7], card_sql[8])
    return card

def get_cards(search:str=None):
    if not search:
        sql = f'SELECT * FROM card WHERE "quantity" > 0'
    else:
        sql = f'SELECT * FROM card WHERE "quantity" > 0 AND "name" LIKE "%{search}%" OR  "text" LIKE "%{search}%"'
    cards_tuple = get_query(sql)
    cards = [Card(card[0], card[1], card[2], card[3], card[4],card[5], card[6], card[7], card[8]) for card in cards_tuple]
    return cards

def create_card(name:str, image:str, type:str, text:str, attack:int, hp:int, price:float, quantity:int):
    sql = f'INSERT INTO card (name, image, type, text, attack, hp, price, quantity) VALUES ("{name}", "{image}", "{type}", "{text}", {attack}, {hp}, {price}, {quantity})'
    cardid = commit_query(sql)
    sql = f'SELECT * from card WHERE cardID = {cardid}'
    card = get_query(sql, False)
    return card

"""
Cart
"""
def add_to_cart(cardID, userID, quantity):
    sql = f'SELECT quantity FROM cart WHERE cardID = {cardID} AND userID = {userID}'
    exists = get_query(sql, False)
    if exists:
        quantity = exists[0] + quantity
        sql = f'UPDATE cart SET quantity = {quantity} WHERE cardID = {cardID} and userID = {userID}'
        commit_query(sql)
    else:
        sql = f'INSERT INTO cart (cardID, userID, quantity) VALUES ({cardID}, {userID}, {quantity})'
        commit_query(sql)

def delete_cart(userID:int):
    sql = f'DELETE FROM cart WHERE userID = {userID}'
    commit_query(sql)

def delete_cart_item(userID:int, cardID:int):
    sql = f'DELETE FROM cart WHERE userID = {userID} AND cardID = {cardID}'
    commit_query(sql)

def get_cart(userID:int):
    sql = f'SELECT * FROM cart WHERE userID = {userID}'
    cart_tuple = get_query(sql)
    if cart_tuple:
        cart = [Cart(item[0], item[1], item[2]) for item in cart_tuple]
        return cart

def get_cart_item(userID:int, cardID:int):
    sql = f'SELECT * FROM cart WHERE userID = {userID} AND cardID = {cardID}'
    item = get_query(sql, False)
    if item:
        return Cart(item[0], item[1], item[2])

"""
Order
"""
def create_order(userID:int, date:datetime = datetime.now(), total=0) -> int:
    with connector() as c:
        cursor = c.cursor()
        sql = f"INSERT INTO 'orders' (userID, date, total) VALUES ({userID}, '{date}', {total})"
        cursor.execute(sql)
        c.commit()
        return cursor.lastrowid

def delete_order(orderid:int):
    sql = f'DELETE FROM orders WHERE orderID = {orderid}'
    commit_query(sql)

def get_order(orderID):
    sql = f'SELECT * FROM orders WHERE orderID = {orderID}'
    orders = get_query(sql, multi=False)
    return Order(orders[0],orders[1],orders[2], orders[3])

def get_orders(userID:int):
    sql = f'SELECT * FROM orders WHERE userID = {userID}'
    return [Order(orders[0],orders[1],orders[2], orders[3]) for orders in get_query(sql)] 

"""
CardOrders
"""
def create_card_orders(orderID, cardID, quantity, unit_price):
    sql = f'INSERT INTO card_orders (orderID, cardID, quantity, unit_price) VALUES ({orderID}, {cardID}, {quantity}, {unit_price})'
    return commit_query(sql)

# db = sqlite3_db('/home/code/Documents/card.db')
# user = db.getUser(username="admin")
# print(user.password)