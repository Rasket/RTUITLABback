from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import threading, time
import json
import werkzeug 


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///factory_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Products(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	Shop = db.Column(db.String(120))
	Product = db.Column(db.String(120))
	Amount = db.Column(db.Integer)


def transfer():
    threading.Timer(25, transfer).start()#каждый час поставка 3600 sec
    temp_prod = Products(Shop = "First", Product = "first", Amount = "1")
    db.session.add(temp_prod)
    db.session.commit()
    '''
    json_data = json.dumps({"shop" : "First", "product" : 
        { "1" : "first"}, "amount" : {"1":"1"}})
    '''
    query = Products.query.all()
    element_del = []
#=============================================================
    try:
        temp_prod, temp_amount = {}, {}#  словарик, в который пишутся все продукты
        key = 0# ключик словарика
        for element in query:
            temp_prod[key] = element.Product
            temp_amount[key] = element.Amount    
            key += 1
            element_del.append(e тlement.id)
        temp_json = json.dumps({"shop" : element.Shop, "product" : temp_prod, "amount" : temp_amount})
        r = requests.post("http://shop:9998/api/products/", data = temp_json)
        if r.text[1:-2] == 'GET':
            print('Allright')                        
        else:
            print('Some error occured')
    except Exception as e:
        print('No connect')
    for delete in element_del:
        delete_q = Products.__table__.delete().where(Products.id == delete)
        db.session.execute(delete_q)
    db.session.commit()
    return 0
#=============================================================
'''    
    try:
        for element in query:
            temp_json = json.dumps({"shop" : element.Shop, "product" : element.Product, "amount" : element.Amount})
            r = requests.post("http://127.0.0.1:9998/api/products/", data = temp_json)
            if r.text[1:-2] == 'GET':
                print('Allright')
                element_del.append(element.id)

            else:
                print('Some error occured')
            # вот это вообще не штатный случай, так как подключение есть, но ответ некорректный
            # все также пишем на склад
    except:
    	print('No connect')
    for element in element_del:
    	Products.query.filter_by(id = int(element)).delete()
    	db.session.commit()
'''
#==============================================================






'''
Завод производит продукты на склад
С склада переодически идет проверка на доступность магазина
Если магазин доступен, то отсылаются продукты, иначе записываются на склад
'''





if __name__ == "__main__":
	if werkzeug.serving.is_running_from_reloader():
		transfer()
	else:
		pass
	app.run(port=7777, debug=False)