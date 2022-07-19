from .database import connector
from datetime import datetime

class Card:
    def __init__(self, cardID:int, name:str, image:str, type:str, text:str, attack:int, hp:int, price:float, quantity:int):
        self.__cardID = cardID
        self.__name = name
        self.__image = image
        self.__type = type
        self.__text = text
        self.__attack = attack
        self.__hp = hp
        self.__price = price
        self.__quantity = quantity

    @property
    def cardID(self):
        return self.__cardID
    
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new:str):
        c = connector()
        self.__name = new
        c.execute(f'UPDATE card SET name = "{new}" WHERE cardID={self.__cardID}')
        c.commit()

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, new):
        c = connector()
        self.__image = new
        c.execute(f'UPDATE card SET image = "{new}" WHERE cardID={self.__cardID}')
        c.commit()

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, new:str):
        c = connector()
        self.__name = new
        c.execute(f'UPDATE card SET type = "{new}" WHERE cardID={self.__cardID}')
        c.commit()

    @property
    def text(self):
        return self.__text
    
    @text.setter
    def type(self, new:str):
        c = connector()
        self.__name = new
        c.execute(f'UPDATE card SET text = "{new}" WHERE cardID={self.__cardID}')
        c.commit()
    
    @property
    def attack(self):
        return self.__attack

    @attack.setter
    def type(self, new:str):
        c = connector()
        self.__name = new
        c.execute(f'UPDATE card SET attack = {new} WHERE cardID={self.__cardID}')
        c.commit()

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def type(self, new:str):
        c = connector()
        self.__name = new
        c.execute(f'UPDATE card SET hp = {new} WHERE cardID={self.__cardID}')
        c.commit()

    @property
    def price(self):
        return self.__price
    
    @price.setter
    def type(self, new:str):
        c = connector()
        self.__name = new
        c.execute(f'UPDATE card SET price = {new} WHERE cardID={self.__cardID}')
        c.commit()

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, new:str):
        c = connector()
        self.__quantity = new
        c.execute(f'UPDATE card SET quantity = {new} WHERE cardID={self.__cardID}')
        c.commit()

class User():
    def __init__(self, userID, username, email, name, password, user_type='U'):
        self.__userID = userID
        self.__username = username
        self.__email = email
        self.__name = name
        self.__password = password
        self.__user_type = user_type

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
        c = connector()
        c.execute(f'UPDATE user SET password="{new}" WHERE userID={self.__userID}')
        c.commit()
        self.__password = new

    @property
    def user_type(self):
        return self.__user_type

class Cart:
    def __init__(self, userID, cardID, quantity):
        self.__userID = userID
        self.__cardID = cardID
        self.__quantity = quantity

    @property
    def userID(self):
        return self.__userID

    @property
    def cardID(self):
        return self.__cardID
    
    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        c = connector()
        sql = f'UPDATE cart SET quantity = {value} WHERE cardID = {self.__cardID}'
        c.execute(sql)
        c.commit()
        self.__quantity = value

    @property
    def cardInfo(self):
        c = connector()
        cursor = c.cursor()
        sql = f'SELECT * FROM card WHERE cardID = {self.__cardID}'
        cursor.execute(sql)
        card_sql = cursor.fetchone()
        card = Card(card_sql[0], card_sql[1], card_sql[2], card_sql[3], card_sql[4],card_sql[5], card_sql[6], card_sql[7], card_sql[8])
        return card
    
class Order:
    def __init__(self, orderID:int, userID:int, date:datetime, total:float):
        self.__orderID = orderID
        self.__userID = userID
        self.__date = date
        self.__total = total
        #cards

    @property
    def orderID(self):
        return self.__orderID

    @property
    def userID(self):
        return self.__userID

    @property
    def date(self):
        return self.__date
    
    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, total):
        c = connector()
        sql = f'UPDATE "order" SET total = {total} WHERE orderID = {self.__orderID}'
        c.execute(sql)
        c.commit()
        self.__total = total

class CardOrders:
    def __init__(self, orderID:int, cardID:int, quantity:int, unit_price:float):
        self.__orderID = orderID
        self.__cardID = cardID 
        self.__quantity = quantity 
        self.__unit_price = unit_price
        #cardInfo

    @property
    def orderID(self):
        return self.__orderID

    @property
    def cardID(self):
        return self.__cardID

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if value != self.__quantity:
            self.__quantity = value
            c = connector()
            sql = f'UPDATE cardorders SET quantity = {value} WHERE cardID = {self.__cardID} AND orderID = {self.__orderID}'
            c.execute(sql)
            c.commit()

    @property
    def unit_price(self):
        return self.__unit_price

    @unit_price.setter
    def unit_price(self, price):
        if price != self.__unit_price:
            self.__unit_price = price
            c = connector()
            sql = f'UPDATE cardorders SET unit_price = {price} WHERE cardID = {self.__cardID} AND orderID = {self.__orderID}'
            c.execute(sql)
            c.commit()