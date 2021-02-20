from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
'''
Документацию не постандарту PEP8 (не на английском), но думаю на это все равно
Основная задача микросервиса shop принимать и обрабатывать 3 типа запросов
1. Запрос от пользователя на приобретение товара
2. Запрос от пользователя на чек о покупке по номеру покупавшего
3. Пост запрос от завода
'''


#  Настройка фласка, апи и БД
app = Flask(__name__)
app.secret_key = b'_5#  y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
api = Api(app)


#  Класс для апи запросов
class Products(Resource):
    def get(self):
        id_buy = request.args.get('id', None)#   id покупателя
        shop = request.args.get('shop', None)#  магазин, из которого покупаем
        product = str(request.args.get('product', None))#  приобретаемые продукты
        amount  = request.args.get('amount', None)#  кол-во товара
        type_pay  = request.args.get('type_pay', None)#  тип оплаты (тут просто строка, так что данные любые)
        #  получаем из апи запроса данные для покупки
        p = Product.query.filter_by(name = product).first()#  получаем запись о продукте
        s = Shop.query.filter_by(name = shop).first()#  получаем инфо о магазине
        if p.shop_id == s.id: #  проверяем что магазин и товар связаны
            if (p.amount >= int(amount)) and (int(amount) > 0):# проверяем кол-во товара 
                p.amount -= int(amount)#  "приобретаем"
                temp_check = Check(id_buy = id_buy, date = datetime.utcnow()
                , cost = p.cost*int(amount), category = s.category, type_pay = type_pay)# создаем чек о приобретение
                db.session.add(temp_check)
                db.session.commit()# коммитик
                return 'Buy'# Подтверждаем что операция прошла успешно
            else:
            	return 'Out of product' # В случае ошибки с кол-вом товара (меньше 0) или его нехваткой пишем об этом
        return 'Incorrect data' # в случае некорректных данных
    def post(self):# Будущий пост запрос для завода
        pass

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
    id_buy = db.Column(db.Integer)# id покупателя
    date = db.Column(db.DateTime, default = datetime.utcnow)# дата по Гринвичу
    cost = db.Column(db.Integer)# стоимость всей покупки
    category = db.Column(db.String(140))# категория товара
    type_pay = db.Column(db.String(140))# способ оплаты

'''
End of models
'''



api.add_resource(Products, "/api/products")# добавляем api


@app.route('/check/<id>', methods=['GET'])
def getcheck(id):# рут для получения чека
    u = Check.query.filter_by(id_buy = id).all()    
    ret = {}# словарик, в который пишутся все чеки
    key = 0# ключик словарика
    for i in u:
        ret[key] = {'id' : i.id, 'id_buy' : i.id_buy, 'date' : i.date,
            'category' : i.category, 'cost' : i.cost, 'type_pay' : i.type_pay}# вытаскиваем поля из записей
        key += 1
    return jsonify(ret)
if __name__ == "__main__":
	app.run(debug=True)# отключить debug