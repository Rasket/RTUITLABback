from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Shop
from models import Check
from models import Product
from datetime import datetime
import json
import requests
import socket
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
#db = SQLAlchemy(app)
db.init_app(app)
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
        dict_data = {"id_buy" : str(id_buy), "shop" : str(s.name), "data" : str(datetime.utcnow())
            , "products" : str(temp_prod), "amounts" : str(temp_amount)
            , "cost" : str(cost), "category" : str(s.category)
            , "type_pay" : str(type_pay)}
        element_del = []
        try:                
            json_data_check = json.dumps(dict_data)
            requests.post("http://check:8888/getcheck/", data = json_data_check)
            checks = Check.query.all()
            for element in checks:
                json_data_check = json.dumps({"id_buy" : str(element.id_buy), "shop" : str(element.shop), "data" : str(element.date)
            , "products" : str(element.products), "amounts" : str(element.amounts)
            , "cost" : str(element.cost), "category" : str(element.category)
            , "type_pay" : str(element.type_pay)})
                requests.post("http://check:8888/getcheck/", data = json_data_check)                
                element_del.append(element.id)

        except Exception as e:
            temp_check = Check(id_buy = dict_data["id_buy"], shop = dict_data["shop"], date = dict_data["data"]
                , products = dict_data["products"], amounts = dict_data["amounts"]
                , cost = dict_data["cost"], category = dict_data["category"], type_pay = dict_data["type_pay"])
            db.session.add(temp_check)
        for delete in element_del:
            delete_q = Check.__table__.delete().where(Check.id == delete)
            db.session.execute(delete_q)
            
        db.session.commit()
        #temp_check = Check(id_buy = id_buy, date = datetime.utcnow(), products = temp_prod, amounts = temp_amount
        #        , cost = cost, category = s.category, type_pay = type_pay)
        #db.session.add(temp_check)
        #db.session.commit()
        return 'Buy'
        # -------------------------------------
        '''
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
        '''
    def post(self):# пост запрос для завода
    #присылаем продукты в магазин
        json_data = request.get_json(force=True)
        shop_name = json_data['shop']# переменная не используется, но по логике продукты присылаются в магазин
        products = json_data['product']# продукты присылаются строкой
        amounts = json_data['amount']# кол-во продуктов


        # если продукты отправляются пачкой
        
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
        '''
        # если продукты по одной записи
        p = Product.query.filter_by(name = products).first()
        p.amount += int(amounts) 
        
        '''
        db.session.commit()
        return 'GET' #ключ того, что все прошло успешно







api.add_resource(Products, "/api/products/")# добавляем api

'''
@app.route('/check/<int:id>', methods=['GET'])
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
'''

@app.route('/api/getcheck/', methods=['GET'])
def get_all_check():
    checks = Check.query.all()
    for element in checks:
        json_data_check = json.dumps({"id_buy" : str(element.id_buy), "shop" : str(element.shop), "data" : str(element.date)
            , "products" : str(element.products), "amounts" : str(element.amounts)
            , "cost" : str(element.cost), "category" : str(element.category)
            , "type_pay" : str(element.type_pay)})
        try:
            requests.post("http://check:8888/getcheck/", data = json_data_check)
        except Exception as e:
        	return 'error'
    return 'SEND'                


if __name__ == "__main__":
	#json_data_check = json.dumps()
	#requests.post("http://"+ socket.gethostname() + ":8888/getcheck/", data = json_data_check)
    app.run(host="0.0.0.0", port=9998, debug=False)# отключить debug