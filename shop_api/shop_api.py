from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import requests
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


parser = reqparse.RequestParser()
parser.add_argument('Shop', 'Product', 'Amount')

#  Класс для апи запросов
class Products(Resource):
    def get(self):
        json_data = request.get_json(force=True)
        id_buy = json_data['id']
        shop = json_data['shop']
        products = json_data['products']
        amounts = json_data['amounts']
        type_pay = json_data['type_pay']   
        temp_prod = []
        temp_amount = []

        for i in products:
            temp_prod.append(products[i])
        products = temp_prod
        for i in amounts:
            temp_amount.append(amounts[i])
        amounts = temp_amount
             
        ''' получение аргументов из строки
        id_buy = request.args.get('id', None)#   id покупателя
        shop = request.args.get('shop', None)#  магазин, из которого покупаем
        products = str(request.args.get('products', None))#  приобретаемые продукты
        amounts  = request.args.get('amounts', None)#  кол-во товара
        type_pay  = request.args.get('type_pay', None)#  тип оплаты (тут просто строка, так что данные любые)
        #  получаем из апи запроса данные для покупки
        #  получаем запись о продукте
        #  получаем инфо о магазине
        products = products.split(',')
        amounts = amounts.split(',')
        '''
        product = [list(temp) for temp in zip(map(int, amounts), products)]
        temp_prod = ""
        temp_amount = ""
        

        s = Shop.query.filter_by(name = shop).first()
        cost = 0
        for prod in product:
            temp_prod += prod[1] + " "
            temp_amount += str(prod[0]) + " "
            p = Product.query.filter_by(name = prod[1]).first()
            if p.amount >= prod[0] and prod[0] > 0:
                if p.shop_id == s.id:   
                    p.amount -= int(prod[0])
                    cost += int(prod[0]) * p.cost
                else:
                    return 'Incorrect shop'
            else:
                return 'Incorrect amount'
        json_data_check = json.dumps({"id_buy" : str(id_buy), "shop" : str(s.name), "data" : str(datetime.utcnow()), "products" : str(temp_prod), "amounts" : str(temp_amount), "cost" : str(cost), "category" : str(s.category), "type_pay" : str(type_pay)})
        requests.post("http://127.0.0.1:8888/getcheck/", data = json_data_check)
        db.session.commit()
        #temp_check = Check(id_buy = id_buy, date = datetime.utcnow(), products = temp_prod, amounts = temp_amount
        #        , cost = cost, category = s.category, type_pay = type_pay)
        #db.session.add(temp_check)
        #db.session.commit()
        return 'Buy'
        # -------------------------------------
        if p.shop_id == s.id: #  проверяем что магазин и товары связаны
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
    def post(self):# пост запрос для завода
    #присылаем продукты в магазин
        json_data = request.get_json(force=True)
        shop_name = json_data['shop']# переменная не используется, но по логике продукты присылаются в магазин
        products = json_data['product']# продукты присылаются строкой
        amounts = json_data['amount']# кол-во продуктов
        temp_prod = []
        temp_amount = []

        for i in products:
            temp_prod.append(products[i])
        products = temp_prod

        for i in amounts:
            temp_amount.append(amounts[i])
        amounts = temp_amount

        product = [list(temp) for temp in zip(map(int, amounts), products)]        
        for prod in product:
            p = Product.query.filter_by(name = prod[1]).first() 
            p.amount += int(prod[0])
        db.session.commit()
        return 'GET' #ключ того, что все прошло успешно



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
    products = db.Column(db.String(500))
    amounts = db.Column(db.Integer)
    category = db.Column(db.String(140))# категория товара
    cost = db.Column(db.Integer)# стоимость всей покупки
    type_pay = db.Column(db.String(140))# способ оплаты
    date = db.Column(db.DateTime, default = datetime.utcnow)# дата по Гринвичу
    
'''
End of models
'''



api.add_resource(Products, "/api/products/")# добавляем api


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

@app.route('/check/', methods=['GET'])
def getcheck_alt():# рут для получения чека
    json_data = request.get_json(force=True)
    id_buy = json_data['id']
    u = Check.query.filter_by(id_buy = id_buy).all() 
    ret = {}# словарик, в который пишутся все чеки
    key = 0# ключик словарика
    for i in u:
        ret[key] = {'id' : i.id, 'id_buy' : i.id_buy, 'products' : i.products, 'amounts' : i.amounts,
            'category' : i.category, 'cost' : i.cost, 'date' : i.date, 'type_pay' : i.type_pay}# вытаскиваем поля из записей
        key += 1
    return jsonify(ret)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9998, debug=True)# отключить debug