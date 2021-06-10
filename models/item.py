import sqlite3
from db import db


# Luôn luôn sử dụng self cho đối số đầu tiên cho các phương thức thể hiện.
# Luôn luôn sử dụng cls cho đối số đầu tiên cho các phương thức class.


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # ItemModel.query.filter_by(name=name)
    # select * from items where name = name

    # ItemModel.query.filter_by(name=name).filter_by(id=1)

    # ItemModel.query.filter_by(name=name).first()
    # select * from items where name=name LIMIT 1
    #################################

    #    connection = sqlite3.connect('data.db')
    #    cursor = connection.cursor()

    #    query = "SELECT * FROM items WHERE name=?"
    #    result = cursor.execute(query, (name,))
    #    row = result.fetchone()
    #   connection.close()

    #    if row:  # is not None
    #        # return cls(row[0], row[1])
    #        return cls(*row)

    def save_to_db(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO items VALUES(?, ?)"
        # cursor.execute(query, (self.name, self.price))
        #
        # connection.commit()
        # connection.close()
        db.session.add(self)
        db.session.commit()
        # sử dụng cho cả update và insert

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
