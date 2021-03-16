from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

   
'''
Models
'''
class Shop(db.Model):# модель Магазинов
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(120))# имя магазина
    category = db.Column(db.String(120))# категория товаров магазина

class Product(db.Model):# модель Продуктов
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    shop_id = db.Column(db.Integer)# id магазина торгующего товарами
    name = db.Column(db.String(120))# имя товара
    description = db.Column(db.String(250))# описание (по ТЗ, вроде как использовать не надо)
    cost = db.Column(db.Integer)# стоимость
    amount = db.Column(db.Integer)# кол-во

    def __repr__(self):
        return f'<Product {self.name} {self.description} {self.amount}>' # удобный print

class Check(db.Model):# модель Чеков
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    shop = db.Column(db.String)
    id_buy = db.Column(db.Integer)# id покупателя
    products = db.Column(db.String(500))
    amounts = db.Column(db.Integer)
    category = db.Column(db.String(140))# категория товара
    cost = db.Column(db.Integer)# стоимость всей покупки
    type_pay = db.Column(db.String(140))# способ оплаты
    date = db.Column(db.String, default = str(datetime.utcnow))# дата по Гринвичу
'''
End of models
'''