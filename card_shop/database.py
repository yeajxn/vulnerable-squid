import sqlite3
from datetime import datetime

from sqlalchemy import false
from . import DATABASE_URI

def connector():
    return sqlite3.connect(DATABASE_URI)

def commit_query(sql):
    c = sqlite3.connect(DATABASE_URI)
    cursor = c.cursor()
    cursor.execute(sql)
    c.commit()
    return cursor.lastrowid

def get_query(sql, multi=True):
    c = sqlite3.connect(DATABASE_URI)
    cursor = c.cursor()
    cursor.execute(sql)
    if multi:
        return cursor.fetchall()
    else:
        return cursor.fetchone()

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
    c = connector()
    sql = f'INSERT INTO user (username, email, password, user_type) VALUES ("{username}", "{email}", "{password}", "{user_type}")'
    c.execute(sql)
    c.commit()
    sql = f'SELECT * FROM user WHERE username = "{username}"'
    user = c.execute(sql).fetchone()
    return user

def check_login(username:str, password:str):
    sql = f'SELECT * FROM user WHERE username = "{username}" and password = "{password}"'
    user = get_query(sql, multi=False)
    if user:
        print(f'{user=}')
        return getUser(userID=user[0])
        
"""
Card
"""

def get_card(id:int):
    c = connector()
    if not id:
        return
    sql = f'SELECT * FROM card WHERE cardID = {id}'
    card_sql = c.execute(sql).fetchone()
    card = Card(card_sql[0], card_sql[1], card_sql[2], card_sql[3], card_sql[4],card_sql[5], card_sql[6], card_sql[7], card_sql[8])
    return card

def get_cards(search:str=None):
    c = connector()
    if not search:
        sql = f'SELECT * FROM card WHERE quantity > 0'
    else:
        sql = f'SELECT * FROM card WHERE quantity > 0 AND name LIKE "%{search}%" OR  text LIKE "%{search}%"'
    cards_tuple = c.execute(sql).fetchall()
    cards = [Card(card[0], card[1], card[2], card[3], card[4],card[5], card[6], card[7], card[8]) for card in cards_tuple]
    return cards

def create_card(name:str, image:str, type:str, text:str, attack:int, hp:int, price:float, quantity:int):
    c = connector()
    cursor = c.cursor()
    sql = f'INSERT INTO card (name, image, type, text, attack, hp, price, quantity) VALUES ("{name}", "{image}", "{type}", "{text}", {attack}, {hp}, {price}, {quantity})'
    cursor.execute(sql)
    c.commit()
    sql = f'SELECT * from card WHERE cardID = {cursor.lastrowid}'
    card = cursor.execute(sql)
    return card

"""
Cart
"""

def add_to_cart(cardID, userID, quantity):
    c = connector()
    sql = f'SELECT quantity FROM cart WHERE cardID = {cardID} AND userID = {userID}'
    exists = c.execute(sql).fetchone()
    if exists:
        quantity = exists[0]+1
        sql = f'UPDATE cart SET quantity = {quantity} WHERE cardID = {cardID} and userID = {userID}'
        c.execute(sql)
        c.commit()
    else:
        sql = f'INSERT INTO cart (cardID, userID, quantity) VALUES ({cardID}, {userID}, {quantity})'
        c.execute(sql)
        c.commit()

def delete_cart(userID:int):
    c = connector()
    sql = f'DELETE FROM cart WHERE userID = {userID}'
    c.execute(sql)
    c.commit()

def delete_cart_item(userID:int, cardID:int):
    c = connector()
    sql = f'DELETE FROM cart WHERE userID = {userID} AND cardID = {cardID}'
    c.execute(sql)
    c.commit()

def get_cart(userID:int):
    c = connector()
    sql = f'SELECT * FROM cart WHERE userID = {userID}'
    cart_tuple = c.execute(sql).fetchall()
    cart = [Cart(item[0], item[1], item[2]) for item in cart_tuple]
    return cart

def get_cart_item(userID:int, cardID:int):
    c = connector()
    sql = f'SELECT * FROM cart WHERE userID = {userID} AND cardID = {cardID}'
    item = c.execute(sql).fetchone()
    if item:
        return Cart(item[0], item[1], item[2])

"""
Order
"""
def create_order(userID:int, date:datetime = datetime.now(), total=0) -> int:
    c = connector()
    cursor = c.cursor()
    sql = f"INSERT INTO 'order' (userID, date, total) VALUES ({userID}, '{date}', {total})"
    cursor.execute(sql)
    c.commit()
    return cursor.lastrowid

def delete_order(orderid:int):
    sql = f'DELETE FROM "order" WHERE orderID = {orderid}'
    commit_query(sql)

def get_order(orderID):
    sql = f'SELECT * FROM "order" WHERE orderID = {orderID}'
    order = get_query(sql, multi=False)
    return Order(order[0],order[1],order[2], order[3])

def get_orders(userID:int):
    sql = f'SELECT * FROM "order" WHERE userID = {userID}'
    return [Order(order[0],order[1],order[2], order[3]) for order in get_query(sql)] 

"""
CardOrders
"""
def create_card_orders(orderID, cardID, quantity, unit_price):
    sql = f'INSERT INTO card_orders (orderID, cardID, quantity, unit_price) VALUES ({orderID}, {cardID}, {quantity}, {unit_price})'
    return commit_query(sql)

# db = sqlite3_db('/home/code/Documents/card.db')
# user = db.getUser(username="admin")
# print(user.password)