from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import threading, time
import json
import werkzeug 
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Products(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	Shop = db.Column(db.String(120))
	Product = db.Column(db.String(120))
	Amount = db.Column(db.String(120))


def transfer():
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
            element_del.append(element.id)
        temp_json = json.dumps({"shop" : element.Shop, "product" : temp_prod, "amount" : temp_amount})
        try:
            r = requests.post("http://shop:9998/api/products/", data = temp_json)
        except:
            print('Some error occured')
        if r.text[1:-2] == 'GET':
                for delete in element_del:
                    delete_q = Products.__table__.delete().where(Products.id == delete)
                    db.session.execute(delete_q)                       
        else:
            print('Some error occured')
    except Exception as e:
        print('No connect')
    #каждый час поставка 3600 sec
    temp_product = Products(Shop = "First", Product = "first", Amount = "1")
    db.session.add(temp_product) 
    db.session.commit()
    threading.Timer(25, transfer).start()
    return 0



if __name__ == "__main__":
    #'''
    if werkzeug.serving.is_running_from_reloader():
        pass
    else:
         transfer()
    #    '''
    #transfer()
    app.run(port=7777, debug=False, host = "0.0.0.0")